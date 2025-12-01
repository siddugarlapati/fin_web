"""
Evaluation metrics for Aiza model
"""
import torch
import torch.nn.functional as F
from typing import Dict, List
import json


class AizaEvaluator:
    """Evaluate model performance on various metrics"""
    
    def __init__(self, model, tokenizer, device='cuda'):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
    
    @torch.no_grad()
    def calculate_perplexity(self, text_samples: List[str]) -> float:
        """Calculate perplexity on text samples"""
        self.model.eval()
        total_loss = 0
        total_tokens = 0
        
        for text in text_samples:
            tokens = self.tokenizer.encode(text)
            if len(tokens) < 2:
                continue
            
            input_ids = torch.tensor([tokens[:-1]], dtype=torch.long).to(self.device)
            target_ids = torch.tensor([tokens[1:]], dtype=torch.long).to(self.device)
            
            logits = self.model(input_ids)
            loss = F.cross_entropy(
                logits.view(-1, logits.size(-1)),
                target_ids.view(-1),
                reduction='sum'
            )
            
            total_loss += loss.item()
            total_tokens += len(tokens) - 1
        
        avg_loss = total_loss / total_tokens if total_tokens > 0 else float('inf')
        perplexity = torch.exp(torch.tensor(avg_loss)).item()
        
        return perplexity
    
    @torch.no_grad()
    def evaluate_finance_qa(self, qa_pairs: List[Dict[str, str]]) -> Dict[str, float]:
        """Evaluate on finance Q&A pairs"""
        self.model.eval()
        correct = 0
        total = len(qa_pairs)
        
        for pair in qa_pairs:
            prompt = pair['prompt']
            expected_keywords = self._extract_keywords(pair['response'])
            
            # Generate response
            tokens = self.tokenizer.encode(prompt)
            input_ids = torch.tensor([tokens], dtype=torch.long).to(self.device)
            output_ids = self.model.generate(input_ids, max_new_tokens=100, temperature=0.7)
            generated = self.tokenizer.decode(output_ids[0].tolist())
            
            # Check if key concepts are present
            if self._contains_keywords(generated, expected_keywords):
                correct += 1
        
        accuracy = correct / total if total > 0 else 0
        return {
            "accuracy": accuracy,
            "correct": correct,
            "total": total
        }
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract key finance terms from text"""
        keywords = []
        finance_terms = [
            'budget', 'save', 'savings', 'invest', 'debt', 'expense',
            'income', 'emergency fund', 'interest', 'compound', '50/30/20',
            'diversify', 'portfolio', 'credit', 'loan', 'payment'
        ]
        
        text_lower = text.lower()
        for term in finance_terms:
            if term in text_lower:
                keywords.append(term)
        
        return keywords[:5]  # Top 5 keywords
    
    def _contains_keywords(self, text: str, keywords: List[str]) -> bool:
        """Check if text contains at least some keywords"""
        if not keywords:
            return True
        
        text_lower = text.lower()
        matches = sum(1 for kw in keywords if kw in text_lower)
        return matches >= len(keywords) * 0.3  # At least 30% match
    
    @torch.no_grad()
    def calculate_loss(self, dataloader) -> float:
        """Calculate average loss on dataset"""
        self.model.eval()
        total_loss = 0
        num_batches = 0
        
        for batch in dataloader:
            x, y = batch
            x, y = x.to(self.device), y.to(self.device)
            
            logits = self.model(x)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), y.view(-1))
            total_loss += loss.item()
            num_batches += 1
        
        return total_loss / num_batches if num_batches > 0 else float('inf')
    
    def generate_report(self, test_data: List[str], qa_pairs: List[Dict]) -> Dict:
        """Generate comprehensive evaluation report"""
        report = {
            "perplexity": self.calculate_perplexity(test_data),
            "finance_qa": self.evaluate_finance_qa(qa_pairs),
            "model_size": sum(p.numel() for p in self.model.parameters()),
            "trainable_params": sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        }
        
        return report
    
    def save_report(self, report: Dict, filename: str = "evaluation_report.json"):
        """Save evaluation report to file"""
        with open(filename, 'w') as f:
            json.dumps(report, f, indent=2)
        print(f"Evaluation report saved to {filename}")


class FinanceTaskEvaluator:
    """Evaluate specific finance tasks"""
    
    @staticmethod
    def test_budget_calculation():
        """Test budget calculation accuracy"""
        from aiza.finance_tools import FinanceCalculator
        
        calc = FinanceCalculator()
        result = calc.calculate_budget(
            income=5000,
            expenses={
                "housing": 1500,
                "food": 600,
                "transport": 300,
                "utilities": 200,
                "entertainment": 400
            }
        )
        
        assert result['savings'] == 2000
        assert result['status'] == 'healthy'
        return True
    
    @staticmethod
    def test_savings_goal():
        """Test savings goal calculation"""
        from aiza.finance_tools import FinanceCalculator
        
        calc = FinanceCalculator()
        result = calc.savings_goal(
            target=10000,
            current=2000,
            monthly_save=500
        )
        
        assert result['remaining'] == 8000
        assert result['months_needed'] == 16
        return True
    
    @staticmethod
    def run_all_tests():
        """Run all finance tool tests"""
        tests = [
            ("Budget Calculation", FinanceTaskEvaluator.test_budget_calculation),
            ("Savings Goal", FinanceTaskEvaluator.test_savings_goal)
        ]
        
        results = {}
        for name, test_func in tests:
            try:
                test_func()
                results[name] = "PASS"
                print(f"✓ {name}: PASS")
            except Exception as e:
                results[name] = f"FAIL: {str(e)}"
                print(f"✗ {name}: FAIL - {str(e)}")
        
        return results
