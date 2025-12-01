# Aiza 💰

> BudgetPay's AI-Powered Finance Assistant

Aiza is a complete finance AI system that combines a custom-trained language model with powerful financial calculation tools. Get personalized budget advice, expense analysis, savings goals, and investment guidance - all powered by AI trained specifically for finance.

## Features

### 🤖 AI Capabilities
- Custom-trained finance language model
- Natural language understanding for financial queries
- Personalized budget and savings advice
- Investment and debt management guidance
- Advanced training with gradient clipping, warmup, and scheduling

### 💼 Finance Tools
- **Budget Calculator** - Analyze income vs expenses with 50/30/20 rule
- **Expense Tracker** - Automatic categorization and spending analysis
- **Savings Goals** - Calculate timeline to reach financial targets
- **Debt Payoff** - Plan debt elimination with interest calculations
- **Investment Calculator** - Compound interest and ROI projections
- **Emergency Fund** - Check if you have adequate savings buffer

### 🌐 Real-Time Data (NEW!)
- **Stock Prices** - Live stock quotes and historical data
- **Market Data** - Real-time indices (S&P 500, NASDAQ, Dow)
- **Currency Exchange** - Live exchange rates for 150+ currencies
- **Interest Rates** - Current Fed rates, mortgage rates, savings rates
- **Financial News** - Latest market news and events
- **Bank Integration** - Connect accounts via Plaid API

### 📊 Evaluation & Metrics
- Perplexity measurement
- Finance Q&A accuracy testing
- Model performance reports
- Finance tool validation tests

### 🌐 Web Interface
- Beautiful chat UI with BudgetPay branding
- Real-time AI responses
- Integrated finance calculators
- REST API for all finance tools

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Finance Training Data
```bash
python -m scripts.generate_finance_data
```
This creates 5,000 training samples and 500 validation samples of finance Q&A pairs.

### 3. Train the Model
```bash
python -m scripts.train_finance_model
```
Trains a 12-layer transformer model with advanced optimization features.

### 4. Evaluate Performance
```bash
python -m scripts.evaluate_model
```
Generates comprehensive evaluation report with metrics.

### 5. Start Chat Interface
```bash
python -m scripts.chat_web
```
Visit http://localhost:8000 to chat with Aiza!

## Usage Examples

### Chat Interface
Ask Aiza questions like:
- "How should I budget my $5000 monthly income?"
- "What's the 50/30/20 rule?"
- "How long to save $10,000 if I save $500/month?"
- "Should I pay off debt or invest?"
- "Help me reduce my spending"

### API Endpoints

**Calculate Budget:**
```bash
curl -X POST http://localhost:8000/api/budget \
  -H "Content-Type: application/json" \
  -d '{"income": 5000, "expenses": {"housing": 1500, "food": 600, "transport": 300}}'
```

**Savings Goal:**
```bash
curl -X POST http://localhost:8000/api/savings_goal \
  -H "Content-Type: application/json" \
  -d '{"target": 10000, "current": 2000, "monthly_save": 500}'
```

**Debt Payoff:**
```bash
curl -X POST http://localhost:8000/api/debt_payoff \
  -H "Content-Type: application/json" \
  -d '{"balance": 5000, "interest_rate": 0.18, "monthly_payment": 200}'
```

## Project Structure

```
aiza/
├── aiza/                          # Core library
│   ├── model.py                   # Transformer architecture
│   ├── tokenizer.py               # BPE tokenizer
│   ├── trainer.py                 # Advanced training loop
│   ├── data.py                    # Data loading utilities
│   ├── evaluator.py               # Model evaluation metrics
│   ├── finance_tools.py           # Financial calculators
│   └── finance_data.py            # Training data generation
├── scripts/                       # Training & inference
│   ├── generate_finance_data.py   # Create training data
│   ├── train_finance_model.py     # Train with finance data
│   ├── evaluate_model.py          # Run evaluations
│   ├── chat_web.py                # Web interface + API
│   ├── train_tokenizer.py         # Tokenizer training
│   └── train_model.py             # Base model training
├── data/                          # Training data (generated)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Advanced Features

### Training Enhancements
- **AdamW Optimizer** with weight decay
- **Learning Rate Warmup** for stable training
- **Cosine Annealing** scheduler
- **Gradient Clipping** to prevent exploding gradients
- **Automatic Checkpointing** saves best model
- **Validation Monitoring** tracks performance

### Finance Knowledge Base
- Budgeting strategies (50/30/20, zero-based, envelope)
- Savings principles (emergency fund, automation)
- Investment concepts (compound interest, diversification)
- Debt management (snowball, avalanche methods)

### Evaluation Metrics
- **Perplexity** - Language modeling quality
- **Finance Q&A Accuracy** - Domain-specific performance
- **Tool Validation** - Calculator correctness
- **Model Size** - Parameter count tracking

## Model Architecture

- **Type:** Transformer decoder (GPT-style)
- **Parameters:** ~50M (configurable)
- **Layers:** 12 transformer blocks
- **Attention Heads:** 8 per layer
- **Embedding Dimension:** 512
- **Max Sequence Length:** 512 tokens
- **Vocabulary Size:** 10,000 tokens

## Training Data

Aiza is trained on synthetic finance conversations covering:
- Budget planning and management
- Expense tracking and categorization
- Savings strategies and goals
- Investment basics and compound interest
- Debt payoff strategies
- Emergency fund planning

5,000+ Q&A pairs ensure comprehensive finance knowledge.

## API Reference

### Chat Endpoint
`POST /generate` - Generate AI response
```json
{"prompt": "How should I budget my income?"}
```

### Finance Tools
- `POST /api/budget` - Calculate budget breakdown
- `POST /api/savings_goal` - Savings timeline calculator
- `POST /api/expense_analyze` - Analyze spending patterns
- `POST /api/debt_payoff` - Debt elimination planner
- `POST /api/compound_interest` - Investment growth calculator
- `GET /api/health` - System health check

### Real-Time Data APIs

**Stock Market:**
- `GET /api/stock/{symbol}` - Get current stock price
- `GET /api/stock/{symbol}/history?days=30` - Historical data
- `GET /api/stock/search/{keywords}` - Search stocks

**Currency Exchange:**
- `GET /api/currency/{from}/{to}` - Get exchange rate
- `POST /api/currency/convert` - Convert amount between currencies
- `GET /api/currency/rates/{base}` - Get all rates for base currency

**Interest Rates:**
- `GET /api/rates/federal` - Federal Funds Rate
- `GET /api/rates/mortgage` - Current mortgage rates
- `GET /api/rates/savings` - Savings account rates
- `GET /api/rates/inflation` - Current inflation rate (CPI)

**News & Banking:**
- `GET /api/news/market?limit=10` - Latest market news
- `GET /api/news/search/{query}` - Search financial news
- `GET /api/bank/accounts` - Get user's bank accounts
- `GET /api/bank/transactions?days=30` - Recent transactions
- `GET /api/market/overview` - Comprehensive market snapshot

## Development

### Run Tests
```bash
python -m scripts.evaluate_model
```

### Train Custom Model
Edit `scripts/train_finance_model.py` to adjust:
- Model size (layers, dimensions)
- Training hyperparameters
- Batch size and epochs
- Learning rate schedule

### Add Finance Features
Extend `aiza/finance_tools.py` with new calculators and analyzers.

## Requirements

- Python 3.8+
- PyTorch 2.0+
- FastAPI for web interface
- 4GB+ RAM (8GB+ recommended)
- GPU optional but recommended for training

## License

Copyright (c) 2025 BudgetPay  
All rights reserved.

---

