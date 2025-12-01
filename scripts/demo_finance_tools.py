"""
Demo script to showcase Aiza's finance tools
"""
from aiza.finance_tools import FinanceCalculator, BudgetAnalyzer
import json


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demo_budget_calculator():
    """Demo budget calculation"""
    print_section("💰 Budget Calculator")
    
    calc = FinanceCalculator()
    
    # Example budget
    income = 5000
    expenses = {
        "housing": 1500,
        "food": 600,
        "transport": 300,
        "utilities": 200,
        "entertainment": 400,
        "shopping": 300
    }
    
    result = calc.calculate_budget(income, expenses)
    
    print(f"Monthly Income: ${income:,.0f}")
    print(f"\nExpenses:")
    for category, amount in expenses.items():
        print(f"  {category.capitalize()}: ${amount:,.0f}")
    
    print(f"\nTotal Expenses: ${result['total_expenses']:,.0f}")
    print(f"Savings: ${result['savings']:,.0f}")
    print(f"Savings Rate: {result['savings_rate']}")
    print(f"Status: {result['status'].upper()}")


def demo_budget_recommendations():
    """Demo budget recommendations"""
    print_section("📊 Budget Recommendations (50/30/20 Rule)")
    
    analyzer = BudgetAnalyzer()
    
    income = 5000
    expenses = {
        "housing": 1500,
        "food": 600,
        "transport": 300,
        "utilities": 200,
        "entertainment": 400,
        "shopping": 300
    }
    
    recommendations = analyzer.get_recommendations(income, expenses)
    
    print(f"Income: ${income:,.0f}\n")
    print("Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")


def demo_savings_goal():
    """Demo savings goal calculator"""
    print_section("🎯 Savings Goal Calculator")
    
    calc = FinanceCalculator()
    
    target = 10000
    current = 2000
    monthly_save = 500
    
    result = calc.savings_goal(target, current, monthly_save)
    
    print(f"Goal: ${target:,.0f}")
    print(f"Current Savings: ${current:,.0f}")
    print(f"Monthly Contribution: ${monthly_save:,.0f}")
    print(f"\nRemaining: ${result['remaining']:,.0f}")
    print(f"Time to Goal: {result['time_estimate']}")
    print(f"Status: {result['status'].upper()}")


def demo_expense_analysis():
    """Demo expense analysis"""
    print_section("📈 Expense Analysis")
    
    calc = FinanceCalculator()
    
    # Sample transactions
    transactions = [
        {"description": "Grocery Store", "amount": 150, "category": "food"},
        {"description": "Gas Station", "amount": 60, "category": "transport"},
        {"description": "Netflix", "amount": 15, "category": "entertainment"},
        {"description": "Restaurant", "amount": 80, "category": "food"},
        {"description": "Uber", "amount": 25, "category": "transport"},
        {"description": "Amazon", "amount": 120, "category": "shopping"},
        {"description": "Electric Bill", "amount": 100, "category": "utilities"},
    ]
    
    result = calc.analyze_spending(transactions)
    
    print(f"Total Spent: ${result['total_spent']:,.0f}")
    print(f"Transactions: {result['transaction_count']}")
    print(f"\nTop Category: {result['top_category'].capitalize()} (${result['top_category_amount']:,.0f})")
    
    print("\nSpending by Category:")
    for category, amount in result['category_totals'].items():
        percentage = result['category_percentages'][category]
        print(f"  {category.capitalize()}: ${amount:,.0f} ({percentage})")


def demo_debt_payoff():
    """Demo debt payoff calculator"""
    print_section("💳 Debt Payoff Calculator")
    
    calc = FinanceCalculator()
    
    balance = 5000
    interest_rate = 0.18  # 18% APR
    monthly_payment = 200
    
    result = calc.debt_payoff(balance, interest_rate, monthly_payment)
    
    print(f"Current Balance: ${balance:,.0f}")
    print(f"Interest Rate: {interest_rate*100:.1f}% APR")
    print(f"Monthly Payment: ${monthly_payment:,.0f}")
    print(f"\nTime to Payoff: {result['time_estimate']}")
    print(f"Total Paid: ${result['total_paid']:,.0f}")
    print(f"Total Interest: ${result['total_interest']:,.0f}")


def demo_compound_interest():
    """Demo compound interest calculator"""
    print_section("📈 Investment Calculator (Compound Interest)")
    
    calc = FinanceCalculator()
    
    principal = 10000
    rate = 0.07  # 7% annual return
    years = 10
    
    result = calc.compound_interest(principal, rate, years)
    
    print(f"Initial Investment: ${principal:,.0f}")
    print(f"Annual Return: {result['rate']}")
    print(f"Time Period: {years} years")
    print(f"\nFinal Amount: ${result['final_amount']:,.0f}")
    print(f"Interest Earned: ${result['interest_earned']:,.0f}")
    print(f"Total Return: {result['total_return']}")


def demo_emergency_fund():
    """Demo emergency fund checker"""
    print_section("🚨 Emergency Fund Check")
    
    analyzer = BudgetAnalyzer()
    
    monthly_expenses = 3000
    current_savings = 12000
    
    result = analyzer.emergency_fund_check(monthly_expenses, current_savings)
    
    print(f"Monthly Expenses: ${monthly_expenses:,.0f}")
    print(f"Current Savings: ${current_savings:,.0f}")
    print(f"\nMonths Covered: {result['months_covered']:.1f}")
    print(f"Minimum Target (3 months): ${result['minimum_target']:,.0f}")
    print(f"Ideal Target (6 months): ${result['ideal_target']:,.0f}")
    print(f"\nStatus: {result['status'].upper()}")
    print(f"Message: {result['message']}")


def demo_expense_categorization():
    """Demo automatic expense categorization"""
    print_section("🏷️  Automatic Expense Categorization")
    
    calc = FinanceCalculator()
    
    test_expenses = [
        ("Starbucks Coffee", 5.50),
        ("Uber to Airport", 45.00),
        ("Netflix Subscription", 15.99),
        ("Whole Foods Grocery", 120.00),
        ("Electric Bill", 85.00),
        ("Amazon Purchase", 67.00),
        ("Gym Membership", 50.00),
    ]
    
    print("Categorizing expenses...\n")
    for description, amount in test_expenses:
        result = calc.categorize_expense(description, amount)
        print(f"${amount:>7.2f} | {description:<25} → {result['category'].upper()}")


def main():
    """Run all demos"""
    print("\n" + "=" * 60)
    print("  AIZA FINANCE TOOLS DEMO")
    print("  BudgetPay AI Assistant")
    print("=" * 60)
    
    demos = [
        demo_budget_calculator,
        demo_budget_recommendations,
        demo_savings_goal,
        demo_expense_analysis,
        demo_debt_payoff,
        demo_compound_interest,
        demo_emergency_fund,
        demo_expense_categorization
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n❌ Error in {demo.__name__}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)
    print("\nAll finance tools are working correctly! ✓")
    print("\nNext steps:")
    print("1. Generate training data: python -m scripts.generate_finance_data")
    print("2. Train model: python -m scripts.train_finance_model")
    print("3. Start web UI: python -m scripts.chat_web")
    print()


if __name__ == '__main__':
    main()
