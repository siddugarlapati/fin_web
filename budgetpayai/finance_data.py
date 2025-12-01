"""
Generate synthetic finance training data for Aiza
"""
import json
import random
from typing import List, Dict


class FinanceDataGenerator:
    """Generate synthetic finance conversations and data"""
    
    def __init__(self):
        self.budget_questions = [
            "How should I budget my income?",
            "What's the 50/30/20 rule?",
            "How much should I save each month?",
            "Help me create a budget",
            "I need help managing my money"
        ]
        
        self.expense_questions = [
            "How can I track my expenses?",
            "Where is my money going?",
            "How do I categorize expenses?",
            "I'm spending too much, what should I do?",
            "Help me reduce my spending"
        ]
        
        self.savings_questions = [
            "How do I start saving money?",
            "What's a good savings rate?",
            "How much should I have in emergency fund?",
            "Tips for saving more money?",
            "How to build wealth?"
        ]
        
        self.investment_questions = [
            "Should I invest or save?",
            "What is compound interest?",
            "How do I start investing?",
            "What's a good return on investment?",
            "Explain stocks vs bonds"
        ]
        
        self.debt_questions = [
            "How do I pay off debt faster?",
            "Should I pay off debt or save?",
            "What's the snowball method?",
            "Help me with credit card debt",
            "How long to pay off my loan?"
        ]
    
    def generate_budget_conversation(self) -> Dict[str, str]:
        """Generate budget-related Q&A"""
        responses = [
            "A good budget follows the 50/30/20 rule: 50% for needs (housing, food, utilities), 30% for wants (entertainment, dining out), and 20% for savings and debt repayment. Start by tracking all your expenses for a month to see where your money goes.",
            "To create a budget: 1) Calculate your monthly income, 2) List all expenses, 3) Categorize as needs vs wants, 4) Ensure you're saving at least 20%, 5) Adjust spending if needed. Use apps or spreadsheets to track everything.",
            "The key to budgeting is knowing your income and expenses. Allocate money to essentials first, then savings, then discretionary spending. Review and adjust monthly. Automate savings so you pay yourself first!",
        ]
        
        return {
            "prompt": random.choice(self.budget_questions),
            "response": random.choice(responses)
        }
    
    def generate_expense_conversation(self) -> Dict[str, str]:
        """Generate expense tracking Q&A"""
        responses = [
            "Track expenses by category: Housing, Food, Transport, Utilities, Entertainment, Shopping, Health, and Other. Use apps like Mint or YNAB, or a simple spreadsheet. Review weekly to spot overspending patterns.",
            "Common expense categories: Fixed (rent, insurance, subscriptions) and Variable (groceries, gas, entertainment). Track everything for 30 days to understand your spending habits. Small purchases add up!",
            "To reduce spending: 1) Cut unused subscriptions, 2) Cook at home more, 3) Use public transport, 4) Shop with a list, 5) Wait 24hrs before big purchases. Focus on wants vs needs.",
        ]
        
        return {
            "prompt": random.choice(self.expense_questions),
            "response": random.choice(responses)
        }
    
    def generate_savings_conversation(self) -> Dict[str, str]:
        """Generate savings-related Q&A"""
        responses = [
            "Start saving by: 1) Pay yourself first - automate 20% of income to savings, 2) Build emergency fund (3-6 months expenses), 3) Use high-yield savings account, 4) Set specific goals, 5) Track progress monthly.",
            "Emergency fund should cover 3-6 months of expenses. Start with $1000, then build to one month, then three months. Keep it in a separate savings account. This protects you from unexpected costs.",
            "Savings tips: Automate transfers on payday, use the 24-hour rule for purchases, pack lunch instead of eating out, cancel unused subscriptions, negotiate bills, use cashback apps. Small changes add up!",
        ]
        
        return {
            "prompt": random.choice(self.savings_questions),
            "response": random.choice(responses)
        }
    
    def generate_investment_conversation(self) -> Dict[str, str]:
        """Generate investment Q&A"""
        responses = [
            "Compound interest is earning interest on your interest. If you invest $1000 at 7% annually, after 10 years you'll have $1967 - that's $967 in gains! Start early, invest regularly, and let time work for you.",
            "Before investing: 1) Have emergency fund, 2) Pay off high-interest debt, 3) Understand your risk tolerance, 4) Start with index funds, 5) Think long-term (10+ years). Don't invest money you need soon.",
            "Investment basics: Stocks = ownership in companies (higher risk/reward), Bonds = loans to companies/government (lower risk/reward), Index funds = diversified basket of stocks (good for beginners). Diversify!",
        ]
        
        return {
            "prompt": random.choice(self.investment_questions),
            "response": random.choice(responses)
        }
    
    def generate_debt_conversation(self) -> Dict[str, str]:
        """Generate debt payoff Q&A"""
        responses = [
            "Debt payoff strategies: Snowball method (pay smallest debt first for motivation) or Avalanche method (pay highest interest first to save money). Both work - choose what motivates you. Pay more than minimum!",
            "To pay off debt faster: 1) Pay more than minimum, 2) Use windfalls (tax refunds, bonuses), 3) Cut expenses temporarily, 4) Consider side income, 5) Negotiate lower interest rates. Stay motivated!",
            "Priority: Pay off high-interest debt (credit cards >15%) before investing. Keep making minimum payments on all debts. Once high-interest debt is gone, balance between investing and remaining debt payoff.",
        ]
        
        return {
            "prompt": random.choice(self.debt_questions),
            "response": random.choice(responses)
        }
    
    def generate_training_dataset(self, num_samples: int = 1000) -> List[Dict[str, str]]:
        """Generate complete training dataset"""
        dataset = []
        
        generators = [
            self.generate_budget_conversation,
            self.generate_expense_conversation,
            self.generate_savings_conversation,
            self.generate_investment_conversation,
            self.generate_debt_conversation
        ]
        
        for _ in range(num_samples):
            generator = random.choice(generators)
            dataset.append(generator())
        
        return dataset
    
    def save_dataset(self, filename: str = "finance_training_data.jsonl", num_samples: int = 1000):
        """Save training dataset to file"""
        dataset = self.generate_training_dataset(num_samples)
        
        with open(filename, 'w') as f:
            for item in dataset:
                f.write(json.dumps(item) + '\n')
        
        print(f"Generated {num_samples} training samples saved to {filename}")
        return filename


# Additional finance knowledge base
FINANCE_KNOWLEDGE = {
    "budgeting": {
        "50_30_20_rule": "50% needs, 30% wants, 20% savings",
        "zero_based": "Every dollar has a purpose",
        "envelope_method": "Cash in envelopes for each category"
    },
    "savings": {
        "emergency_fund": "3-6 months of expenses",
        "high_yield_savings": "Online banks offer better rates",
        "automation": "Set up automatic transfers"
    },
    "investing": {
        "compound_interest": "Interest on interest over time",
        "diversification": "Don't put all eggs in one basket",
        "index_funds": "Low-cost, diversified investment",
        "dollar_cost_averaging": "Invest regularly regardless of price"
    },
    "debt": {
        "snowball": "Pay smallest debt first",
        "avalanche": "Pay highest interest first",
        "consolidation": "Combine debts for lower rate"
    }
}
