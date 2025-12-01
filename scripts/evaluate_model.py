"""
Evaluate Aiza model performance
"""
import torch
import json
from aiza.model import AizaModel
from aiza.tokenizer import AizaTokenizer
from aiza.evaluator import AizaEvaluator, FinanceTaskEvaluator

def load_test_data(filename):
    """Load test data from jsonl file"""
    data = []
    with open(filename, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

if __name__ == '__main__':
    print("Loading model and tokenizer...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Load tokenizer
    tokenizer = AizaTokenizer()
    tokenizer.load('tokenizer.json')
    
    # Load model
    model = AizaModel(vocab_size=tokenizer.vocab_size)
    checkpoint = torch.load('aiza_best.pt', map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    
    print("Running evaluations...")
    
    # Test finance tools
    print("\n=== Finance Tools Tests ===")
    tool_results = FinanceTaskEvaluator.run_all_tests()
    
    # Evaluate model
    print("\n=== Model Evaluation ===")
    evaluator = AizaEvaluator(model, tokenizer, device)
    
    # Load test data
    test_data = load_test_data('data/finance_val.jsonl')
    test_texts = [item['prompt'] + ' ' + item['response'] for item in test_data[:100]]
    
    # Calculate metrics
    perplexity = evaluator.calculate_perplexity(test_texts)
    print(f"Perplexity: {perplexity:.2f}")
    
    qa_results = evaluator.evaluate_finance_qa(test_data[:50])
    print(f"Finance Q&A Accuracy: {qa_results['accuracy']:.2%}")
    print(f"Correct: {qa_results['correct']}/{qa_results['total']}")
    
    # Generate full report
    report = evaluator.generate_report(test_texts, test_data[:50])
    report['finance_tools'] = tool_results
    
    # Save report
    with open('evaluation_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n✓ Evaluation complete! Report saved to evaluation_report.json")
