"""
BudgetPay AI - India's Best Finance AI App
Streamlit Application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Import all BudgetPay modules
from budgetpayai.smart_parsing import SmartTransactionDetector
from budgetpayai.predictions import SpendingPredictor, BillReminder, SubscriptionDetector, AdaptiveBudgetManager
from budgetpayai.reports import MonthlyReportGenerator, SpendingAlertSystem
from budgetpayai.investments import PortfolioAnalyzer, SIPRecommender, RiskProfiler, NetWorthTracker
from budgetpayai.security import FraudDetector
from budgetpayai.automation import TaxPlanner, SalaryDistributor
from budgetpayai.finance_tools import FinanceCalculator, BudgetAnalyzer

# Page config
st.set_page_config(
    page_title="BudgetPay AI - India's Best Finance App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'budget' not in st.session_state:
    st.session_state.budget = {}
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []

# Initialize systems
@st.cache_resource
def init_systems():
    return {
        'detector': SmartTransactionDetector(),
        'predictor': SpendingPredictor(),
        'bill_reminder': BillReminder(),
        'sub_detector': SubscriptionDetector(),
        'budget_manager': AdaptiveBudgetManager(),
        'report_gen': MonthlyReportGenerator(),
        'alert_system': SpendingAlertSystem(),
        'portfolio_analyzer': PortfolioAnalyzer(),
        'sip_recommender': SIPRecommender(),
        'risk_profiler': RiskProfiler(),
        'networth_tracker': NetWorthTracker(),
        'fraud_detector': FraudDetector(),
        'tax_planner': TaxPlanner(),
        'salary_dist': SalaryDistributor(),
        'calc': FinanceCalculator(),
        'analyzer': BudgetAnalyzer()
    }

systems = init_systems()

# Sidebar
with st.sidebar:
    st.markdown('<h1 style="color: #667eea;">💰 BudgetPay AI</h1>', unsafe_allow_html=True)
    st.markdown("### India's Best Finance AI")
    
    page = st.selectbox(
        "Navigate",
        ["🏠 Dashboard", "💳 Transactions", "📊 Budget Manager", "📈 Investments", 
         "🔮 Predictions", "📱 Subscriptions", "📄 Reports", "🛡️ Security", 
         "🤖 AI Assistant", "💼 Tax Planning"]
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    total_txns = len(st.session_state.transactions)
    st.metric("Total Transactions", total_txns)
    
    if st.session_state.transactions:
        total_spent = sum(t.get('amount', 0) for t in st.session_state.transactions if t.get('type') == 'debit')
        st.metric("Total Spent", f"₹{total_spent:,.0f}")

# Main content
if page == "🏠 Dashboard":
    st.markdown('<div class="main-header">🏠 Financial Dashboard</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>₹50,000</h3><p>Monthly Income</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>₹35,000</h3><p>Total Expenses</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>₹15,000</h3><p>Savings</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>30%</h3><p>Savings Rate</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Spending by Category")
        categories = {'Food': 8000, 'Transport': 5000, 'Shopping': 12000, 'Bills': 10000}
        fig = px.pie(values=list(categories.values()), names=list(categories.keys()), 
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📈 Monthly Trend")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        spending = [32000, 35000, 33000, 38000, 36000, 35000]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=spending, mode='lines+markers', 
                                 line=dict(color='#667eea', width=3)))
        fig.update_layout(title="Spending Trend", xaxis_title="Month", yaxis_title="Amount (₹)")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("🚨 Recent Alerts")
    st.warning("⚠️ Food budget 85% utilized - ₹6,800 of ₹8,000")
    st.info("💡 You're on track to save ₹15,000 this month!")
    st.success("✅ All bills paid on time this month")

elif page == "💳 Transactions":
    st.title("💳 Transaction Manager")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Transaction", "📋 View All", "📤 Import"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)
            merchant = st.text_input("Merchant/Description")
            txn_type = st.selectbox("Type", ["Debit", "Credit"])
        
        with col2:
            date = st.date_input("Date")
            category = st.selectbox("Category", 
                ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Health", "Other"])
            
        if st.button("Add Transaction"):
            txn = {
                'date': date.isoformat(),
                'amount': amount,
                'merchant': merchant,
                'type': txn_type.lower(),
                'category': category.lower(),
                'timestamp': datetime.now().isoformat()
            }
            st.session_state.transactions.append(txn)
            st.success(f"✅ Added: ₹{amount} at {merchant}")
    
    with tab2:
        if st.session_state.transactions:
            df = pd.DataFrame(st.session_state.transactions)
            st.dataframe(df, use_container_width=True)
            
            # Download
            csv = df.to_csv(index=False)
            st.download_button("📥 Download CSV", csv, "transactions.csv", "text/csv")
        else:
            st.info("No transactions yet. Add some above!")
    
    with tab3:
        st.subheader("📤 Import from SMS")
        sms_text = st.text_area("Paste bank SMS here")
        if st.button("Parse SMS"):
            result = systems['detector'].process_sms(sms_text)
            if result:
                st.success("✅ Parsed successfully!")
                st.json(result)
                if st.button("Add to Transactions"):
                    st.session_state.transactions.append(result)
            else:
                st.error("❌ Could not parse SMS")

elif page == "📊 Budget Manager":
    st.title("📊 Budget Manager")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Set Monthly Budget")
        income = st.number_input("Monthly Income (₹)", value=50000, step=1000)
        
        st.markdown("### Category Budgets")
        food_budget = st.slider("Food", 0, 20000, 8000, 500)
        transport_budget = st.slider("Transport", 0, 10000, 5000, 500)
        shopping_budget = st.slider("Shopping", 0, 20000, 10000, 500)
        bills_budget = st.slider("Bills", 0, 15000, 8000, 500)
        
        if st.button("Save Budget"):
            st.session_state.budget = {
                'income': income,
                'food': food_budget,
                'transport': transport_budget,
                'shopping': shopping_budget,
                'bills': bills_budget
            }
            st.success("✅ Budget saved!")
    
    with col2:
        st.subheader("Budget Analysis")
        if st.session_state.budget:
            total_budget = sum([v for k, v in st.session_state.budget.items() if k != 'income'])
            savings_target = st.session_state.budget['income'] - total_budget
            
            st.metric("Total Budget", f"₹{total_budget:,.0f}")
            st.metric("Target Savings", f"₹{savings_target:,.0f}")
            st.metric("Savings Rate", f"{(savings_target/st.session_state.budget['income']*100):.1f}%")
            
            # Recommendations
            recommendations = systems['analyzer'].get_recommendations(
                st.session_state.budget['income'],
                {k: v for k, v in st.session_state.budget.items() if k != 'income'}
            )
            
            st.markdown("### 💡 Recommendations")
            for rec in recommendations:
                st.info(rec)
        else:
            st.info("Set your budget to see analysis")

elif page == "📈 Investments":
    st.title("📈 Investment Portfolio")
    
    tab1, tab2, tab3 = st.tabs(["Portfolio", "SIP Calculator", "Risk Profile"])
    
    with tab1:
        st.subheader("Your Portfolio")
        
        col1, col2 = st.columns(2)
        with col1:
            holding_name = st.text_input("Investment Name")
            holding_type = st.selectbox("Type", ["Equity", "Debt", "Gold", "Real Estate"])
            invested = st.number_input("Invested Amount", min_value=0, step=1000)
            current = st.number_input("Current Value", min_value=0, step=1000)
            
            if st.button("Add to Portfolio"):
                holding = {
                    'name': holding_name,
                    'type': holding_type.lower(),
                    'invested': invested,
                    'current_value': current
                }
                st.session_state.portfolio.append(holding)
                st.success("✅ Added to portfolio")
        
        with col2:
            if st.session_state.portfolio:
                analysis = systems['portfolio_analyzer'].analyze_portfolio(st.session_state.portfolio)
                
                st.metric("Total Value", f"₹{analysis['total_value']:,.0f}")
                st.metric("Total Returns", f"₹{analysis['total_returns']:,.0f}")
                st.metric("Returns %", f"{analysis['returns_percent']:.2f}%")
                
                st.markdown("### Asset Allocation")
                fig = px.pie(values=list(analysis['allocation'].values()), 
                           names=list(analysis['allocation'].keys()))
                st.plotly_chart(fig)
    
    with tab2:
        st.subheader("SIP Calculator")
        monthly_sip = st.number_input("Monthly SIP Amount (₹)", value=5000, step=500)
        years = st.slider("Investment Period (Years)", 1, 30, 10)
        expected_return = st.slider("Expected Return (%)", 8, 20, 12)
        
        if st.button("Calculate SIP Returns"):
            result = systems['sip_recommender'].calculate_sip_returns(monthly_sip, years, expected_return)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Invested", f"₹{result['total_invested']:,.0f}")
            col2.metric("Future Value", f"₹{result['future_value']:,.0f}")
            col3.metric("Returns", f"₹{result['total_returns']:,.0f}")
    
    with tab3:
        st.subheader("Risk Profile Assessment")
        age = st.number_input("Your Age", 18, 100, 30)
        income_stability = st.selectbox("Income Stability", ["Very Stable", "Stable", "Unstable"])
        experience = st.selectbox("Investment Experience", ["Beginner", "Intermediate", "Expert"])
        time_horizon = st.slider("Investment Horizon (Years)", 1, 30, 10)
        loss_tolerance = st.selectbox("Loss Tolerance", ["Low", "Moderate", "High"])
        
        if st.button("Assess Risk Profile"):
            answers = {
                'age': age,
                'income_stability': income_stability.lower().replace(' ', '_'),
                'investment_experience': experience.lower(),
                'time_horizon': time_horizon,
                'loss_tolerance': loss_tolerance.lower()
            }
            profile = systems['risk_profiler'].assess_risk_profile(answers)
            
            st.success(f"Your Risk Profile: **{profile['risk_profile'].upper()}**")
            st.info(profile['description'])
            st.metric("Risk Score", f"{profile['risk_score']}/100")
            st.metric("Recommended Equity", f"{profile['recommended_equity_allocation']}%")

elif page == "🔮 Predictions":
    st.title("🔮 AI Predictions")
    
    st.subheader("📊 Spending Predictions")
    
    if len(st.session_state.transactions) >= 3:
        # Group by month
        df = pd.DataFrame(st.session_state.transactions)
        df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
        monthly = df.groupby('month')['amount'].sum().reset_index()
        
        historical = [{'month': str(m), 'total': float(t)} for m, t in zip(monthly['month'], monthly['amount'])]
        
        prediction = systems['predictor'].predict_monthly_spending(historical)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Predicted Next Month", f"₹{prediction['predicted_amount']:,.0f}")
        col2.metric("Confidence", prediction['confidence'].upper())
        col3.metric("Trend", prediction['trend'].upper())
        
        st.markdown("### 📈 Spending Forecast")
        months = [h['month'] for h in historical] + ['Next Month']
        amounts = [h['total'] for h in historical] + [prediction['predicted_amount']]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months[:-1], y=amounts[:-1], mode='lines+markers', name='Actual'))
        fig.add_trace(go.Scatter(x=[months[-2], months[-1]], y=[amounts[-2], amounts[-1]], 
                                mode='lines+markers', name='Predicted', line=dict(dash='dash')))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add at least 3 months of transactions to see predictions")

elif page == "📱 Subscriptions":
    st.title("📱 Subscription Manager")
    
    if st.session_state.transactions:
        subs = systems['sub_detector'].detect_subscriptions(st.session_state.transactions)
        
        if subs:
            st.subheader(f"Found {len(subs)} Active Subscriptions")
            
            for sub in subs:
                with st.expander(f"{sub['name']} - ₹{sub['amount']}/{sub['frequency']}"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Amount", f"₹{sub['amount']}")
                    col2.metric("Frequency", sub['frequency'])
                    col3.metric("Annual Cost", f"₹{sub['annual_cost']}")
            
            total = systems['sub_detector'].calculate_total_subscription_cost(subs)
            st.markdown("---")
            st.metric("Total Monthly Cost", f"₹{total['monthly_total']}")
            st.metric("Total Annual Cost", f"₹{total['annual_total']}")
        else:
            st.info("No subscriptions detected yet")
    else:
        st.info("Add transactions to detect subscriptions")

elif page == "📄 Reports":
    st.title("📄 Monthly Reports")
    
    if st.button("Generate Monthly Report"):
        month_data = {
            'period': datetime.now().strftime('%B %Y'),
            'income': st.session_state.budget.get('income', 50000),
            'total_expenses': 35000,
            'expenses_by_category': {
                'food': 8000,
                'transport': 5000,
                'shopping': 12000,
                'bills': 10000
            },
            'transaction_count': len(st.session_state.transactions)
        }
        
        report = systems['report_gen'].generate_report(month_data)
        
        st.success("✅ Report Generated!")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Income", f"₹{report['summary']['total_income']:,.0f}")
        col2.metric("Expenses", f"₹{report['summary']['total_expenses']:,.0f}")
        col3.metric("Savings", f"₹{report['summary']['net_savings']:,.0f}")
        
        st.markdown("### 💡 Key Highlights")
        for highlight in report['highlights']:
            st.info(highlight)
        
        st.markdown("### 🎯 Recommendations")
        for rec in report['recommendations']:
            st.warning(rec)
        
        # Download report
        text_report = systems['report_gen'].export_report_text(report)
        st.download_button("📥 Download Report", text_report, "monthly_report.txt")

elif page == "🛡️ Security":
    st.title("🛡️ Security & Fraud Detection")
    
    st.subheader("🔍 Check Transaction for Fraud")
    
    col1, col2 = st.columns(2)
    with col1:
        check_amount = st.number_input("Transaction Amount", min_value=0, step=100)
        check_merchant = st.text_input("Merchant Name")
        check_category = st.selectbox("Category", ["food", "transport", "shopping", "gambling", "crypto"])
    
    with col2:
        if st.button("Check for Fraud"):
            transaction = {
                'amount': check_amount,
                'merchant': check_merchant,
                'category': check_category,
                'timestamp': datetime.now().isoformat()
            }
            
            user_profile = {'average_transaction': 2000}
            
            result = systems['fraud_detector'].detect_fraud(transaction, user_profile)
            
            if result['risk_level'] == 'high':
                st.error(f"🚨 HIGH RISK - Fraud Score: {result['fraud_score']}/100")
            elif result['risk_level'] == 'medium':
                st.warning(f"⚠️ MEDIUM RISK - Fraud Score: {result['fraud_score']}/100")
            else:
                st.success(f"✅ LOW RISK - Fraud Score: {result['fraud_score']}/100")
            
            if result['alerts']:
                st.markdown("### Alerts:")
                for alert in result['alerts']:
                    st.warning(alert)

elif page == "🤖 AI Assistant":
    st.title("🤖 AI Finance Assistant")
    
    st.markdown("### Ask me anything about finance!")
    
    question = st.text_input("Your Question")
    
    if st.button("Ask AI"):
        # Simple rule-based responses
        responses = {
            'budget': "A good budget follows the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings.",
            'save': "Start by automating your savings. Aim to save at least 20% of your income.",
            'invest': "Before investing, build an emergency fund and pay off high-interest debt. Then start with index funds.",
            'debt': "Pay off high-interest debt first using the avalanche method.",
            'tax': "Maximize 80C deductions (₹1.5L) through ELSS, PPF, or EPF to save taxes."
        }
        
        response = "I can help you with budgeting, saving, investing, debt management, and tax planning!"
        for keyword, answer in responses.items():
            if keyword in question.lower():
                response = answer
                break
        
        st.success(response)

elif page == "💼 Tax Planning":
    st.title("💼 Tax Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Calculate Your Tax")
        annual_income = st.number_input("Annual Income (₹)", value=800000, step=10000)
        regime = st.selectbox("Tax Regime", ["New", "Old"])
        
        if st.button("Calculate Tax"):
            tax_result = systems['tax_planner'].calculate_tax(annual_income, regime.lower())
            
            st.metric("Total Tax", f"₹{tax_result['total_tax']:,.0f}")
            st.metric("Effective Rate", f"{tax_result['effective_tax_rate']}%")
            st.metric("Monthly Tax", f"₹{tax_result['monthly_tax']:,.0f}")
    
    with col2:
        st.subheader("Tax Saving Suggestions")
        current_80c = st.number_input("Current 80C Investments", value=0, step=10000)
        
        if st.button("Get Suggestions"):
            suggestions = systems['tax_planner'].suggest_tax_savings(
                annual_income,
                {'80c': current_80c}
            )
            
            for sug in suggestions:
                st.info(f"**{sug['section']}**: Save ₹{sug['tax_saved']:,.0f} by investing ₹{sug['remaining_limit']:,.0f}")
                st.write(f"Options: {', '.join(sug['options'])}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💰 BudgetPay AI - India's Best Finance App</p>
    <p>Powered by Advanced AI & Machine Learning</p>
</div>
""", unsafe_allow_html=True)
