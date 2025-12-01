"""
Data loading utilities for Aiza
"""
import torch
from torch.utils.data import Dataset


class TextDataset(Dataset):
    def __init__(self, texts, tokenizer, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples = []
        
        for text in texts:
            tokens = tokenizer.encode(text)
            if len(tokens) > max_length:
                tokens = tokens[:max_length]
            self.examples.append(tokens)
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        tokens = self.examples[idx]
        x = torch.tensor(tokens[:-1], dtype=torch.long)
        y = torch.tensor(tokens[1:], dtype=torch.long)
        return x, y


def load_finance_data():
    """Load sample finance data for training"""
    # This is a placeholder - in production, load real finance datasets
    sample_texts = [
        "What is a budget? A budget is a financial plan that helps you track income and expenses.",
        "How do I save money? Start by tracking your spending and identifying areas to cut costs.",
        "What is compound interest? Compound interest is interest calculated on initial principal and accumulated interest.",
        "How to invest wisely? Diversify your portfolio and invest for the long term.",
        "What is an emergency fund? An emergency fund is savings set aside for unexpected expenses.",
    ]
    return sample_texts
