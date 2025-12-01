"""
Complete API with all BudgetPay AI features
Run this for full functionality
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
import uvicorn

# Import all modules
from budgetpayai.smart_parsing import SmartTransactionDetector
from budgetpayai.predictions import SpendingPredictor, BillReminder, SubscriptionDetector, AdaptiveBudgetManager
from budgetpayai.reports import MonthlyReportGenerator, SpendingAlertSystem, generate_weekly_digest
from budgetpayai.investments import PortfolioAnalyzer, SIPRecommender, RiskProfiler, NetWorthTracker
from budgetpayai.security import FraudDetector
from budgetpayai.automation import AutoInvestmentManager, AutoBillPayManager, SalaryDistributor, TaxPlanner
from budgetpayai.finance_tools import FinanceCalculator, BudgetAnalyzer
from budgetpayai.realtime_data import RealTimeDataHub

app = FastAPI(title="BudgetPay AI - Complete API")

# Initialize all systems
transaction_detector = SmartTransactionDetector()
spending_predictor = SpendingPredictor()
bill_reminder = BillReminder()
subscription_detector = SubscriptionDetector()
budget_manager = AdaptiveBudgetManager()
report_generator = MonthlyReportGenerator()
alert_system = SpendingAlertSystem()
portfolio_analyzer = PortfolioAnalyzer()
sip_recommender = SIPRecommender()
risk_profiler = RiskProfiler()
networth_tracker = NetWorthTracker()
fraud_detector = FraudDetector()
auto_invest_manager = AutoInvestmentManager()
auto_bill_manager = AutoBillPayManager()
salary_distributor = SalaryDistributor()
tax_planner = TaxPlanner()
calc = FinanceCalculator()
analyzer = BudgetAnalyzer()
realtime_hub = RealTimeDataHub()


@app.get("/")
async def home():
    return HTMLResponse("""
    <html>
        <head><title>BudgetPay AI - Complete API</title></head>
        <body style="font-family: Arial; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div style="background: white; padding: 40px; border-radius: 20px; max-width: 800px; margin: 0 auto;">
                <h1 style="color: #667eea;">💰 BudgetPay AI</h1>
                <h2>Complete Finance Platform API</h2>
                <p>Access all 70+ features via REST API</p>
                <h3>📚 Documentation:</h3>
                <ul>
                    <li><a href="/docs">Interactive API Docs (Swagger)</a></li>
                    <li><a href="/redoc">ReDoc Documentation</a></li>
                </ul>
                <h3>🚀 Feature Categories:</h3>
                <ul>
                    <li>Smart Parsing (SMS/Email/OCR)</li>
                    <li>Spending Predictions</li>
                    <li>Bill Reminders & Subscriptions</li>
                    <li>Monthly Reports & Alerts</li>
                    <li>Investment Analysis & SIP</li>
                    <li>Portfolio & Risk Profiling</li>
                    <li>Net Worth Tracking</li>
                    <li>Fraud Detection</li>
                    <li>Auto-Investment & Bill Pay</li>
                    <li>Salary Distribution</li>
                    <li>Tax Planning</li>
                    <li>Real-Time Market Data</li>
                </ul>
            </div>
        </body>
    </html>
    """)


# SMART PARSING
@app.post("/api/parse/sms")
async def parse_sms(request: Request):
    data = await request.json()
    result = transaction_detector.process_sms(data.get('message', ''))
    return JSONResponse(result if result else {'error': 'Could not parse'})

@app.post("/api/parse/receipt")
async def parse_receipt(request: Request):
    data = await request.json()
    return JSONResponse(transaction_detector.process_receipt(data.get('ocr_text', '')))

# PREDICTIONS
@app.post("/api/predict/monthly")
async def predict_monthly(request: Request):
    data = await request.json()
    return JSONResponse(spending_predictor.predict_monthly_spending(data.get('historical', [])))

@app.post("/api/predict/balance")
async def predict_balance(request: Request):
    data = await request.json()
    return JSONResponse(spending_predictor.predict_end_of_month_balance(
        data.get('balance', 0), data.get('days', 15), data.get('daily_avg', 200)
    ))

# BILLS & SUBSCRIPTIONS
@app.post("/api/bills/detect")
async def detect_bills(request: Request):
    data = await request.json()
    return JSONResponse({'bills': bill_reminder.detect_recurring_bills(data.get('transactions', []))})

@app.post("/api/subscriptions/detect")
async def detect_subs(request: Request):
    data = await request.json()
    return JSONResponse({'subscriptions': subscription_detector.detect_subscriptions(data.get('transactions', []))})

# REPORTS & ALERTS
@app.post("/api/reports/monthly")
async def monthly_report(request: Request):
    data = await request.json()
    return JSONResponse(report_generator.generate_report(data.get('month_data', {})))

@app.post("/api/alerts/all")
async def all_alerts(request: Request):
    data = await request.json()
    return JSONResponse({'alerts': alert_system.get_all_alerts(
        data.get('spending', {}), data.get('budgets', {}), data.get('profile', {})
    )})

# INVESTMENTS
@app.post("/api/portfolio/analyze")
async def analyze_portfolio(request: Request):
    data = await request.json()
    return JSONResponse(portfolio_analyzer.analyze_portfolio(data.get('holdings', [])))

@app.post("/api/sip/recommend")
async def recommend_sip(request: Request):
    data = await request.json()
    return JSONResponse({'recommendations': sip_recommender.recommend_sip(data.get('profile', {}))})

@app.post("/api/sip/returns")
async def sip_returns(request: Request):
    data = await request.json()
    return JSONResponse(sip_recommender.calculate_sip_returns(
        data.get('amount', 5000), data.get('years', 10), data.get('return', 12)
    ))

@app.post("/api/risk/assess")
async def assess_risk(request: Request):
    data = await request.json()
    return JSONResponse(risk_profiler.assess_risk_profile(data.get('answers', {})))

@app.post("/api/networth/calculate")
async def calc_networth(request: Request):
    data = await request.json()
    return JSONResponse(networth_tracker.calculate_net_worth(
        data.get('assets', {}), data.get('liabilities', {})
    ))

# SECURITY
@app.post("/api/fraud/detect")
async def detect_fraud(request: Request):
    data = await request.json()
    return JSONResponse(fraud_detector.detect_fraud(
        data.get('transaction', {}), data.get('profile', {})
    ))

# AUTOMATION
@app.post("/api/auto/invest")
async def auto_invest(request: Request):
    data = await request.json()
    rule_id = auto_invest_manager.create_auto_investment_rule(
        data.get('user_id', 'user1'), data.get('rule', {})
    )
    return JSONResponse({'rule_id': rule_id})

@app.post("/api/auto/bill")
async def auto_bill(request: Request):
    data = await request.json()
    bill_id = auto_bill_manager.setup_auto_pay(
        data.get('user_id', 'user1'), data.get('bill', {})
    )
    return JSONResponse({'bill_id': bill_id})

@app.post("/api/salary/distribute")
async def distribute(request: Request):
    data = await request.json()
    return JSONResponse(salary_distributor.distribute_salary(
        data.get('user_id', 'user1'), data.get('amount', 0)
    ))

# TAX
@app.post("/api/tax/calculate")
async def calc_tax(request: Request):
    data = await request.json()
    return JSONResponse(tax_planner.calculate_tax(
        data.get('income', 0), data.get('regime', 'new')
    ))

@app.post("/api/tax/savings")
async def tax_savings(request: Request):
    data = await request.json()
    return JSONResponse({'suggestions': tax_planner.suggest_tax_savings(
        data.get('income', 0), data.get('investments', {})
    )})

# FINANCE TOOLS
@app.post("/api/budget/calculate")
async def calc_budget(request: Request):
    data = await request.json()
    return JSONResponse(calc.calculate_budget(
        data.get('income', 0), data.get('expenses', {})
    ))

# REAL-TIME DATA
@app.get("/api/stock/{symbol}")
async def stock_price(symbol: str):
    return JSONResponse(realtime_hub.stocks.get_stock_price(symbol))

@app.get("/api/market/overview")
async def market_overview():
    return JSONResponse(realtime_hub.get_market_overview())


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 BudgetPay AI - Complete API Server")
    print("=" * 60)
    print("\n✅ All 70+ features loaded!")
    print("\n📍 Server starting at: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("\n" + "=" * 60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
