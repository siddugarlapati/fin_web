"""
Automated monthly reports and spending alerts
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json


class MonthlyReportGenerator:
    """Generate comprehensive monthly financial reports"""
    
    def __init__(self):
        self.report_sections = [
            'summary', 'spending_analysis', 'category_breakdown',
            'top_merchants', 'savings', 'predictions', 'recommendations'
        ]
    
    def generate_report(self, month_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete monthly report"""
        report = {
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'period': month_data.get('period', 'Unknown'),
            'summary': self._generate_summary(month_data),
            'spending_analysis': self._analyze_spending(month_data),
            'category_breakdown': self._category_breakdown(month_data),
            'top_merchants': self._top_merchants(month_data),
            'savings_analysis': self._savings_analysis(month_data),
            'comparisons': self._month_comparisons(month_data),
            'predictions': self._predictions(month_data),
            'recommendations': self._recommendations(month_data),
            'highlights': self._generate_highlights(month_data)
        }
        
        return report
    
    def _generate_summary(self, data: Dict) -> Dict[str, Any]:
        """Generate executive summary"""
        income = data.get('income', 0)
        expenses = data.get('total_expenses', 0)
        savings = income - expenses
        savings_rate = (savings / income * 100) if income > 0 else 0
        
        return {
            'total_income': income,
            'total_expenses': expenses,
            'net_savings': savings,
            'savings_rate': f"{savings_rate:.1f}%",
            'transaction_count': data.get('transaction_count', 0),
            'status': 'excellent' if savings_rate > 30 else 'good' if savings_rate > 20 else 'needs_improvement'
        }
    
    def _analyze_spending(self, data: Dict) -> Dict[str, Any]:
        """Analyze spending patterns"""
        expenses = data.get('expenses_by_category', {})
        total = sum(expenses.values())
        
        return {
            'total_spent': total,
            'daily_average': round(total / 30, 2),
            'largest_category': max(expenses.items(), key=lambda x: x[1]) if expenses else ('None', 0),
            'spending_trend': data.get('trend', 'stable')
        }
    
    def _category_breakdown(self, data: Dict) -> Dict[str, Any]:
        """Detailed category breakdown"""
        expenses = data.get('expenses_by_category', {})
        total = sum(expenses.values())
        
        breakdown = {}
        for category, amount in expenses.items():
            percentage = (amount / total * 100) if total > 0 else 0
            breakdown[category] = {
                'amount': amount,
                'percentage': f"{percentage:.1f}%",
                'budget_status': 'over' if amount > data.get('budget', {}).get(category, float('inf')) else 'within'
            }
        
        return breakdown
    
    def _top_merchants(self, data: Dict) -> List[Dict]:
        """Top spending merchants"""
        merchants = data.get('merchant_spending', {})
        sorted_merchants = sorted(merchants.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return [
            {'merchant': m, 'amount': a, 'rank': i+1}
            for i, (m, a) in enumerate(sorted_merchants)
        ]
    
    def _savings_analysis(self, data: Dict) -> Dict[str, Any]:
        """Savings analysis"""
        income = data.get('income', 0)
        expenses = data.get('total_expenses', 0)
        savings = income - expenses
        
        target_savings = income * 0.2  # 20% target
        
        return {
            'actual_savings': savings,
            'target_savings': target_savings,
            'difference': savings - target_savings,
            'on_track': savings >= target_savings,
            'emergency_fund_months': data.get('emergency_fund_months', 0)
        }
    
    def _month_comparisons(self, data: Dict) -> Dict[str, Any]:
        """Compare with previous months"""
        current = data.get('total_expenses', 0)
        previous = data.get('previous_month_expenses', 0)
        
        if previous > 0:
            change = ((current - previous) / previous) * 100
        else:
            change = 0
        
        return {
            'current_month': current,
            'previous_month': previous,
            'change_percent': f"{change:+.1f}%",
            'trend': 'increasing' if change > 5 else 'decreasing' if change < -5 else 'stable'
        }
    
    def _predictions(self, data: Dict) -> Dict[str, Any]:
        """Predictions for next month"""
        return {
            'predicted_expenses': data.get('predicted_next_month', 0),
            'predicted_savings': data.get('predicted_savings', 0),
            'confidence': 'medium'
        }
    
    def _recommendations(self, data: Dict) -> List[str]:
        """Personalized recommendations"""
        recommendations = []
        
        summary = self._generate_summary(data)
        savings_rate = float(summary['savings_rate'].rstrip('%'))
        
        if savings_rate < 20:
            recommendations.append("💡 Try to increase your savings rate to at least 20%")
        
        # Check category spending
        expenses = data.get('expenses_by_category', {})
        total = sum(expenses.values())
        
        for category, amount in expenses.items():
            percentage = (amount / total * 100) if total > 0 else 0
            if percentage > 30:
                recommendations.append(f"⚠️ {category.title()} spending is {percentage:.0f}% of total - consider reducing")
        
        # Subscription check
        if data.get('subscription_count', 0) > 5:
            recommendations.append("📱 You have multiple subscriptions - review and cancel unused ones")
        
        if not recommendations:
            recommendations.append("✅ Great job! Your finances are well-managed")
        
        return recommendations
    
    def _generate_highlights(self, data: Dict) -> List[str]:
        """Generate key highlights"""
        highlights = []
        
        summary = self._generate_summary(data)
        
        highlights.append(f"💰 Saved ₹{summary['net_savings']:.0f} this month ({summary['savings_rate']})")
        
        # Largest expense
        expenses = data.get('expenses_by_category', {})
        if expenses:
            largest = max(expenses.items(), key=lambda x: x[1])
            highlights.append(f"📊 Largest spending: {largest[0].title()} (₹{largest[1]:.0f})")
        
        # Transaction count
        highlights.append(f"🔢 {summary['transaction_count']} transactions processed")
        
        return highlights
    
    def export_report_text(self, report: Dict) -> str:
        """Export report as formatted text"""
        text = f"""
╔══════════════════════════════════════════════════════════╗
║          BUDGETPAY AI - MONTHLY FINANCIAL REPORT         ║
║          {report['report_date']}                         ║
╚══════════════════════════════════════════════════════════╝

📊 SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Income:          ₹{report['summary']['total_income']:,.2f}
Expenses:        ₹{report['summary']['total_expenses']:,.2f}
Net Savings:     ₹{report['summary']['net_savings']:,.2f}
Savings Rate:    {report['summary']['savings_rate']}
Status:          {report['summary']['status'].upper()}

💡 KEY HIGHLIGHTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        for highlight in report['highlights']:
            text += f"  {highlight}\n"
        
        text += f"""
📈 CATEGORY BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        for category, data in report['category_breakdown'].items():
            text += f"  {category.title():<15} ₹{data['amount']:>10,.2f}  ({data['percentage']})\n"
        
        text += f"""
🎯 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        for rec in report['recommendations']:
            text += f"  {rec}\n"
        
        text += "\n" + "═" * 60 + "\n"
        text += "Generated by BudgetPay AI - Your Smart Finance Assistant\n"
        
        return text


class SpendingAlertSystem:
    """Real-time spending alerts"""
    
    def __init__(self):
        self.alert_thresholds = {
            'budget_warning': 0.8,  # 80% of budget
            'budget_exceeded': 1.0,  # 100% of budget
            'large_transaction': 5000,  # ₹5000+
            'unusual_spending': 2.0  # 2x average
        }
    
    def check_budget_alerts(self, category: str, spent: float, budget: float) -> List[Dict]:
        """Check if spending triggers budget alerts"""
        alerts = []
        
        if budget <= 0:
            return alerts
        
        percentage = spent / budget
        
        if percentage >= self.alert_thresholds['budget_exceeded']:
            alerts.append({
                'type': 'budget_exceeded',
                'severity': 'high',
                'category': category,
                'message': f"🚨 Budget EXCEEDED for {category}! Spent ₹{spent:.0f} of ₹{budget:.0f} ({percentage*100:.0f}%)",
                'spent': spent,
                'budget': budget,
                'overspend': spent - budget
            })
        elif percentage >= self.alert_thresholds['budget_warning']:
            alerts.append({
                'type': 'budget_warning',
                'severity': 'medium',
                'category': category,
                'message': f"⚠️ Approaching budget limit for {category}. Spent ₹{spent:.0f} of ₹{budget:.0f} ({percentage*100:.0f}%)",
                'spent': spent,
                'budget': budget,
                'remaining': budget - spent
            })
        
        return alerts
    
    def check_transaction_alerts(self, transaction: Dict, user_profile: Dict) -> List[Dict]:
        """Check if transaction triggers alerts"""
        alerts = []
        
        amount = transaction.get('amount', 0)
        category = transaction.get('category', 'other')
        
        # Large transaction alert
        if amount >= self.alert_thresholds['large_transaction']:
            alerts.append({
                'type': 'large_transaction',
                'severity': 'medium',
                'message': f"💳 Large transaction detected: ₹{amount:.0f} at {transaction.get('merchant', 'Unknown')}",
                'amount': amount,
                'merchant': transaction.get('merchant')
            })
        
        # Unusual spending alert
        avg_spending = user_profile.get('average_transaction', {}).get(category, 0)
        if avg_spending > 0 and amount > avg_spending * self.alert_thresholds['unusual_spending']:
            alerts.append({
                'type': 'unusual_spending',
                'severity': 'low',
                'message': f"📊 Unusual spending in {category}: ₹{amount:.0f} (avg: ₹{avg_spending:.0f})",
                'amount': amount,
                'average': avg_spending,
                'category': category
            })
        
        return alerts
    
    def check_daily_limit(self, today_spending: float, daily_limit: float) -> Optional[Dict]:
        """Check daily spending limit"""
        if today_spending >= daily_limit:
            return {
                'type': 'daily_limit_exceeded',
                'severity': 'high',
                'message': f"🚨 Daily spending limit reached! Spent ₹{today_spending:.0f} of ₹{daily_limit:.0f}",
                'spent': today_spending,
                'limit': daily_limit
            }
        elif today_spending >= daily_limit * 0.8:
            return {
                'type': 'daily_limit_warning',
                'severity': 'medium',
                'message': f"⚠️ Approaching daily limit. Spent ₹{today_spending:.0f} of ₹{daily_limit:.0f}",
                'spent': today_spending,
                'limit': daily_limit,
                'remaining': daily_limit - today_spending
            }
        return None
    
    def get_all_alerts(self, spending_data: Dict, budgets: Dict, user_profile: Dict) -> List[Dict]:
        """Get all active alerts"""
        all_alerts = []
        
        # Check budget alerts for each category
        for category, spent in spending_data.items():
            budget = budgets.get(category, 0)
            if budget > 0:
                alerts = self.check_budget_alerts(category, spent, budget)
                all_alerts.extend(alerts)
        
        # Sort by severity
        severity_order = {'high': 0, 'medium': 1, 'low': 2}
        all_alerts.sort(key=lambda x: severity_order.get(x['severity'], 3))
        
        return all_alerts
    
    def format_alert_notification(self, alert: Dict) -> str:
        """Format alert for notification"""
        return alert['message']


def generate_weekly_digest(transactions: List[Dict], budget: Dict) -> str:
    """Generate weekly spending digest"""
    # Calculate weekly totals
    total_spent = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'debit')
    transaction_count = len([t for t in transactions if t.get('type') == 'debit'])
    
    # Category breakdown
    category_spending = {}
    for txn in transactions:
        if txn.get('type') == 'debit':
            cat = txn.get('category', 'other')
            category_spending[cat] = category_spending.get(cat, 0) + txn.get('amount', 0)
    
    top_category = max(category_spending.items(), key=lambda x: x[1]) if category_spending else ('None', 0)
    
    digest = f"""
📅 WEEKLY SPENDING DIGEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 Total Spent: ₹{total_spent:,.2f}
🔢 Transactions: {transaction_count}
📊 Top Category: {top_category[0].title()} (₹{top_category[1]:,.2f})
📈 Daily Average: ₹{total_spent/7:,.2f}

Keep tracking your expenses with BudgetPay AI! 🚀
"""
    
    return digest
