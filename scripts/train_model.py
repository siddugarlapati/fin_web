"""
Train Aiza base model
"""
import torch
from aiza.model import AizaModel
from aiza.trainer import AizaTrainer
from aiza.data import TextDataset, load_finance_data
from aiza.tokenizer import AizaTokenizer


def main():
    # Load tokenizer
    tokenizer = AizaTokenizer()
    tokenizer.load('tokenizer.json')
    
    # Load data
    texts = load_finance_data()
    dataset = TextDataset(texts, tokenizer)
    
    # Initialize model
    model = AizaModel(
        vocab_size=tokenizer.vocab_size,
        dim=512,
        num_layers=8,
        num_heads=8,
        max_seq_len=512
    )
    
    # Train
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    trainer = AizaTrainer(model, dataset, device=device)
    trainer.train(num_epochs=10, batch_size=4)
    
    # Save
    trainer.save_checkpoint('aiza_model.pt')
    print("Training complete! Model saved to aiza_model.pt")


if __name__ == '__main__':
    main()
