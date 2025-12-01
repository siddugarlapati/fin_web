"""
Train Aiza on finance data with advanced features
"""
import torch
import json
import os
from torch.utils.data import Dataset
from aiza.model import AizaModel
from aiza.tokenizer import AizaTokenizer
from aiza.trainer import AizaTrainer


class FinanceDataset(Dataset):
    """Dataset for finance Q&A pairs"""
    
    def __init__(self, data_file, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.data = []
        
        # Load data
        with open(data_file, 'r') as f:
            for line in f:
                item = json.loads(line)
                text = f"Q: {item['prompt']}\nA: {item['response']}"
                self.data.append(text)
        
        print(f"Loaded {len(self.data)} samples from {data_file}")
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        text = self.data[idx]
        tokens = self.tokenizer.encode(text)
        
        # Truncate or pad
        if len(tokens) > self.max_length:
            tokens = tokens[:self.max_length]
        
        # Create input and target
        x = tokens[:-1]
        y = tokens[1:]
        
        # Pad if needed
        if len(x) < self.max_length - 1:
            x = x + [0] * (self.max_length - 1 - len(x))
            y = y + [0] * (self.max_length - 1 - len(y))
        
        return torch.tensor(x, dtype=torch.long), torch.tensor(y, dtype=torch.long)


def main():
    print("=" * 60)
    print("Aiza Finance Model Training")
    print("=" * 60)
    
    # Configuration
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"\nDevice: {device}")
    
    # Create data directory if needed
    os.makedirs('data', exist_ok=True)
    
    # Check if training data exists
    if not os.path.exists('data/finance_train.jsonl'):
        print("\n⚠️  Training data not found!")
        print("Run: python -m scripts.generate_finance_data")
        return
    
    # Load tokenizer
    print("\nLoading tokenizer...")
    tokenizer = AizaTokenizer()
    try:
        tokenizer.load('tokenizer.json')
        print(f"✓ Tokenizer loaded (vocab size: {tokenizer.vocab_size})")
    except:
        print("⚠️  Tokenizer not found. Using default vocab size 10000")
        tokenizer.vocab_size = 10000
    
    # Load datasets
    print("\nLoading datasets...")
    train_dataset = FinanceDataset('data/finance_train.jsonl', tokenizer)
    val_dataset = FinanceDataset('data/finance_val.jsonl', tokenizer)
    
    # Create model
    print("\nInitializing model...")
    model = AizaModel(
        vocab_size=tokenizer.vocab_size,
        dim=512,
        num_layers=12,
        num_heads=8,
        max_seq_len=512
    )
    
    num_params = sum(p.numel() for p in model.parameters())
    print(f"✓ Model created with {num_params:,} parameters")
    
    # Create trainer
    print("\nInitializing trainer...")
    trainer = AizaTrainer(
        model=model,
        train_data=train_dataset,
        val_data=val_dataset,
        lr=3e-4,
        device=device,
        weight_decay=0.1,
        grad_clip=1.0,
        warmup_steps=100
    )
    
    # Train
    print("\n" + "=" * 60)
    print("Starting training...")
    print("=" * 60 + "\n")
    
    trainer.train(
        num_epochs=10,
        batch_size=16,
        save_every=2
    )
    
    # Save final model
    print("\nSaving final model...")
    trainer.save_checkpoint('aiza_model.pt')
    print("✓ Model saved to aiza_model.pt")
    
    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Evaluate: python -m scripts.evaluate_model")
    print("2. Chat: python -m scripts.chat_web")


if __name__ == '__main__':
    main()
