"""
SMS/Email parsing and OCR for automatic transaction detection
"""
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import json


class SMSParser:
    """Parse bank SMS messages to extract transaction details"""
    
    def __init__(self):
        # Common bank SMS patterns
        self.patterns = {
            'debit': [
                r'debited.*?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'spent.*?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'withdrawn.*?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'paid.*?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            ],
            'credit': [
                r'credited.*?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'received.*?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'deposited.*?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            ],
            'merchant': [
                r'at\s+([A-Z][A-Za-z0-9\s]+?)(?:\s+on|\s+Rs)',
                r'to\s+([A-Z][A-Za-z0-9\s]+?)(?:\s+on|\s+Rs)',
            ],
            'card': [
                r'card\s+(?:ending\s+)?(\d{4})',
                r'XX(\d{4})',
            ],
            'balance': [
                r'(?:balance|bal|avl\s+bal).*?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            ]
        }
    
    def parse_sms(self, message: str) -> Optional[Dict[str, Any]]:
        """Parse a bank SMS message"""
        message_lower = message.lower()
        
        # Detect transaction type
        is_debit = any(word in message_lower for word in ['debited', 'spent', 'withdrawn', 'paid'])
        is_credit = any(word in message_lower for word in ['credited', 'received', 'deposited'])
        
        if not (is_debit or is_credit):
            return None
        
        transaction = {
            'type': 'debit' if is_debit else 'credit',
            'amount': None,
            'merchant': None,
            'card_last4': None,
            'balance': None,
            'timestamp': datetime.now().isoformat(),
            'raw_message': message
        }
        
        # Extract amount
        patterns = self.patterns['debit'] if is_debit else self.patterns['credit']
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                transaction['amount'] = float(amount_str)
                break
        
        # Extract merchant
        for pattern in self.patterns['merchant']:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                transaction['merchant'] = match.group(1).strip()
                break
        
        # Extract card number
        for pattern in self.patterns['card']:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                transaction['card_last4'] = match.group(1)
                break
        
        # Extract balance
        for pattern in self.patterns['balance']:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                balance_str = match.group(1).replace(',', '')
                transaction['balance'] = float(balance_str)
                break
        
        return transaction if transaction['amount'] else None
    
    def parse_bulk_sms(self, messages: List[str]) -> List[Dict[str, Any]]:
        """Parse multiple SMS messages"""
        transactions = []
        for msg in messages:
            parsed = self.parse_sms(msg)
            if parsed:
                transactions.append(parsed)
        return transactions


class EmailParser:
    """Parse bank emails to extract transaction and bill details"""
    
    def __init__(self):
        self.bill_keywords = ['bill', 'invoice', 'payment due', 'statement', 'due date']
    
    def parse_email(self, subject: str, body: str) -> Optional[Dict[str, Any]]:
        """Parse bank/bill email"""
        subject_lower = subject.lower()
        body_lower = body.lower()
        
        # Detect if it's a bill
        is_bill = any(keyword in subject_lower or keyword in body_lower for keyword in self.bill_keywords)
        
        if is_bill:
            return self._parse_bill_email(subject, body)
        else:
            return self._parse_transaction_email(subject, body)
    
    def _parse_bill_email(self, subject: str, body: str) -> Dict[str, Any]:
        """Parse bill/invoice email"""
        bill = {
            'type': 'bill',
            'amount': None,
            'due_date': None,
            'biller': None,
            'subject': subject
        }
        
        # Extract amount
        amount_patterns = [
            r'(?:amount|total|due).*?Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
            r'Rs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)',
        ]
        
        for pattern in amount_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                bill['amount'] = float(amount_str)
                break
        
        # Extract due date
        date_patterns = [
            r'due\s+(?:date|on)?\s*:?\s*(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
            r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                bill['due_date'] = match.group(1)
                break
        
        # Extract biller from subject
        bill['biller'] = subject.split()[0] if subject else 'Unknown'
        
        return bill
    
    def _parse_transaction_email(self, subject: str, body: str) -> Optional[Dict[str, Any]]:
        """Parse transaction notification email"""
        # Similar to SMS parsing
        return {
            'type': 'transaction',
            'subject': subject,
            'parsed': False  # Placeholder
        }


class OCRReceiptParser:
    """Parse receipt images using OCR"""
    
    def __init__(self):
        self.amount_patterns = [
            r'total.*?(\d+(?:\.\d+)?)',
            r'amount.*?(\d+(?:\.\d+)?)',
            r'₹\s*(\d+(?:\.\d+)?)',
            r'rs\.?\s*(\d+(?:\.\d+)?)',
        ]
    
    def parse_receipt_text(self, ocr_text: str) -> Dict[str, Any]:
        """Parse OCR text from receipt"""
        receipt = {
            'amount': None,
            'merchant': None,
            'items': [],
            'date': None,
            'category': 'shopping'
        }
        
        lines = ocr_text.split('\n')
        
        # Extract merchant (usually first line)
        if lines:
            receipt['merchant'] = lines[0].strip()
        
        # Extract amount
        for pattern in self.amount_patterns:
            match = re.search(pattern, ocr_text, re.IGNORECASE)
            if match:
                receipt['amount'] = float(match.group(1))
                break
        
        # Extract date
        date_pattern = r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})'
        match = re.search(date_pattern, ocr_text)
        if match:
            receipt['date'] = match.group(1)
        
        # Extract items (lines with prices)
        for line in lines:
            if re.search(r'\d+(?:\.\d+)?', line):
                receipt['items'].append(line.strip())
        
        return receipt
    
    def parse_receipt_image(self, image_path: str) -> Dict[str, Any]:
        """
        Parse receipt from image file
        Note: Requires OCR library like pytesseract or cloud OCR API
        """
        # Placeholder - would integrate with OCR service
        return {
            'status': 'pending',
            'message': 'OCR processing required - integrate pytesseract or Google Vision API',
            'image_path': image_path
        }


class TransactionCategorizer:
    """Automatically categorize transactions"""
    
    def __init__(self):
        self.category_keywords = {
            'food': ['restaurant', 'cafe', 'swiggy', 'zomato', 'food', 'dominos', 'mcdonald', 'kfc', 'pizza'],
            'transport': ['uber', 'ola', 'rapido', 'petrol', 'fuel', 'parking', 'metro', 'bus', 'taxi'],
            'shopping': ['amazon', 'flipkart', 'myntra', 'ajio', 'mall', 'store', 'shop'],
            'utilities': ['electricity', 'water', 'gas', 'internet', 'broadband', 'mobile', 'recharge'],
            'entertainment': ['netflix', 'prime', 'hotstar', 'spotify', 'movie', 'cinema', 'bookmyshow'],
            'health': ['pharmacy', 'hospital', 'doctor', 'clinic', 'medicine', 'apollo', 'medplus'],
            'education': ['school', 'college', 'course', 'udemy', 'coursera', 'books'],
            'bills': ['bill', 'payment', 'emi', 'loan', 'insurance'],
            'investment': ['mutual fund', 'sip', 'stock', 'zerodha', 'groww', 'upstox'],
            'transfer': ['transfer', 'upi', 'neft', 'imps', 'rtgs'],
        }
    
    def categorize(self, merchant: str, amount: float = None) -> str:
        """Categorize transaction based on merchant name"""
        if not merchant:
            return 'other'
        
        merchant_lower = merchant.lower()
        
        # Check keywords
        for category, keywords in self.category_keywords.items():
            if any(keyword in merchant_lower for keyword in keywords):
                return category
        
        # Amount-based heuristics
        if amount:
            if amount > 10000:
                return 'bills'  # Likely rent or large bill
            elif amount < 50:
                return 'food'  # Likely small purchase
        
        return 'other'
    
    def categorize_bulk(self, transactions: List[Dict]) -> List[Dict]:
        """Categorize multiple transactions"""
        for txn in transactions:
            merchant = txn.get('merchant', '')
            amount = txn.get('amount', 0)
            txn['category'] = self.categorize(merchant, amount)
        return transactions


class SmartTransactionDetector:
    """Unified transaction detection from multiple sources"""
    
    def __init__(self):
        self.sms_parser = SMSParser()
        self.email_parser = EmailParser()
        self.ocr_parser = OCRReceiptParser()
        self.categorizer = TransactionCategorizer()
    
    def process_sms(self, message: str) -> Optional[Dict]:
        """Process SMS and categorize"""
        txn = self.sms_parser.parse_sms(message)
        if txn:
            txn['source'] = 'sms'
            txn['category'] = self.categorizer.categorize(txn.get('merchant'), txn.get('amount'))
        return txn
    
    def process_email(self, subject: str, body: str) -> Optional[Dict]:
        """Process email and categorize"""
        result = self.email_parser.parse_email(subject, body)
        if result:
            result['source'] = 'email'
        return result
    
    def process_receipt(self, ocr_text: str) -> Dict:
        """Process receipt OCR text"""
        receipt = self.ocr_parser.parse_receipt_text(ocr_text)
        receipt['source'] = 'receipt'
        receipt['category'] = self.categorizer.categorize(receipt.get('merchant'), receipt.get('amount'))
        return receipt
    
    def get_transaction_insights(self, transactions: List[Dict]) -> Dict:
        """Analyze transactions and provide insights"""
        if not transactions:
            return {'message': 'No transactions to analyze'}
        
        total_spent = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'debit')
        total_received = sum(t.get('amount', 0) for t in transactions if t.get('type') == 'credit')
        
        # Category breakdown
        category_spending = {}
        for txn in transactions:
            if txn.get('type') == 'debit':
                cat = txn.get('category', 'other')
                category_spending[cat] = category_spending.get(cat, 0) + txn.get('amount', 0)
        
        # Top merchant
        merchant_spending = {}
        for txn in transactions:
            if txn.get('type') == 'debit' and txn.get('merchant'):
                merch = txn['merchant']
                merchant_spending[merch] = merchant_spending.get(merch, 0) + txn.get('amount', 0)
        
        top_merchant = max(merchant_spending.items(), key=lambda x: x[1]) if merchant_spending else ('None', 0)
        
        return {
            'total_transactions': len(transactions),
            'total_spent': total_spent,
            'total_received': total_received,
            'net_cashflow': total_received - total_spent,
            'category_breakdown': category_spending,
            'top_merchant': {'name': top_merchant[0], 'amount': top_merchant[1]},
            'average_transaction': total_spent / len([t for t in transactions if t.get('type') == 'debit']) if transactions else 0
        }
