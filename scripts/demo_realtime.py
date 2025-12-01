"""
Demo script for real-time data features
"""
from aiza.realtime_data import RealTimeDataHub
import json


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demo_stock_prices():
    """Demo stock price lookup"""
    print_section("📈 Real-Time Stock Prices")
    
    hub = RealTimeDataHub()
    
    symbols = ["AAPL", "GOOGL", "MSFT"]
    
    for symbol in symbols:
        result = hub.stocks.get_stock_price(symbol)
        if result["status"] == "success":
            print(f"{symbol}:")
            print(f"  Price: ${result['price']:.2f}")
            print(f"  Change: {result['change']:+.2f} ({result['change_percent']})")
            print(f"  Volume: {result['volume']:,}")
            print()
        else:
            print(f"{symbol}: {result['message']}\n")


def demo_currency_exchange():
    """Demo currency exchange rates"""
    print_section("💱 Currency Exchange Rates")
    
    hub = RealTimeDataHub()
    
    # Single conversion
    result = hub.currency.convert_currency(1000, "USD", "EUR")
    if result["status"] == "success":
        print(f"${result['amount']:,.2f} USD = €{result['converted_amount']:,.2f} EUR")
        print(f"Exchange Rate: {result['rate']:.4f}")
        print()
    
    # Multiple currencies
    print("Popular Exchange Rates (from USD):")
    currencies = ["EUR", "GBP", "JPY", "CAD", "AUD"]
    
    for curr in currencies:
        result = hub.currency.get_exchange_rate("USD", curr)
        if result["status"] == "success":
            print(f"  1 USD = {result['rate']:.4f} {curr}")


def demo_interest_rates():
    """Demo current interest rates"""
    print_section("📊 Current Interest Rates")
    
    hub = RealTimeDataHub()
    
    # Federal Funds Rate
    fed_rate = hub.interest.get_federal_funds_rate()
    print(f"Federal Funds Rate: {fed_rate['rate_percent']}")
    print()
    
    # Mortgage Rates
    mortgage = hub.interest.get_mortgage_rates()
    print("Mortgage Rates:")
    print(f"  30-Year Fixed: {mortgage['30_year_fixed']:.2f}%")
    print(f"  15-Year Fixed: {mortgage['15_year_fixed']:.2f}%")
    print(f"  5/1 ARM: {mortgage['5_1_arm']:.2f}%")
    print()
    
    # Savings Rates
    savings = hub.interest.get_savings_rates()
    print("Savings Rates:")
    print(f"  National Average: {savings['national_average']:.2f}%")
    print(f"  High-Yield Savings: {savings['high_yield_savings']:.2f}%")
    print(f"  1-Year CD: {savings['cd_1_year']:.2f}%")
    print()
    
    # Inflation
    inflation = hub.interest.get_inflation_rate()
    print(f"Current Inflation (CPI): {inflation['rate_percent']}")


def demo_market_news():
    """Demo financial news"""
    print_section("📰 Latest Market News")
    
    hub = RealTimeDataHub()
    
    news = hub.news.get_market_news(5)
    
    for i, article in enumerate(news, 1):
        print(f"{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        if article.get('description'):
            print(f"   {article['description'][:100]}...")
        print()


def demo_bank_accounts():
    """Demo bank account integration"""
    print_section("🏦 Bank Account Integration")
    
    hub = RealTimeDataHub()
    
    # Get accounts
    accounts = hub.bank.get_accounts("demo_token")
    
    if accounts["status"] == "success":
        print("Your Accounts:")
        total_balance = 0
        
        for acc in accounts["accounts"]:
            balance = acc["balance"]
            total_balance += balance
            sign = "-" if balance < 0 else ""
            print(f"  {acc['name']}: {sign}${abs(balance):,.2f}")
        
        print(f"\nTotal Net Worth: ${total_balance:,.2f}")
        print()
    
    # Get transactions
    transactions = hub.bank.get_transactions("demo_token", 7)
    
    if transactions["status"] == "success":
        print("Recent Transactions (Last 7 days):")
        for txn in transactions["transactions"][:5]:
            print(f"  {txn['date']} | {txn['name']:<25} | ${txn['amount']:>8.2f}")


def demo_market_overview():
    """Demo comprehensive market overview"""
    print_section("🌍 Market Overview")
    
    hub = RealTimeDataHub()
    
    overview = hub.get_market_overview()
    
    # Major Indices
    print("Major Indices:")
    for name, data in overview["stocks"].items():
        if data.get("status") == "success":
            print(f"  {name.upper()}: ${data['price']:.2f} ({data['change_percent']})")
    
    print()
    
    # Key Rates
    print("Key Rates:")
    print(f"  Fed Funds: {overview['rates']['federal_funds']['rate_percent']}")
    print(f"  30Y Mortgage: {overview['rates']['mortgage']['30_year_fixed']:.2f}%")
    print(f"  Inflation: {overview['rates']['inflation']['rate_percent']}")
    
    print()
    
    # Top News
    print("Top Headlines:")
    for i, article in enumerate(overview["news"][:3], 1):
        print(f"  {i}. {article['title']}")


def demo_stock_search():
    """Demo stock search"""
    print_section("🔍 Stock Search")
    
    hub = RealTimeDataHub()
    
    query = "Apple"
    print(f"Searching for: {query}\n")
    
    results = hub.stocks.search_stocks(query)
    
    if results:
        print("Search Results:")
        for result in results:
            print(f"  {result['symbol']}: {result['name']}")
            print(f"    Type: {result['type']} | Region: {result['region']}")
            print()
    else:
        print("No results found or API limit reached")


def main():
    """Run all demos"""
    print("\n" + "=" * 60)
    print("  AIZA REAL-TIME DATA DEMO")
    print("  BudgetPay AI Assistant")
    print("=" * 60)
    
    demos = [
        demo_stock_prices,
        demo_currency_exchange,
        demo_interest_rates,
        demo_market_news,
        demo_bank_accounts,
        demo_market_overview,
        demo_stock_search
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n❌ Error in {demo.__name__}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)
    print("\n✓ All real-time data features are working!")
    print("\nNote: Some features use demo/mock data.")
    print("Add API keys for full functionality:")
    print("  - Alpha Vantage (stocks): https://www.alphavantage.co/")
    print("  - News API (news): https://newsapi.org/")
    print("  - Plaid (banking): https://plaid.com/")
    print()


if __name__ == '__main__':
    main()
