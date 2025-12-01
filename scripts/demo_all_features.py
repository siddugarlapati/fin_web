"""
Demo all BudgetPay AI features
"""
from budgetpayai.smart_parsing import SmartTransactionDetector
from budgetpayai.predictions import SpendingPredictor, BillReminder, SubscriptionDetector
from budgetpayai.reports import MonthlyReportGenerator, SpendingAlertSystem
from budgetpayai.investments import PortfolioAnalyzer, SIPRecommender, RiskProfiler, NetWorthTracker
from budgetpayai.security import FraudDetector
from budgetpayai.automation import TaxPlanner, SalaryDistributor

print("=" * 70)
print("💰 BUDGETPAY AI - COMPLETE FEATURE DEMO")
print("=" * 70)

# 1. SMS PARSING
print("\n1️⃣  SMS PARSING")
print("-" * 70)
detector = SmartTransactionDetector()
sms = "Your account debited Rs.2,500 at Swiggy on 01-12-2025. Avl bal: Rs.45,000"
result = detector.process_sms(sms)
print(f"SMS: {sms}")
print(f"Parsed: Amount=₹{result['amount']}, Merchant={result['merchant']}, Category={result['category']}")

# 2. SPENDING PREDICTION
print("\n2️⃣  SPENDING PREDICTION")
print("-" * 70)
predictor = SpendingPredictor()
historical = [
    {'month': 'Jan', 'total': 35000},
    {'month': 'Feb', 'total': 38000},
    {'month': 'Mar', 'total': 36000}
]
prediction = predictor.predict_monthly_spending(historical)
print(f"Historical Average: ₹{prediction['average_spending']}")
print(f"Next Month Prediction: ₹{prediction['predicted_amount']}")
print(f"Trend: {prediction['trend'].upper()}")

# 3. BILL REMINDERS
print("\n3️⃣  BILL REMINDERS")
print("-" * 70)
reminder = BillReminder()
transactions = [
    {'merchant': 'Netflix', 'amount': 199, 'timestamp': '2025-01-01T00:00:00'},
    {'merchant': 'Netflix', 'amount': 199, 'timestamp': '2025-02-01T00:00:00'},
    {'merchant': 'Netflix', 'amount': 199, 'timestamp': '2025-03-01T00:00:00'}
]
bills = reminder.detect_recurring_bills(transactions)
print(f"Detected {len(bills)} recurring bills:")
for bill in bills:
    print(f"  • {bill['merchant']}: ₹{bill['average_amount']} ({bill['frequency']})")

# 4. SUBSCRIPTION DETECTION
print("\n4️⃣  SUBSCRIPTION DETECTION")
print("-" * 70)
sub_detector = SubscriptionDetector()
subs = sub_detector.detect_subscriptions(transactions)
total = sub_detector.calculate_total_subscription_cost(subs)
print(f"Active Subscriptions: {total['count']}")
print(f"Monthly Cost: ₹{total['monthly_total']}")
print(f"Annual Cost: ₹{total['annual_total']}")

# 5. MONTHLY REPORT
print("\n5️⃣  MONTHLY REPORT")
print("-" * 70)
report_gen = MonthlyReportGenerator()
month_data = {
    'period': 'March 2025',
    'income': 50000,
    'total_expenses': 35000,
    'expenses_by_category': {
        'food': 8000,
        'transport': 5000,
        'utilities': 3000,
        'entertainment': 4000,
        'shopping': 15000
    },
    'transaction_count': 45
}
report = report_gen.generate_report(month_data)
print(f"Income: ₹{report['summary']['total_income']}")
print(f"Expenses: ₹{report['summary']['total_expenses']}")
print(f"Savings: ₹{report['summary']['net_savings']} ({report['summary']['savings_rate']})")
print(f"Status: {report['summary']['status'].upper()}")

# 6. SPENDING ALERTS
print("\n6️⃣  SPENDING ALERTS")
print("-" * 70)
alert_system = SpendingAlertSystem()
alerts = alert_system.check_budget_alerts('food', 8500, 8000)
if alerts:
    print(f"⚠️  {alerts[0]['message']}")

# 7. PORTFOLIO ANALYSIS
print("\n7️⃣  PORTFOLIO ANALYSIS")
print("-" * 70)
portfolio = PortfolioAnalyzer()
holdings = [
    {'name': 'HDFC Index Fund', 'type': 'equity', 'invested': 50000, 'current_value': 58000},
    {'name': 'Corporate Bond Fund', 'type': 'debt', 'invested': 30000, 'current_value': 31500}
]
analysis = portfolio.analyze_portfolio(holdings)
print(f"Total Value: ₹{analysis['total_value']}")
print(f"Total Returns: ₹{analysis['total_returns']} ({analysis['returns_percent']}%)")
print(f"Risk Level: {analysis['risk_score']['level'].upper()}")

# 8. SIP RECOMMENDATION
print("\n8️⃣  SIP RECOMMENDATION")
print("-" * 70)
sip = SIPRecommender()
profile = {
    'age': 30,
    'risk_appetite': 'moderate',
    'monthly_income': 50000,
    'sip_amount': 10000
}
recommendations = sip.recommend_sip(profile)
print(f"Recommended SIP Allocation:")
for rec in recommendations:
    print(f"  • {rec['category']}: ₹{rec['amount']} ({rec['allocation']})")

# 9. RISK PROFILING
print("\n9️⃣  RISK PROFILING")
print("-" * 70)
risk = RiskProfiler()
answers = {
    'age': 30,
    'income_stability': 'stable',
    'investment_experience': 'intermediate',
    'time_horizon': 10,
    'loss_tolerance': 'moderate'
}
profile = risk.assess_risk_profile(answers)
print(f"Risk Profile: {profile['risk_profile'].upper()}")
print(f"Risk Score: {profile['risk_score']}/100")
print(f"Recommended Equity: {profile['recommended_equity_allocation']}%")

# 10. NET WORTH TRACKING
print("\n🔟 NET WORTH TRACKING")
print("-" * 70)
networth = NetWorthTracker()
assets = {'savings': 100000, 'investments': 80000, 'property': 2000000}
liabilities = {'home_loan': 1500000, 'car_loan': 200000}
nw = networth.calculate_net_worth(assets, liabilities)
print(f"Total Assets: ₹{nw['total_assets']:,}")
print(f"Total Liabilities: ₹{nw['total_liabilities']:,}")
print(f"Net Worth: ₹{nw['net_worth']:,}")

# 11. FRAUD DETECTION
print("\n1️⃣1️⃣  FRAUD DETECTION")
print("-" * 70)
fraud = FraudDetector()
transaction = {
    'amount': 25000,
    'category': 'shopping',
    'merchant': 'Unknown Store',
    'timestamp': '2025-12-01T02:30:00'
}
user_profile = {'average_transaction': 2000}
fraud_check = fraud.detect_fraud(transaction, user_profile)
print(f"Fraud Score: {fraud_check['fraud_score']}/100")
print(f"Risk Level: {fraud_check['risk_level'].upper()}")
print(f"Action: {fraud_check['recommended_action'].upper()}")

# 12. TAX PLANNING
print("\n1️⃣2️⃣  TAX PLANNING")
print("-" * 70)
tax = TaxPlanner()
tax_calc = tax.calculate_tax(800000, 'new')
print(f"Annual Income: ₹{tax_calc['annual_income']:,}")
print(f"Total Tax: ₹{tax_calc['total_tax']:,}")
print(f"Effective Rate: {tax_calc['effective_tax_rate']}%")
print(f"Monthly Tax: ₹{tax_calc['monthly_tax']:,}")

# 13. SALARY DISTRIBUTION
print("\n1️⃣3️⃣  SALARY DISTRIBUTION")
print("-" * 70)
distributor = SalaryDistributor()
suggested = distributor.suggest_distribution(50000)
print(f"Suggested Distribution for ₹50,000:")
for envelope, percentage in suggested.items():
    amount = 50000 * (percentage / 100)
    print(f"  • {envelope.title()}: ₹{amount:,.0f} ({percentage}%)")

print("\n" + "=" * 70)
print("✅ ALL FEATURES DEMONSTRATED SUCCESSFULLY!")
print("=" * 70)
print("\n🚀 BudgetPay AI is ready for production!")
print("\nTo start the complete API server:")
print("  python -m scripts.complete_api")
print("\nThen visit: http://localhost:8000")
print()
