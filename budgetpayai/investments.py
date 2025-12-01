"""
Investment analysis, portfolio tracking, and SIP recommendations
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any
import statistics


class PortfolioAnalyzer:
    """Analyze investment portfolio"""
    
    def __init__(self):
        self.risk_categories = {
            'very_low': {'stocks': 0.1, 'bonds': 0.7, 'cash': 0.2},
            'low': {'stocks': 0.3, 'bonds': 0.5, 'cash': 0.2},
            'moderate': {'stocks': 0.5, 'bonds': 0.3, 'cash': 0.2},
            'high': {'stocks': 0.7, 'bonds': 0.2, 'cash': 0.1},
            'very_high': {'stocks': 0.9, 'bonds': 0.05, 'cash': 0.05}
        }
    
    def analyze_portfolio(self, holdings: List[Dict]) -> Dict[str, Any]:
        """Analyze complete portfolio"""
        total_value = sum(h.get('current_value', 0) for h in holdings)
        total_invested = sum(h.get('invested', 0) for h in holdings)
        
        # Calculate returns
        total_returns = total_value - total_invested
        returns_percent = (total_returns / total_invested * 100) if total_invested > 0 else 0
        
        # Asset allocation
        allocation = self._calculate_allocation(holdings, total_value)
        
        # Risk score
        risk_score = self._calculate_risk_score(allocation)
        
        # Diversification score
        diversification = self._calculate_diversification(holdings)
        
        return {
            'total_value': round(total_value, 2),
            'total_invested': round(total_invested, 2),
            'total_returns': round(total_returns, 2),
            'returns_percent': round(returns_percent, 2),
            'allocation': allocation,
            'risk_score': risk_score,
            'diversification_score': diversification,
            'holdings_count': len(holdings),
            'top_performers': self._get_top_performers(holdings),
            'recommendations': self._get_recommendations(allocation, risk_score)
        }
    
    def _calculate_allocation(self, holdings: List[Dict], total: float) -> Dict[str, float]:
        """Calculate asset allocation"""
        allocation = {}
        
        for holding in holdings:
            asset_type = holding.get('type', 'other')
            value = holding.get('current_value', 0)
            percentage = (value / total * 100) if total > 0 else 0
            
            if asset_type not in allocation:
                allocation[asset_type] = 0
            allocation[asset_type] += percentage
        
        return {k: round(v, 2) for k, v in allocation.items()}
    
    def _calculate_risk_score(self, allocation: Dict[str, float]) -> Dict[str, Any]:
        """Calculate portfolio risk score"""
        # Simple risk scoring based on allocation
        stocks_pct = allocation.get('stocks', 0) + allocation.get('equity', 0)
        bonds_pct = allocation.get('bonds', 0) + allocation.get('debt', 0)
        
        if stocks_pct > 70:
            risk_level = 'high'
        elif stocks_pct > 50:
            risk_level = 'moderate'
        elif stocks_pct > 30:
            risk_level = 'low'
        else:
            risk_level = 'very_low'
        
        return {
            'level': risk_level,
            'score': round(stocks_pct, 1),
            'description': f"{risk_level.replace('_', ' ').title()} risk portfolio"
        }
    
    def _calculate_diversification(self, holdings: List[Dict]) -> Dict[str, Any]:
        """Calculate diversification score"""
        if not holdings:
            return {'score': 0, 'level': 'poor'}
        
        # Count unique asset types and sectors
        asset_types = set(h.get('type') for h in holdings)
        sectors = set(h.get('sector') for h in holdings if h.get('sector'))
        
        # Simple diversification score
        score = min(100, (len(asset_types) * 20 + len(sectors) * 10))
        
        if score >= 80:
            level = 'excellent'
        elif score >= 60:
            level = 'good'
        elif score >= 40:
            level = 'moderate'
        else:
            level = 'poor'
        
        return {
            'score': score,
            'level': level,
            'asset_types': len(asset_types),
            'sectors': len(sectors)
        }
    
    def _get_top_performers(self, holdings: List[Dict]) -> List[Dict]:
        """Get top performing investments"""
        performers = []
        
        for holding in holdings:
            invested = holding.get('invested', 0)
            current = holding.get('current_value', 0)
            if invested > 0:
                returns = ((current - invested) / invested) * 100
                performers.append({
                    'name': holding.get('name'),
                    'returns': round(returns, 2),
                    'value': current
                })
        
        return sorted(performers, key=lambda x: x['returns'], reverse=True)[:5]
    
    def _get_recommendations(self, allocation: Dict, risk_score: Dict) -> List[str]:
        """Get portfolio recommendations"""
        recommendations = []
        
        stocks_pct = allocation.get('stocks', 0) + allocation.get('equity', 0)
        bonds_pct = allocation.get('bonds', 0) + allocation.get('debt', 0)
        
        if stocks_pct > 80:
            recommendations.append("⚠️ High equity exposure - consider adding bonds for stability")
        
        if bonds_pct > 70:
            recommendations.append("💡 Conservative portfolio - consider adding equity for growth")
        
        if len(allocation) < 3:
            recommendations.append("📊 Limited diversification - consider adding more asset classes")
        
        if not recommendations:
            recommendations.append("✅ Well-balanced portfolio")
        
        return recommendations


class SIPRecommender:
    """Recommend SIP investments"""
    
    def __init__(self):
        self.fund_categories = {
            'large_cap': {'risk': 'low', 'expected_return': 12},
            'mid_cap': {'risk': 'moderate', 'expected_return': 15},
            'small_cap': {'risk': 'high', 'expected_return': 18},
            'index': {'risk': 'low', 'expected_return': 11},
            'debt': {'risk': 'very_low', 'expected_return': 7},
            'hybrid': {'risk': 'moderate', 'expected_return': 10}
        }
    
    def recommend_sip(self, user_profile: Dict) -> List[Dict]:
        """Recommend SIP based on user profile"""
        age = user_profile.get('age', 30)
        risk_appetite = user_profile.get('risk_appetite', 'moderate')
        monthly_income = user_profile.get('monthly_income', 50000)
        investment_amount = user_profile.get('sip_amount', 5000)
        goal = user_profile.get('goal', 'wealth_creation')
        
        recommendations = []
        
        # Age-based allocation
        equity_allocation = min(100, 100 - age)
        debt_allocation = 100 - equity_allocation
        
        # Adjust for risk appetite
        if risk_appetite == 'high':
            equity_allocation = min(100, equity_allocation + 10)
        elif risk_appetite == 'low':
            equity_allocation = max(0, equity_allocation - 20)
        
        debt_allocation = 100 - equity_allocation
        
        # Recommend funds
        equity_amount = investment_amount * (equity_allocation / 100)
        debt_amount = investment_amount * (debt_allocation / 100)
        
        if equity_amount > 0:
            recommendations.append({
                'category': 'Equity Funds',
                'allocation': f"{equity_allocation}%",
                'amount': round(equity_amount, 2),
                'suggested_funds': [
                    {'name': 'Large Cap Index Fund', 'amount': round(equity_amount * 0.5, 2)},
                    {'name': 'Mid Cap Growth Fund', 'amount': round(equity_amount * 0.3, 2)},
                    {'name': 'Small Cap Fund', 'amount': round(equity_amount * 0.2, 2)}
                ],
                'expected_return': '12-15% p.a.',
                'risk': 'Moderate to High'
            })
        
        if debt_amount > 0:
            recommendations.append({
                'category': 'Debt Funds',
                'allocation': f"{debt_allocation}%",
                'amount': round(debt_amount, 2),
                'suggested_funds': [
                    {'name': 'Corporate Bond Fund', 'amount': round(debt_amount * 0.6, 2)},
                    {'name': 'Liquid Fund', 'amount': round(debt_amount * 0.4, 2)}
                ],
                'expected_return': '6-8% p.a.',
                'risk': 'Low'
            })
        
        return recommendations
    
    def calculate_sip_returns(self, monthly_amount: float, years: int, 
                             expected_return: float = 12) -> Dict[str, Any]:
        """Calculate SIP returns"""
        months = years * 12
        monthly_rate = expected_return / 12 / 100
        
        # Future value of SIP
        if monthly_rate > 0:
            future_value = monthly_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
        else:
            future_value = monthly_amount * months
        
        total_invested = monthly_amount * months
        returns = future_value - total_invested
        
        return {
            'monthly_investment': monthly_amount,
            'duration_years': years,
            'expected_return': f"{expected_return}%",
            'total_invested': round(total_invested, 2),
            'future_value': round(future_value, 2),
            'total_returns': round(returns, 2),
            'returns_percent': round((returns / total_invested * 100), 2)
        }
    
    def suggest_sip_amount(self, monthly_income: float, goal_amount: float, 
                          years: int) -> Dict[str, Any]:
        """Suggest SIP amount to reach goal"""
        # Assume 12% return
        monthly_rate = 0.12 / 12
        months = years * 12
        
        # Calculate required monthly SIP
        if monthly_rate > 0:
            required_sip = goal_amount * monthly_rate / (((1 + monthly_rate) ** months - 1) * (1 + monthly_rate))
        else:
            required_sip = goal_amount / months
        
        # Check affordability
        affordable = required_sip <= monthly_income * 0.3
        
        return {
            'goal_amount': goal_amount,
            'duration_years': years,
            'required_monthly_sip': round(required_sip, 2),
            'percentage_of_income': round((required_sip / monthly_income * 100), 2),
            'affordable': affordable,
            'recommendation': 'Achievable' if affordable else 'Consider longer duration or lower goal'
        }


class RiskProfiler:
    """Assess investment risk profile"""
    
    def __init__(self):
        self.risk_questions = [
            {'q': 'age', 'weight': 0.2},
            {'q': 'income_stability', 'weight': 0.15},
            {'q': 'investment_experience', 'weight': 0.15},
            {'q': 'time_horizon', 'weight': 0.2},
            {'q': 'loss_tolerance', 'weight': 0.3}
        ]
    
    def assess_risk_profile(self, answers: Dict) -> Dict[str, Any]:
        """Assess user's risk profile"""
        score = 0
        
        # Age scoring (younger = higher risk capacity)
        age = answers.get('age', 30)
        if age < 30:
            score += 25
        elif age < 40:
            score += 20
        elif age < 50:
            score += 15
        else:
            score += 10
        
        # Income stability
        income_stability = answers.get('income_stability', 'stable')
        if income_stability == 'very_stable':
            score += 20
        elif income_stability == 'stable':
            score += 15
        else:
            score += 10
        
        # Investment experience
        experience = answers.get('investment_experience', 'beginner')
        if experience == 'expert':
            score += 20
        elif experience == 'intermediate':
            score += 15
        else:
            score += 10
        
        # Time horizon
        time_horizon = answers.get('time_horizon', 5)
        if time_horizon > 10:
            score += 25
        elif time_horizon > 5:
            score += 20
        else:
            score += 15
        
        # Loss tolerance
        loss_tolerance = answers.get('loss_tolerance', 'moderate')
        if loss_tolerance == 'high':
            score += 30
        elif loss_tolerance == 'moderate':
            score += 20
        else:
            score += 10
        
        # Determine risk profile
        if score >= 85:
            profile = 'aggressive'
            equity_allocation = 80
        elif score >= 70:
            profile = 'moderately_aggressive'
            equity_allocation = 65
        elif score >= 55:
            profile = 'moderate'
            equity_allocation = 50
        elif score >= 40:
            profile = 'conservative'
            equity_allocation = 35
        else:
            profile = 'very_conservative'
            equity_allocation = 20
        
        return {
            'risk_score': score,
            'risk_profile': profile,
            'recommended_equity_allocation': equity_allocation,
            'recommended_debt_allocation': 100 - equity_allocation,
            'description': self._get_profile_description(profile),
            'suitable_investments': self._get_suitable_investments(profile)
        }
    
    def _get_profile_description(self, profile: str) -> str:
        """Get risk profile description"""
        descriptions = {
            'aggressive': 'High risk tolerance, seeking maximum growth',
            'moderately_aggressive': 'Above average risk tolerance, growth focused',
            'moderate': 'Balanced approach to risk and returns',
            'conservative': 'Low risk tolerance, stability focused',
            'very_conservative': 'Very low risk tolerance, capital preservation'
        }
        return descriptions.get(profile, 'Moderate risk profile')
    
    def _get_suitable_investments(self, profile: str) -> List[str]:
        """Get suitable investment types"""
        investments = {
            'aggressive': ['Small Cap Funds', 'Sectoral Funds', 'International Equity'],
            'moderately_aggressive': ['Mid Cap Funds', 'Large Cap Funds', 'Balanced Funds'],
            'moderate': ['Index Funds', 'Hybrid Funds', 'Large Cap Funds'],
            'conservative': ['Debt Funds', 'Balanced Funds', 'FDs'],
            'very_conservative': ['Liquid Funds', 'FDs', 'Government Bonds']
        }
        return investments.get(profile, ['Balanced Funds'])


class NetWorthTracker:
    """Track net worth over time"""
    
    def __init__(self):
        pass
    
    def calculate_net_worth(self, assets: Dict, liabilities: Dict) -> Dict[str, Any]:
        """Calculate current net worth"""
        total_assets = sum(assets.values())
        total_liabilities = sum(liabilities.values())
        net_worth = total_assets - total_liabilities
        
        return {
            'total_assets': round(total_assets, 2),
            'total_liabilities': round(total_liabilities, 2),
            'net_worth': round(net_worth, 2),
            'asset_breakdown': assets,
            'liability_breakdown': liabilities,
            'debt_to_asset_ratio': round((total_liabilities / total_assets * 100), 2) if total_assets > 0 else 0
        }
    
    def track_net_worth_timeline(self, historical_data: List[Dict]) -> Dict[str, Any]:
        """Track net worth over time"""
        if not historical_data:
            return {'error': 'No historical data'}
        
        # Calculate growth
        first = historical_data[0]['net_worth']
        last = historical_data[-1]['net_worth']
        growth = last - first
        growth_percent = (growth / first * 100) if first > 0 else 0
        
        # Calculate average monthly growth
        months = len(historical_data)
        avg_monthly_growth = growth / months if months > 0 else 0
        
        return {
            'current_net_worth': last,
            'starting_net_worth': first,
            'total_growth': round(growth, 2),
            'growth_percent': round(growth_percent, 2),
            'average_monthly_growth': round(avg_monthly_growth, 2),
            'data_points': months,
            'timeline': historical_data
        }
    
    def project_net_worth(self, current_net_worth: float, monthly_savings: float, 
                         years: int, investment_return: float = 12) -> Dict[str, Any]:
        """Project future net worth"""
        months = years * 12
        monthly_rate = investment_return / 12 / 100
        
        # Future value with compound interest
        if monthly_rate > 0:
            future_savings = monthly_savings * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
            future_current = current_net_worth * ((1 + monthly_rate) ** months)
        else:
            future_savings = monthly_savings * months
            future_current = current_net_worth
        
        projected_net_worth = future_current + future_savings
        
        return {
            'current_net_worth': current_net_worth,
            'monthly_savings': monthly_savings,
            'years': years,
            'expected_return': f"{investment_return}%",
            'projected_net_worth': round(projected_net_worth, 2),
            'growth': round(projected_net_worth - current_net_worth, 2)
        }
