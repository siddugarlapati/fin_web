# Training Data Directory

This directory contains the finance training data for Aiza.

## Files

After running `python -m scripts.generate_finance_data`, you'll have:

- `finance_train.jsonl` - 5,000 training samples
- `finance_val.jsonl` - 500 validation samples

## Format

Each line is a JSON object with:
```json
{
  "prompt": "How should I budget my income?",
  "response": "A good budget follows the 50/30/20 rule..."
}
```

## Topics Covered

- Budget planning and management
- Expense tracking and categorization
- Savings strategies and goals
- Investment basics and compound interest
- Debt payoff strategies
- Emergency fund planning

## Generate Data

```bash
python -m scripts.generate_finance_data
```

This will create both training and validation datasets.
