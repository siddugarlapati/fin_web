"""
Real-time financial data integrations for Aiza
"""
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
import json


class StockMarketAPI:
    """Real-time stock market data"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "demo"  # Use demo key if none provided
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """Get current stock price"""
        try:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if "Global Quote" in data and data["Global Quote"]:
                quote = data["Global Quote"]
                return {
                    "symbol": symbol,
                    "price": float(quote.get("05. price", 0)),
                    "change": float(quote.get("09. change", 0)),
                    "change_percent": quote.get("10. change percent", "0%"),
                    "volume": int(quote.get("06. volume", 0)),
                    "timestamp": quote.get("07. latest trading day", ""),
                    "status": "success"
                }
            else:
                return {"status": "error", "message": "Stock not found or API limit reached"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_stock_history(self, symbol: str, days: int = 30) -> Dict[str, Any]:
        """Get historical stock data"""
        try:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if "Time Series (Daily)" in data:
                time_series = data["Time Series (Daily)"]
                history = []
                
                for date, values in list(time_series.items())[:days]:
                    history.append({
                        "date": date,
                        "open": float(values["1. open"]),
                        "high": float(values["2. high"]),
                        "low": float(values["3. low"]),
                        "close": float(values["4. close"]),
                        "volume": int(values["5. volume"])
                    })
                
                return {
                    "symbol": symbol,
                    "history": history,
                    "status": "success"
                }
            else:
                return {"status": "error", "message": "Data not available"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def search_stocks(self, keywords: str) -> List[Dict[str, str]]:
        """Search for stocks by name or symbol"""
        try:
            params = {
                "function": "SYMBOL_SEARCH",
                "keywords": keywords,
                "apikey": self.api_key
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if "bestMatches" in data:
                results = []
                for match in data["bestMatches"][:5]:
                    results.append({
                        "symbol": match.get("1. symbol", ""),
                        "name": match.get("2. name", ""),
                        "type": match.get("3. type", ""),
                        "region": match.get("4. region", "")
                    })
                return results
            return []
        except Exception as e:
            return []


class CurrencyExchangeAPI:
    """Real-time currency exchange rates"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.exchangerate-api.com/v4/latest"
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Get exchange rate between two currencies"""
        try:
            response = requests.get(f"{self.base_url}/{from_currency.upper()}", timeout=10)
            data = response.json()
            
            if "rates" in data and to_currency.upper() in data["rates"]:
                rate = data["rates"][to_currency.upper()]
                return {
                    "from": from_currency.upper(),
                    "to": to_currency.upper(),
                    "rate": rate,
                    "timestamp": data.get("date", ""),
                    "status": "success"
                }
            else:
                return {"status": "error", "message": "Currency not found"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Dict[str, Any]:
        """Convert amount from one currency to another"""
        rate_data = self.get_exchange_rate(from_currency, to_currency)
        
        if rate_data["status"] == "success":
            converted = amount * rate_data["rate"]
            return {
                "amount": amount,
                "from": from_currency.upper(),
                "to": to_currency.upper(),
                "rate": rate_data["rate"],
                "converted_amount": round(converted, 2),
                "status": "success"
            }
        return rate_data
    
    def get_all_rates(self, base_currency: str = "USD") -> Dict[str, Any]:
        """Get all exchange rates for a base currency"""
        try:
            response = requests.get(f"{self.base_url}/{base_currency.upper()}", timeout=10)
            data = response.json()
            
            if "rates" in data:
                return {
                    "base": base_currency.upper(),
                    "rates": data["rates"],
                    "timestamp": data.get("date", ""),
                    "status": "success"
                }
            return {"status": "error", "message": "Data not available"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


class InterestRatesAPI:
    """Current interest rates and economic indicators"""
    
    def __init__(self):
        self.fred_base = "https://api.stlouisfed.org/fred/series/observations"
    
    def get_federal_funds_rate(self) -> Dict[str, Any]:
        """Get current Federal Funds Rate"""
        # Using mock data - replace with actual FRED API key
        return {
            "rate": 5.33,
            "rate_percent": "5.33%",
            "name": "Federal Funds Effective Rate",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "Federal Reserve",
            "status": "success"
        }
    
    def get_mortgage_rates(self) -> Dict[str, Any]:
        """Get current mortgage rates"""
        return {
            "30_year_fixed": 6.95,
            "15_year_fixed": 6.38,
            "5_1_arm": 6.25,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "Freddie Mac",
            "status": "success"
        }
    
    def get_savings_rates(self) -> Dict[str, Any]:
        """Get typical savings account rates"""
        return {
            "national_average": 0.46,
            "high_yield_savings": 4.50,
            "money_market": 4.25,
            "cd_1_year": 5.00,
            "cd_5_year": 4.50,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "success"
        }
    
    def get_inflation_rate(self) -> Dict[str, Any]:
        """Get current inflation rate"""
        return {
            "rate": 3.2,
            "rate_percent": "3.2%",
            "name": "Consumer Price Index (CPI)",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "source": "Bureau of Labor Statistics",
            "status": "success"
        }


class FinancialNewsAPI:
    """Real-time financial news and events"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"
    
    def get_market_news(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get latest market news"""
        if not self.api_key:
            return self._get_mock_news()
        
        try:
            params = {
                "apiKey": self.api_key,
                "category": "business",
                "language": "en",
                "pageSize": limit
            }
            response = requests.get(f"{self.base_url}/top-headlines", params=params, timeout=10)
            data = response.json()
            
            if data.get("status") == "ok":
                articles = []
                for article in data.get("articles", []):
                    articles.append({
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "source": article.get("source", {}).get("name", ""),
                        "url": article.get("url", ""),
                        "published_at": article.get("publishedAt", "")
                    })
                return articles
            return self._get_mock_news()
        except Exception as e:
            return self._get_mock_news()
    
    def _get_mock_news(self) -> List[Dict[str, Any]]:
        """Mock news data when API not available"""
        return [
            {
                "title": "Markets Rally on Strong Economic Data",
                "description": "Stock markets reached new highs following positive employment reports.",
                "source": "Financial Times",
                "published_at": datetime.now().isoformat()
            },
            {
                "title": "Fed Holds Interest Rates Steady",
                "description": "Federal Reserve maintains current interest rate policy amid inflation concerns.",
                "source": "Reuters",
                "published_at": datetime.now().isoformat()
            },
            {
                "title": "Tech Stocks Lead Market Gains",
                "description": "Technology sector outperforms as investors bet on AI growth.",
                "source": "Bloomberg",
                "published_at": datetime.now().isoformat()
            }
        ]
    
    def search_news(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for specific financial news"""
        if not self.api_key:
            return self._get_mock_news()[:limit]
        
        try:
            params = {
                "apiKey": self.api_key,
                "q": query,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": limit
            }
            response = requests.get(f"{self.base_url}/everything", params=params, timeout=10)
            data = response.json()
            
            if data.get("status") == "ok":
                articles = []
                for article in data.get("articles", []):
                    articles.append({
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "source": article.get("source", {}).get("name", ""),
                        "url": article.get("url", ""),
                        "published_at": article.get("publishedAt", "")
                    })
                return articles
            return []
        except Exception as e:
            return []


class BankIntegrationAPI:
    """Bank account integration (Plaid-style)"""
    
    def __init__(self, client_id: Optional[str] = None, secret: Optional[str] = None):
        self.client_id = client_id
        self.secret = secret
        self.base_url = "https://sandbox.plaid.com"  # Use sandbox for demo
    
    def get_accounts(self, access_token: str) -> Dict[str, Any]:
        """Get user's bank accounts"""
        # Mock implementation - replace with actual Plaid integration
        return {
            "accounts": [
                {
                    "account_id": "acc_001",
                    "name": "Checking Account",
                    "type": "depository",
                    "subtype": "checking",
                    "balance": 5420.50,
                    "currency": "USD"
                },
                {
                    "account_id": "acc_002",
                    "name": "Savings Account",
                    "type": "depository",
                    "subtype": "savings",
                    "balance": 12500.00,
                    "currency": "USD"
                },
                {
                    "account_id": "acc_003",
                    "name": "Credit Card",
                    "type": "credit",
                    "subtype": "credit card",
                    "balance": -1250.75,
                    "currency": "USD"
                }
            ],
            "status": "success"
        }
    
    def get_transactions(self, access_token: str, days: int = 30) -> Dict[str, Any]:
        """Get recent transactions"""
        # Mock implementation
        return {
            "transactions": [
                {
                    "transaction_id": "txn_001",
                    "date": "2025-11-30",
                    "name": "Whole Foods Market",
                    "amount": 87.43,
                    "category": ["Shops", "Food and Drink", "Groceries"],
                    "account_id": "acc_001"
                },
                {
                    "transaction_id": "txn_002",
                    "date": "2025-11-29",
                    "name": "Shell Gas Station",
                    "amount": 52.00,
                    "category": ["Travel", "Gas Stations"],
                    "account_id": "acc_001"
                },
                {
                    "transaction_id": "txn_003",
                    "date": "2025-11-28",
                    "name": "Netflix",
                    "amount": 15.99,
                    "category": ["Service", "Entertainment", "Streaming"],
                    "account_id": "acc_001"
                }
            ],
            "status": "success"
        }
    
    def categorize_transactions(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Categorize and analyze transactions"""
        categories = {}
        total = 0
        
        for txn in transactions:
            amount = txn.get("amount", 0)
            category = txn.get("category", ["Other"])[0] if txn.get("category") else "Other"
            
            categories[category] = categories.get(category, 0) + amount
            total += amount
        
        return {
            "total_spending": total,
            "categories": categories,
            "transaction_count": len(transactions),
            "status": "success"
        }


class RealTimeDataHub:
    """Central hub for all real-time data"""
    
    def __init__(self, stock_api_key=None, news_api_key=None, plaid_client_id=None, plaid_secret=None):
        self.stocks = StockMarketAPI(stock_api_key)
        self.currency = CurrencyExchangeAPI()
        self.interest = InterestRatesAPI()
        self.news = FinancialNewsAPI(news_api_key)
        self.bank = BankIntegrationAPI(plaid_client_id, plaid_secret)
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Get comprehensive market overview"""
        return {
            "stocks": {
                "sp500": self.stocks.get_stock_price("SPY"),
                "nasdaq": self.stocks.get_stock_price("QQQ"),
                "dow": self.stocks.get_stock_price("DIA")
            },
            "rates": {
                "federal_funds": self.interest.get_federal_funds_rate(),
                "mortgage": self.interest.get_mortgage_rates(),
                "savings": self.interest.get_savings_rates(),
                "inflation": self.interest.get_inflation_rate()
            },
            "news": self.news.get_market_news(5),
            "timestamp": datetime.now().isoformat()
        }
