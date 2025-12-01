"""
Financial automation and tax planning
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


class AutoInvestmentManager:
    """Manage automatic investments"""
    
    def __init__(self):
        self.auto_rules = {}
    
    def create_auto_investment_rule(self, user_id: str, rule: Dict) -> str:
        """Create automatic investment rule"""
        rule_id = f"rule_{len(self.auto_rules) + 1}"
        
        self.auto_rules[rule_id] = {
            'user_id': user_id,
            'type': rule.get('type', 'sip'),  # sip, recurring_deposit, etc.
            'amount': rule.get('amount', 0),
            'frequency': rule.get('frequency', 'monthly'),  # monthly, weekly, daily
            'fund_name': rule.get('fund_name'),
            'start_date': rule.get('start_date', datetime.now().isoformat()),
            'end_date': rule.get('end_date'),
            'active': True,
            'last_executed': None,
            'total_invested': 0
        }
        
        return rule_id
    
    def execute_auto_investments(self, user_id: str, current_balance: float) -> List[Dict]:
        """Execute pending auto investments"""
        executed = []
        
        for rule_id, rule in self.auto_rules.items():
            if rule['user_id'] != user_id or not rule['active']:
                continue
            
            # Check if due
            if self._is_investment_due(rule):
                amount = rule['amount']
                
                # Check if sufficient balance
                if current_balance >= amount:
                    execution = {
                        'rule_id': rule_id,
                        'type': rule['type'],
                        'amount': amount,
                        'fund_name': rule['fund_name'],
                        'executed_at': datetime.now().isoformat(),
                        'status': 'success'
                    }
                    
                    # Update rule
                    rule['last_executed'] = datetime.now().isoformat()
                    rule['total_invested'] += amount
                    current_balance -= amount
                    
                    executed.append(execution)
                else:
                    executed.append({
                        'rule_id': rule_id,
                        'status': 'failed',
                        'reason': 'insufficient_balance',
                        'required': amount,
                        'available': current_balance
                    })
        
        return executed
    
    def _is_investment_due(self, rule: Dict) -> bool:
        """Check if investment is due"""
        if not rule.get('last_executed'):
            return True
        
        last_executed = datetime.fromisoformat(rule['last_executed'])
        frequency = rule['frequency']
        
        if frequency == 'daily':
            return (datetime.now() - last_executed).days >= 1
        elif frequency == 'weekly':
            return (datetime.now() - last_executed).days >= 7
        elif frequency == 'monthly':
            return (datetime.now() - last_executed).days >= 30
        
        return False
    
    def get_auto_investment_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of auto investments"""
        user_rules = [r for r in self.auto_rules.values() if r['user_id'] == user_id]
        
        total_monthly = sum(r['amount'] for r in user_rules if r['frequency'] == 'monthly' and r['active'])
        total_invested = sum(r['total_invested'] for r in user_rules)
        
        return {
            'active_rules': len([r for r in user_rules if r['active']]),
            'total_monthly_investment': total_monthly,
            'total_invested_to_date': total_invested,
            'rules': user_rules
        }


class AutoBillPayManager:
    """Manage automatic bill payments"""
    
    def __init__(self):
        self.auto_bills = {}
    
    def setup_auto_pay(self, user_id: str, bill: Dict) -> str:
        """Setup automatic bill payment"""
        bill_id = f"bill_{len(self.auto_bills) + 1}"
        
        self.auto_bills[bill_id] = {
            'user_id': user_id,
            'biller_name': bill.get('biller_name'),
            'amount': bill.get('amount'),
            'due_day': bill.get('due_day', 1),  # Day of month
            'account_number': bill.get('account_number'),
            'active': True,
            'last_paid': None,
            'total_paid': 0,
            'payment_history': []
        }
        
        return bill_id
    
    def execute_auto_payments(self, user_id: str, current_balance: float) -> List[Dict]:
        """Execute pending bill payments"""
        executed = []
        today = datetime.now().day
        
        for bill_id, bill in self.auto_bills.items():
            if bill['user_id'] != user_id or not bill['active']:
                continue
            
            # Check if payment is due
            if today == bill['due_day']:
                # Check if already paid this month
                if bill['last_paid']:
                    last_paid = datetime.fromisoformat(bill['last_paid'])
                    if last_paid.month == datetime.now().month:
                        continue
                
                amount = bill['amount']
                
                if current_balance >= amount:
                    payment = {
                        'bill_id': bill_id,
                        'biller': bill['biller_name'],
                        'amount': amount,
                        'paid_at': datetime.now().isoformat(),
                        'status': 'success'
                    }
                    
                    # Update bill
                    bill['last_paid'] = datetime.now().isoformat()
                    bill['total_paid'] += amount
                    bill['payment_history'].append(payment)
                    current_balance -= amount
                    
                    executed.append(payment)
                else:
                    executed.append({
                        'bill_id': bill_id,
                        'biller': bill['biller_name'],
                        'status': 'failed',
                        'reason': 'insufficient_balance',
                        'required': amount,
                        'available': current_balance
                    })
        
        return executed
    
    def get_upcoming_bills(self, user_id: str, days_ahead: int = 7) -> List[Dict]:
        """Get bills due in next N days"""
        upcoming = []
        today = datetime.now().day
        
        for bill_id, bill in self.auto_bills.items():
            if bill['user_id'] != user_id or not bill['active']:
                continue
            
            due_day = bill['due_day']
            days_until = (due_day - today) % 30
            
            if 0 <= days_until <= days_ahead:
                upcoming.append({
                    'bill_id': bill_id,
                    'biller': bill['biller_name'],
                    'amount': bill['amount'],
                    'due_day': due_day,
                    'days_until': days_until
                })
        
        return sorted(upcoming, key=lambda x: x['days_until'])


class SalaryDistributor:
    """Automatically distribute salary into envelopes"""
    
    def __init__(self):
        self.distribution_rules = {}
    
    def create_distribution_rule(self, user_id: str, salary: float, 
                                 allocations: Dict[str, float]) -> str:
        """Create salary distribution rule"""
        rule_id = f"dist_{len(self.distribution_rules) + 1}"
        
        # Validate allocations sum to 100%
        total_percent = sum(allocations.values())
        if abs(total_percent - 100) > 0.01:
            raise ValueError(f"Allocations must sum to 100%, got {total_percent}%")
        
        self.distribution_rules[rule_id] = {
            'user_id': user_id,
            'salary': salary,
            'allocations': allocations,
            'active': True,
            'last_executed': None
        }
        
        return rule_id
    
    def distribute_salary(self, user_id: str, salary_amount: float) -> Dict[str, Any]:
        """Distribute salary according to rules"""
        # Find user's rule
        rule = None
        for r in self.distribution_rules.values():
            if r['user_id'] == user_id and r['active']:
                rule = r
                break
        
        if not rule:
            return {'error': 'No distribution rule found'}
        
        distribution = {}
        for envelope, percentage in rule['allocations'].items():
            amount = salary_amount * (percentage / 100)
            distribution[envelope] = round(amount, 2)
        
        return {
            'salary_amount': salary_amount,
            'distribution': distribution,
            'distributed_at': datetime.now().isoformat()
        }
    
    def suggest_distribution(self, monthly_income: float) -> Dict[str, float]:
        """Suggest salary distribution"""
        # Based on 50/30/20 rule with envelopes
        return {
            'essentials': 50.0,  # Rent, utilities, groceries
            'wants': 30.0,  # Entertainment, dining, shopping
            'savings': 15.0,  # Emergency fund, investments
            'investments': 5.0  # SIP, stocks
        }


class TaxPlanner:
    """Tax planning and optimization"""
    
    def __init__(self):
        # Indian tax slabs (FY 2024-25)
        self.tax_slabs = [
            {'min': 0, 'max': 300000, 'rate': 0},
            {'min': 300000, 'max': 700000, 'rate': 5},
            {'min': 700000, 'max': 1000000, 'rate': 10},
            {'min': 1000000, 'max': 1200000, 'rate': 15},
            {'min': 1200000, 'max': 1500000, 'rate': 20},
            {'min': 1500000, 'max': float('inf'), 'rate': 30}
        ]
        
        self.deductions_80c_limit = 150000
        self.deductions_80d_limit = 25000
    
    def calculate_tax(self, annual_income: float, regime: str = 'new') -> Dict[str, Any]:
        """Calculate income tax"""
        if regime == 'old':
            # Old regime with deductions
            taxable_income = annual_income
        else:
            # New regime without deductions
            taxable_income = annual_income
        
        tax = 0
        for slab in self.tax_slabs:
            if taxable_income > slab['min']:
                taxable_in_slab = min(taxable_income, slab['max']) - slab['min']
                tax += taxable_in_slab * (slab['rate'] / 100)
        
        # Add cess (4%)
        cess = tax * 0.04
        total_tax = tax + cess
        
        return {
            'annual_income': annual_income,
            'taxable_income': taxable_income,
            'tax_before_cess': round(tax, 2),
            'cess': round(cess, 2),
            'total_tax': round(total_tax, 2),
            'effective_tax_rate': round((total_tax / annual_income * 100), 2),
            'monthly_tax': round(total_tax / 12, 2)
        }
    
    def suggest_tax_savings(self, annual_income: float, current_investments: Dict) -> List[Dict]:
        """Suggest tax-saving investments"""
        suggestions = []
        
        # 80C deductions
        current_80c = current_investments.get('80c', 0)
        remaining_80c = self.deductions_80c_limit - current_80c
        
        if remaining_80c > 0:
            suggestions.append({
                'section': '80C',
                'remaining_limit': remaining_80c,
                'options': ['ELSS Mutual Funds', 'PPF', 'EPF', 'Life Insurance', 'NSC'],
                'tax_saved': round(remaining_80c * 0.3, 2),  # Assuming 30% tax bracket
                'priority': 'high'
            })
        
        # 80D deductions (Health Insurance)
        current_80d = current_investments.get('80d', 0)
        remaining_80d = self.deductions_80d_limit - current_80d
        
        if remaining_80d > 0:
            suggestions.append({
                'section': '80D',
                'remaining_limit': remaining_80d,
                'options': ['Health Insurance Premium'],
                'tax_saved': round(remaining_80d * 0.3, 2),
                'priority': 'medium'
            })
        
        # NPS (80CCD(1B))
        if current_investments.get('nps', 0) < 50000:
            suggestions.append({
                'section': '80CCD(1B)',
                'remaining_limit': 50000 - current_investments.get('nps', 0),
                'options': ['National Pension System (NPS)'],
                'tax_saved': round((50000 - current_investments.get('nps', 0)) * 0.3, 2),
                'priority': 'medium'
            })
        
        return suggestions
    
    def compare_tax_regimes(self, annual_income: float, deductions: float) -> Dict[str, Any]:
        """Compare old vs new tax regime"""
        # New regime (no deductions)
        new_regime_tax = self.calculate_tax(annual_income, 'new')
        
        # Old regime (with deductions)
        taxable_old = max(0, annual_income - deductions)
        old_regime_tax = self.calculate_tax(taxable_old, 'old')
        
        savings = old_regime_tax['total_tax'] - new_regime_tax['total_tax']
        
        return {
            'new_regime': new_regime_tax,
            'old_regime': old_regime_tax,
            'savings_with_old': round(savings, 2),
            'recommended': 'old' if savings > 0 else 'new',
            'reason': f"Save ₹{abs(savings):.0f} with {'old' if savings > 0 else 'new'} regime"
        }
