"""
Web interface for Aiza with finance tools
"""
import torch
import json
import re
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from aiza.model import AizaModel
from aiza.tokenizer import AizaTokenizer
from aiza.finance_tools import FinanceCalculator, BudgetAnalyzer
import uvicorn


app = FastAPI()

# Load model and tokenizer
device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = AizaTokenizer()
try:
    tokenizer.load('tokenizer.json')
    model = AizaModel(vocab_size=tokenizer.vocab_size)
    checkpoint = torch.load('aiza_model.pt', map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()
    MODEL_LOADED = True
except:
    MODEL_LOADED = False
    print("⚠️  Model not loaded - using finance tools only mode")

# Initialize finance tools
calc = FinanceCalculator()
analyzer = BudgetAnalyzer()


@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Aiza - BudgetPay Finance Assistant</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .container {
                width: 90%;
                max-width: 800px;
                height: 90vh;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                display: flex;
                flex-direction: column;
            }
            .header {
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 20px 20px 0 0;
                text-align: center;
            }
            .header h1 { font-size: 28px; margin-bottom: 5px; }
            .header p { font-size: 14px; opacity: 0.9; }
            .chat-area {
                flex: 1;
                padding: 20px;
                overflow-y: auto;
                background: #f7f7f7;
            }
            .message {
                margin-bottom: 15px;
                padding: 12px 16px;
                border-radius: 12px;
                max-width: 80%;
                animation: fadeIn 0.3s;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .user-message {
                background: #667eea;
                color: white;
                margin-left: auto;
                text-align: right;
            }
            .ai-message {
                background: white;
                color: #333;
                border: 1px solid #e0e0e0;
            }
            .input-area {
                padding: 20px;
                background: white;
                border-radius: 0 0 20px 20px;
                border-top: 1px solid #e0e0e0;
            }
            .input-group {
                display: flex;
                gap: 10px;
            }
            input {
                flex: 1;
                padding: 12px 16px;
                border: 2px solid #e0e0e0;
                border-radius: 25px;
                font-size: 14px;
                outline: none;
                transition: border-color 0.3s;
            }
            input:focus { border-color: #667eea; }
            button {
                padding: 12px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                transition: transform 0.2s;
            }
            button:hover { transform: scale(1.05); }
            button:active { transform: scale(0.95); }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>💰 Aiza</h1>
                <p>Your BudgetPay Finance Assistant</p>
            </div>
            <div class="chat-area" id="chatArea">
                <div class="message ai-message">
                    Hello! I'm Aiza, your finance assistant. How can I help you with your budget today?
                </div>
            </div>
            <div class="input-area">
                <div class="input-group">
                    <input type="text" id="userInput" placeholder="Ask me about budgeting, saving, or investing..." />
                    <button onclick="sendMessage()">Send</button>
                </div>
            </div>
        </div>
        
        <script>
            async function sendMessage() {
                const input = document.getElementById('userInput');
                const message = input.value.trim();
                if (!message) return;
                
                const chatArea = document.getElementById('chatArea');
                chatArea.innerHTML += `<div class="message user-message">${message}</div>`;
                input.value = '';
                chatArea.scrollTop = chatArea.scrollHeight;
                
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: message })
                });
                
                const data = await response.json();
                chatArea.innerHTML += `<div class="message ai-message">${data.response}</div>`;
                chatArea.scrollTop = chatArea.scrollHeight;
            }
            
            document.getElementById('userInput').addEventListener('keypress', (e) => {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    """


@app.post("/generate")
async def generate(request: Request):
    data = await request.json()
    prompt = data.get('prompt', '').lower()
    
    # Check if it's a finance calculation request
    if 'calculate' in prompt or 'budget' in prompt or 'expense' in prompt:
        # Try to extract numbers and calculate
        numbers = re.findall(r'\d+(?:\.\d+)?', prompt)
        if len(numbers) >= 2:
            try:
                income = float(numbers[0])
                expenses = {"total": sum(float(n) for n in numbers[1:])}
                result = calc.calculate_budget(income, expenses)
                response = f"Based on income ${income:.0f} and expenses ${result['total_expenses']:.0f}, you have ${result['savings']:.0f} in savings ({result['savings_rate']} savings rate). Status: {result['status']}."
                return {"response": response, "calculation": result}
            except:
                pass
    
    # Check for savings goal
    if 'save' in prompt or 'goal' in prompt:
        numbers = re.findall(r'\d+(?:\.\d+)?', prompt)
        if len(numbers) >= 3:
            try:
                target, current, monthly = float(numbers[0]), float(numbers[1]), float(numbers[2])
                result = calc.savings_goal(target, current, monthly)
                response = f"To reach your ${target:.0f} goal from ${current:.0f}, saving ${monthly:.0f}/month, it will take {result['time_estimate']}."
                return {"response": response, "calculation": result}
            except:
                pass
    
    # Use AI model if loaded
    if MODEL_LOADED:
        try:
            tokens = tokenizer.encode(prompt)
            input_ids = torch.tensor([tokens], dtype=torch.long).to(device)
            output_ids = model.generate(input_ids, max_new_tokens=100, temperature=0.8)
            response = tokenizer.decode(output_ids[0].tolist())
            return {"response": response}
        except Exception as e:
            return {"response": f"Error generating response: {str(e)}"}
    
    # Fallback responses
    fallback_responses = {
        "budget": "A good budget follows the 50/30/20 rule: 50% for needs, 30% for wants, and 20% for savings. Track your expenses and adjust as needed!",
        "save": "Start by automating your savings - pay yourself first! Aim to save at least 20% of your income. Build an emergency fund of 3-6 months expenses.",
        "invest": "Before investing, have an emergency fund and pay off high-interest debt. Start with low-cost index funds and think long-term (10+ years).",
        "debt": "Pay off high-interest debt first (avalanche method) or smallest debt first (snowball method). Pay more than the minimum whenever possible!",
        "expense": "Track expenses by category: housing, food, transport, utilities, entertainment. Review monthly and cut unnecessary spending."
    }
    
    for keyword, response in fallback_responses.items():
        if keyword in prompt:
            return {"response": response}
    
    return {"response": "I'm Aiza, your finance assistant! Ask me about budgeting, saving, investing, or debt management. I can also help calculate budgets and savings goals!"}


if __name__ == '__main__':
    print("Starting Aiza web interface...")
    print("Visit http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.post("/api/budget")
async def calculate_budget_api(request: Request):
    """Calculate budget breakdown"""
    data = await request.json()
    income = data.get('income', 0)
    expenses = data.get('expenses', {})
    
    result = calc.calculate_budget(income, expenses)
    recommendations = analyzer.get_recommendations(income, expenses)
    
    return JSONResponse({
        "budget": result,
        "recommendations": recommendations
    })


@app.post("/api/savings_goal")
async def savings_goal_api(request: Request):
    """Calculate savings goal timeline"""
    data = await request.json()
    target = data.get('target', 0)
    current = data.get('current', 0)
    monthly_save = data.get('monthly_save', 0)
    
    result = calc.savings_goal(target, current, monthly_save)
    return JSONResponse(result)


@app.post("/api/expense_analyze")
async def analyze_expenses_api(request: Request):
    """Analyze spending patterns"""
    data = await request.json()
    transactions = data.get('transactions', [])
    
    result = calc.analyze_spending(transactions)
    return JSONResponse(result)


@app.post("/api/debt_payoff")
async def debt_payoff_api(request: Request):
    """Calculate debt payoff timeline"""
    data = await request.json()
    balance = data.get('balance', 0)
    interest_rate = data.get('interest_rate', 0)
    monthly_payment = data.get('monthly_payment', 0)
    
    result = calc.debt_payoff(balance, interest_rate, monthly_payment)
    return JSONResponse(result)


@app.post("/api/compound_interest")
async def compound_interest_api(request: Request):
    """Calculate compound interest"""
    data = await request.json()
    principal = data.get('principal', 0)
    rate = data.get('rate', 0)
    years = data.get('years', 0)
    
    result = calc.compound_interest(principal, rate, years)
    return JSONResponse(result)


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse({
        "status": "healthy",
        "model_loaded": MODEL_LOADED,
        "device": device,
        "finance_tools": "active"
    })


# Real-time data integrations
from aiza.realtime_data import RealTimeDataHub

# Initialize real-time data hub
realtime_hub = RealTimeDataHub()


@app.get("/api/stock/{symbol}")
async def get_stock_price(symbol: str):
    """Get current stock price"""
    result = realtime_hub.stocks.get_stock_price(symbol.upper())
    return JSONResponse(result)


@app.get("/api/stock/{symbol}/history")
async def get_stock_history(symbol: str, days: int = 30):
    """Get stock price history"""
    result = realtime_hub.stocks.get_stock_history(symbol.upper(), days)
    return JSONResponse(result)


@app.get("/api/stock/search/{keywords}")
async def search_stocks(keywords: str):
    """Search for stocks"""
    results = realtime_hub.stocks.search_stocks(keywords)
    return JSONResponse({"results": results})


@app.get("/api/currency/{from_curr}/{to_curr}")
async def get_exchange_rate(from_curr: str, to_curr: str):
    """Get currency exchange rate"""
    result = realtime_hub.currency.get_exchange_rate(from_curr, to_curr)
    return JSONResponse(result)


@app.post("/api/currency/convert")
async def convert_currency(request: Request):
    """Convert currency amount"""
    data = await request.json()
    amount = data.get('amount', 0)
    from_curr = data.get('from', 'USD')
    to_curr = data.get('to', 'EUR')
    
    result = realtime_hub.currency.convert_currency(amount, from_curr, to_curr)
    return JSONResponse(result)


@app.get("/api/currency/rates/{base}")
async def get_all_rates(base: str = "USD"):
    """Get all exchange rates for base currency"""
    result = realtime_hub.currency.get_all_rates(base)
    return JSONResponse(result)


@app.get("/api/rates/federal")
async def get_federal_rate():
    """Get Federal Funds Rate"""
    result = realtime_hub.interest.get_federal_funds_rate()
    return JSONResponse(result)


@app.get("/api/rates/mortgage")
async def get_mortgage_rates():
    """Get current mortgage rates"""
    result = realtime_hub.interest.get_mortgage_rates()
    return JSONResponse(result)


@app.get("/api/rates/savings")
async def get_savings_rates():
    """Get savings account rates"""
    result = realtime_hub.interest.get_savings_rates()
    return JSONResponse(result)


@app.get("/api/rates/inflation")
async def get_inflation():
    """Get current inflation rate"""
    result = realtime_hub.interest.get_inflation_rate()
    return JSONResponse(result)


@app.get("/api/news/market")
async def get_market_news(limit: int = 10):
    """Get latest market news"""
    news = realtime_hub.news.get_market_news(limit)
    return JSONResponse({"news": news})


@app.get("/api/news/search/{query}")
async def search_news(query: str, limit: int = 5):
    """Search financial news"""
    news = realtime_hub.news.search_news(query, limit)
    return JSONResponse({"news": news})


@app.get("/api/bank/accounts")
async def get_bank_accounts(access_token: str = "demo"):
    """Get user's bank accounts"""
    result = realtime_hub.bank.get_accounts(access_token)
    return JSONResponse(result)


@app.get("/api/bank/transactions")
async def get_transactions(access_token: str = "demo", days: int = 30):
    """Get recent transactions"""
    result = realtime_hub.bank.get_transactions(access_token, days)
    return JSONResponse(result)


@app.get("/api/market/overview")
async def get_market_overview():
    """Get comprehensive market overview"""
    result = realtime_hub.get_market_overview()
    return JSONResponse(result)
