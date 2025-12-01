"""
ML-based spending predictions and bill reminders
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import statistics


class SpendingPredictor:
    """Predict future expenses using historical data"""
    
    def __init__(self):
        self.min_data_points = 3
    
    def predict_monthly_spending(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """Predict next month's spending based on history"""
        if len(historical_data) < self.min_data_points:
            return {'error': 'Insufficient data for prediction'}
        
        # Extract monthly totals
        monthly_totals = [month['total'] for month in historical_data]
        
        # Calculate statistics
        avg_spending = statistics.mean(monthly_totals)
        std_dev = statistics.stdev(monthly_totals) if len(monthly_totals) > 1 else 0
        
        # Detect trend
        if len(monthly_totals) >= 3:
            recent_avg = statistics.mean(monthly_totals[-3:])
            older_avg = statistics.mean(monthly_totals[:-3]) if len(monthly_totals) > 3 else monthly_totals[0]
            trend = 'increasing' if recent_avg > older_avg * 1.1 else 'decreasing' if recent_avg < older_avg * 0.9 else 'stable'
        else:
            trend = 'stable'
        
        # Prediction with trend adjustment
        if trend == 'increasing':
            predicted = avg_spending * 1.05
        elif trend == 'decreasing':
            predicted = avg_spending * 0.95
        else:
            predicted = avg_spending
        
        return {
            'predicted_amount': round(predicted, 2),
            'confidence': 'high' if std_dev < avg_spending * 0.2 else 'medium' if std_dev < avg_spending * 0.4 else 'low',
            'trend': trend,
            'average_spending': round(avg_spending, 2),
            'min_expected': round(predicted - std_dev, 2),
            'max_expected': round(predicted + std_dev, 2),
            'based_on_months': len(monthly_totals)
        }
    
    def predict_category_spending(self, category_history: Dict[str, List[float]]) -> Dict[str, float]:
        """Predict spending by category"""
        predictions = {}
        
        for category, amounts in category_history.items():
            if len(amounts) >= self.min_data_points:
                avg = statistics.mean(amounts)
                # Adjust for recent trend
                if len(amounts) >= 3:
                    recent_avg = statistics.mean(amounts[-3:])
                    if recent_avg > avg * 1.1:
                        predictions[category] = recent_avg * 1.05
                    elif recent_avg < avg * 0.9:
                        predictions[category] = recent_avg * 0.95
                    else:
                        predictions[category] = avg
                else:
                    predictions[category] = avg
        
        return {k: round(v, 2) for k, v in predictions.items()}
    
    def predict_end_of_month_balance(self, current_balance: float, days_remaining: int, 
                                     daily_avg_spending: float) -> Dict[str, Any]:
        """Predict balance at end of month"""
        predicted_spending = daily_avg_spending * days_remaining
        predicted_balance = current_balance - predicted_spending
        
        return {
            'current_balance': current_balance,
            'days_remaining': days_remaining,
            'predicted_spending': round(predicted_spending, 2),
            'predicted_balance': round(predicted_balance, 2),
            'status': 'healthy' if predicted_balance > 0 else 'warning',
            'daily_budget': round(current_balance / days_remaining, 2) if days_remaining > 0 else 0
        }
    
    def predict_goal_completion(self, current_amount: float, target: float, 
                                monthly_savings: float) -> Dict[str, Any]:
        """Predict when a savings goal will be reached"""
        remaining = target - current_amount
        
        if monthly_savings <= 0:
            return {'error': 'No savings detected'}
        
        months_needed = remaining / monthly_savings
        completion_date = datetime.now() + timedelta(days=months_needed * 30)
        
        return {
            'current_amount': current_amount,
            'target': target,
            'remaining': round(remaining, 2),
            'monthly_savings': monthly_savings,
            'months_needed': round(months_needed, 1),
            'estimated_completion': completion_date.strftime('%Y-%m-%d'),
            'on_track': True if months_needed < 24 else False
        }


class BillReminder:
    """Detect and remind upcoming bills"""
    
    def __init__(self):
        self.bill_patterns = {
            'rent': {'day': 1, 'amount_variance': 0.05},
            'electricity': {'day': 5, 'amount_variance': 0.3},
            'internet': {'day': 1, 'amount_variance': 0.1},
            'mobile': {'day': 1, 'amount_variance': 0.1},
            'credit_card': {'day': 5, 'amount_variance': 0.5},
        }
    
    def detect_recurring_bills(self, transactions: List[Dict]) -> List[Dict]:
        """Detect recurring bills from transaction history"""
        # Group transactions by merchant
        merchant_txns = {}
        for txn in transactions:
            merchant = txn.get('merchant', 'Unknown')
            if merchant not in merchant_txns:
                merchant_txns[merchant] = []
            merchant_txns[merchant].append(txn)
        
        recurring_bills = []
        
        for merchant, txns in merchant_txns.items():
            if len(txns) >= 3:  # At least 3 occurrences
                # Check if amounts are similar
                amounts = [t.get('amount', 0) for t in txns]
                avg_amount = statistics.mean(amounts)
                std_dev = statistics.stdev(amounts) if len(amounts) > 1 else 0
                
                # Check if dates are regular
                if std_dev < avg_amount * 0.2:  # Low variance = recurring
                    recurring_bills.append({
                        'merchant': merchant,
                        'average_amount': round(avg_amount, 2),
                        'frequency': 'monthly',
                        'last_payment': txns[-1].get('timestamp'),
                        'next_due': self._predict_next_due(txns),
                        'confidence': 'high' if std_dev < avg_amount * 0.1 else 'medium'
                    })
        
        return recurring_bills
    
    def _predict_next_due(self, transactions: List[Dict]) -> str:
        """Predict next due date based on transaction history"""
        # Simple prediction: add 30 days to last transaction
        if transactions:
            last_date = transactions[-1].get('timestamp', datetime.now().isoformat())
            try:
                last_dt = datetime.fromisoformat(last_date)
                next_due = last_dt + timedelta(days=30)
                return next_due.strftime('%Y-%m-%d')
            except:
                pass
        return (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    def get_upcoming_bills(self, recurring_bills: List[Dict], days_ahead: int = 7) -> List[Dict]:
        """Get bills due in next N days"""
        upcoming = []
        today = datetime.now()
        cutoff = today + timedelta(days=days_ahead)
        
        for bill in recurring_bills:
            try:
                due_date = datetime.strptime(bill['next_due'], '%Y-%m-%d')
                if today <= due_date <= cutoff:
                    days_until = (due_date - today).days
                    bill['days_until_due'] = days_until
                    bill['urgency'] = 'urgent' if days_until <= 2 else 'soon'
                    upcoming.append(bill)
            except:
                continue
        
        return sorted(upcoming, key=lambda x: x['days_until_due'])
    
    def create_reminders(self, upcoming_bills: List[Dict]) -> List[str]:
        """Create reminder messages"""
        reminders = []
        
        for bill in upcoming_bills:
            days = bill['days_until_due']
            merchant = bill['merchant']
            amount = bill['average_amount']
            
            if days == 0:
                msg = f"🚨 URGENT: {merchant} bill of ₹{amount:.0f} is due TODAY!"
            elif days == 1:
                msg = f"⚠️ {merchant} bill of ₹{amount:.0f} is due TOMORROW!"
            else:
                msg = f"📅 {merchant} bill of ₹{amount:.0f} is due in {days} days"
            
            reminders.append(msg)
        
        return reminders


class SubscriptionDetector:
    """Detect and analyze subscriptions"""
    
    def __init__(self):
        self.subscription_keywords = [
            'netflix', 'prime', 'spotify', 'hotstar', 'youtube', 'apple',
            'subscription', 'membership', 'plan', 'renewal'
        ]
    
    def detect_subscriptions(self, transactions: List[Dict]) -> List[Dict]:
        """Detect active subscriptions"""
        subscriptions = []
        
        # Group by merchant
        merchant_txns = {}
        for txn in transactions:
            merchant = txn.get('merchant', '').lower()
            
            # Check if it's a subscription
            is_subscription = any(keyword in merchant for keyword in self.subscription_keywords)
            
            if is_subscription:
                if merchant not in merchant_txns:
                    merchant_txns[merchant] = []
                merchant_txns[merchant].append(txn)
        
        # Analyze each subscription
        for merchant, txns in merchant_txns.items():
            if len(txns) >= 2:  # At least 2 payments
                amounts = [t.get('amount', 0) for t in txns]
                avg_amount = statistics.mean(amounts)
                
                # Calculate frequency
                if len(txns) >= 2:
                    dates = [datetime.fromisoformat(t.get('timestamp', datetime.now().isoformat())) for t in txns]
                    dates.sort()
                    intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
                    avg_interval = statistics.mean(intervals) if intervals else 30
                    
                    frequency = 'monthly' if 25 <= avg_interval <= 35 else 'yearly' if avg_interval > 300 else 'other'
                else:
                    frequency = 'monthly'
                
                subscriptions.append({
                    'name': merchant.title(),
                    'amount': round(avg_amount, 2),
                    'frequency': frequency,
                    'annual_cost': round(avg_amount * 12, 2) if frequency == 'monthly' else round(avg_amount, 2),
                    'last_charged': txns[-1].get('timestamp'),
                    'total_payments': len(txns),
                    'status': 'active'
                })
        
        return subscriptions
    
    def suggest_cancellations(self, subscriptions: List[Dict], usage_data: Dict = None) -> List[Dict]:
        """Suggest subscriptions to cancel"""
        suggestions = []
        
        for sub in subscriptions:
            # Simple heuristics for suggestions
            annual_cost = sub['annual_cost']
            
            # Suggest if expensive and potentially unused
            if annual_cost > 1000:
                suggestions.append({
                    'subscription': sub['name'],
                    'annual_cost': annual_cost,
                    'reason': f"High cost subscription (₹{annual_cost:.0f}/year)",
                    'potential_savings': annual_cost
                })
        
        return sorted(suggestions, key=lambda x: x['potential_savings'], reverse=True)
    
    def calculate_total_subscription_cost(self, subscriptions: List[Dict]) -> Dict[str, float]:
        """Calculate total subscription costs"""
        monthly_total = sum(s['amount'] for s in subscriptions if s['frequency'] == 'monthly')
        annual_total = sum(s['annual_cost'] for s in subscriptions)
        
        return {
            'monthly_total': round(monthly_total, 2),
            'annual_total': round(annual_total, 2),
            'count': len(subscriptions),
            'average_per_subscription': round(annual_total / len(subscriptions), 2) if subscriptions else 0
        }


class AdaptiveBudgetManager:
    """AI-powered adaptive budget management"""
    
    def __init__(self):
        self.adjustment_threshold = 0.15  # 15% variance triggers adjustment
    
    def analyze_budget_performance(self, budget: Dict[str, float], 
                                   actual_spending: Dict[str, float]) -> Dict[str, Any]:
        """Analyze how well user is sticking to budget"""
        performance = {}
        
        for category, budgeted in budget.items():
            actual = actual_spending.get(category, 0)
            variance = (actual - budgeted) / budgeted if budgeted > 0 else 0
            
            performance[category] = {
                'budgeted': budgeted,
                'actual': actual,
                'variance_percent': round(variance * 100, 1),
                'status': 'over' if variance > 0.1 else 'under' if variance < -0.1 else 'on_track',
                'difference': round(actual - budgeted, 2)
            }
        
        return performance
    
    def suggest_budget_adjustments(self, performance: Dict[str, Any]) -> Dict[str, float]:
        """Suggest budget adjustments based on actual spending"""
        adjustments = {}
        
        for category, data in performance.items():
            variance = data['variance_percent'] / 100
            
            # Suggest adjustment if variance is significant
            if abs(variance) > self.adjustment_threshold:
                current = data['budgeted']
                # Adjust by 50% of the variance
                suggested = current * (1 + variance * 0.5)
                adjustments[category] = round(suggested, 2)
        
        return adjustments
    
    def create_adaptive_budget(self, historical_spending: Dict[str, List[float]], 
                              income: float) -> Dict[str, float]:
        """Create adaptive budget based on spending patterns"""
        budget = {}
        
        # Calculate average spending per category
        for category, amounts in historical_spending.items():
            if amounts:
                avg = statistics.mean(amounts)
                # Add 10% buffer
                budget[category] = round(avg * 1.1, 2)
        
        # Ensure total doesn't exceed 80% of income
        total_budget = sum(budget.values())
        if total_budget > income * 0.8:
            # Scale down proportionally
            scale_factor = (income * 0.8) / total_budget
            budget = {k: round(v * scale_factor, 2) for k, v in budget.items()}
        
        # Add savings goal (20% of income)
        budget['savings'] = round(income * 0.2, 2)
        
        return budget
