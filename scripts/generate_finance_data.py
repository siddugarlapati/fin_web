"""
Generate synthetic finance training data
"""
from aiza.finance_data import FinanceDataGenerator

if __name__ == '__main__':
    print("Generating finance training data...")
    generator = FinanceDataGenerator()
    
    # Generate training data
    generator.save_dataset('data/finance_train.jsonl', num_samples=5000)
    
    # Generate validation data
    generator.save_dataset('data/finance_val.jsonl', num_samples=500)
    
    print("✓ Finance training data generated successfully!")
    print("  - Training: data/finance_train.jsonl (5000 samples)")
    print("  - Validation: data/finance_val.jsonl (500 samples)")
