"""
Train Aiza tokenizer
"""
from aiza.tokenizer import AizaTokenizer
from aiza.data import load_finance_data


def main():
    # Load training data
    texts = load_finance_data()
    
    # Train tokenizer
    tokenizer = AizaTokenizer(vocab_size=10000)
    tokenizer.train(texts)
    
    # Save
    tokenizer.save('tokenizer.json')
    print("Tokenizer trained and saved to tokenizer.json")
    
    # Test
    test_text = "What is a budget?"
    encoded = tokenizer.encode(test_text)
    decoded = tokenizer.decode(encoded)
    print(f"\nTest encoding:")
    print(f"Original: {test_text}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")


if __name__ == '__main__':
    main()
