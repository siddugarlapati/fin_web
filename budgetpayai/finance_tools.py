"""
Finance calculation and analysis tools for Aiza
"""
import json
from datetime import datetime
from typing import List, Dict, Any


class FinanceCalculator:
    """Financial calculations and analysis"""
    
    @staticmethod
    def calculate_budget(income: float, expenses: Dict[str, float]) -> Dict[str, Any]:
        """Calculate budget breakdown"""
        total_expenses = sum(expenses.values())
        savings = income - total_expenses
        savings_rate = (savings / income * 100) if income > 0 else 0
        
        return {
            "income": income,
            "total_expenses": total_expenses,
            "savings": savings,
            "savings_rate": f"{savings_rate:.1f}%",
            "expense_breakdown": expenses,
            "status": "healthy" if savings > 0 else "overspending"
        }
    
    @staticmethod
    def categorize_expense(description: str, amount: float) -> Dict[str, Any]:
        """Categorize expenses based on description"""
        categories = {
            "food": ["restaurant", "grocery", "food", "cafe", "lunch", "dinner"],
            "transport": ["uber", "gas", "parking", "transit", "taxi", "bus"],
            "utilities": ["electric", "water", "internet", "phone", "bill"],
            "entertainment": ["movie", "netflix", "spotify", "game", "concert"],
            "shopping": ["amazon", "store", "mall", "clothing", "shoes"],
            "health": ["pharmacy", "doctor", "hospital", "gym", "fitness"],
            "housing": ["rent", "mortgage", "insurance", "maintenance"]
        }
        
        desc_lower = description.lower()
        category = "other"
        
        for cat, keywords in categories.items():
            if any(keyword in desc_lower for keyword in keywords):
                category = cat
                break
        
        return {
            "description": description,
            "amount": amount,
            "category": category,
            "date": datetime.now().isoformat()
        }
    
    @staticmethod
    def analyze_spending(transactions: List[Dict]) -> Dict[str, Any]:
        """Analyze spending patterns"""
        if not transactions:
            return {"error": "No transactions to analyze"}
        
        category_totals = {}
        total_spent = 0
        
        for txn in transactions:
            category = txn.get("category", "other")
            amount = txn.get("amount", 0)
            category_totals[category] = category_totals.get(category, 0) + amount
            total_spent += amount
        
        # Calculate percentages
        category_percentages = {
            cat: f"{(amt/total_spent*100):.1f}%" 
            for cat, amt in category_totals.items()
        }
        
        # Find top spending category
        top_category = max(category_totals.items(), key=lambda x: x[1])
        
        return {
            "total_spent": total_spent,
            "category_totals": category_totals,
            "category_percentages": category_percentages,
            "top_category": top_category[0],
            "top_category_amount": top_category[1],
            "transaction_count": len(transactions)
        }
    
    @staticmethod
    def savings_goal(target: float, current: float, monthly_save: float) -> Dict[str, Any]:
        """Calculate time to reach savings goal"""
        remaining = target - current
        if remaining <= 0:
            return {"status": "goal_reached", "message": "You've already reached your goal!"}
        
        if monthly_save <= 0:
            return {"status": "error", "message": "Monthly savings must be positive"}
        
        months_needed = remaining / monthly_save
        years = int(months_needed // 12)
        months = int(months_needed % 12)
        
        return {
            "target": target,
            "current": current,
            "remaining": remaining,
            "monthly_save": monthly_save,
            "months_needed": months_needed,
            "time_estimate": f"{years} years, {months} months" if years > 0 else f"{months} months",
            "status": "on_track"
        }
    
    @staticmethod
    def compound_interest(principal: float, rate: float, years: int, compounds_per_year: int = 12) -> Dict[str, Any]:
        """Calculate compound interest for investments"""
        amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)
        interest_earned = amount - principal
        
        return {
            "principal": principal,
            "rate": f"{rate*100:.2f}%",
            "years": years,
            "final_amount": round(amount, 2),
            "interest_earned": round(interest_earned, 2),
            "total_return": f"{(interest_earned/principal*100):.1f}%"
        }
    
    @staticmethod
    def debt_payoff(balance: float, interest_rate: float, monthly_payment: float) -> Dict[str, Any]:
        """Calculate debt payoff timeline"""
        if monthly_payment <= 0:
            return {"error": "Monthly payment must be positive"}
        
        monthly_rate = interest_rate / 12
        if monthly_rate * balance >= monthly_payment:
            return {"error": "Payment too low to cover interest"}
        
        months = 0
        remaining = balance
        total_paid = 0
        
        while remaining > 0 and months < 600:  # Cap at 50 years
            interest = remaining * monthly_rate
            principal_payment = min(monthly_payment - interest, remaining)
            remaining -= principal_payment
            total_paid += monthly_payment
            months += 1
        
        years = months // 12
        remaining_months = months % 12
        
        return {
            "original_balance": balance,
            "monthly_payment": monthly_payment,
            "months_to_payoff": months,
            "time_estimate": f"{years} years, {remaining_months} months",
            "total_paid": round(total_paid, 2),
            "total_interest": round(total_paid - balance, 2)
        }


class BudgetAnalyzer:
    """Analyze and provide budget recommendations"""
    
    @staticmethod
    def get_recommendations(income: float, expenses: Dict[str, float]) -> List[str]:
        """Provide budget recommendations based on 50/30/20 rule"""
        recommendations = []
        total_expenses = sum(expenses.values())
        
        # 50/30/20 rule: 50% needs, 30% wants, 20% savings
        needs_target = income * 0.50
        wants_target = income * 0.30
        savings_target = income * 0.20
        
        # Categorize expenses
        needs = expenses.get("housing", 0) + expenses.get("utilities", 0) + expenses.get("food", 0) + expenses.get("transport", 0)
        wants = expenses.get("entertainment", 0) + expenses.get("shopping", 0)
        savings = income - total_expenses
        
        if savings < savings_target:
            recommendations.append(f"💡 Try to save at least ${savings_target:.0f} (20% of income) per month. Currently saving ${savings:.0f}")
        
        if needs > needs_target:
            recommendations.append(f"⚠️ Essential expenses (${needs:.0f}) exceed 50% of income. Consider reducing housing or transport costs.")
        
        if wants > wants_target:
            recommendations.append(f"🎯 Discretionary spending (${wants:.0f}) is above 30% target. Look for areas to cut back.")
        
        if total_expenses > income:
            recommendations.append("🚨 URGENT: You're spending more than you earn! Review all expenses immediately.")
        
        if not recommendations:
            recommendations.append("✅ Great job! Your budget follows healthy financial principles.")
        
        return recommendations
    
    @staticmethod
    def emergency_fund_check(monthly_expenses: float, current_savings: float) -> Dict[str, Any]:
        """Check emergency fund adequacy (3-6 months expenses)"""
        min_target = monthly_expenses * 3
        ideal_target = monthly_expenses * 6
        
        if current_savings >= ideal_target:
            status = "excellent"
            message = "You have a strong emergency fund!"
        elif current_savings >= min_target:
            status = "good"
            message = "You have adequate emergency savings."
        else:
            status = "needs_improvement"
            message = f"Build your emergency fund to at least ${min_target:.0f}"
        
        return {
            "current_savings": current_savings,
            "minimum_target": min_target,
            "ideal_target": ideal_target,
            "months_covered": current_savings / monthly_expenses if monthly_expenses > 0 else 0,
            "status": status,
            "message": message
        }
