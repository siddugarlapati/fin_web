"""
Security, encryption, and fraud detection
"""
import hashlib
import secrets
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import base64


class DataEncryption:
    """End-to-end encryption for sensitive data"""
    
    def __init__(self, master_key: Optional[str] = None):
        self.master_key = master_key or self._generate_key()
    
    def _generate_key(self) -> str:
        """Generate encryption key"""
        return secrets.token_hex(32)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        # Simple XOR encryption (use proper encryption in production like Fernet)
        key_bytes = self.master_key.encode()
        data_bytes = data.encode()
        
        encrypted = bytearray()
        for i, byte in enumerate(data_bytes):
            encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        
        return base64.b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt data"""
        encrypted_bytes = base64.b64decode(encrypted_data.encode())
        key_bytes = self.master_key.encode()
        
        decrypted = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
        
        return decrypted.decode()
    
    def hash_sensitive_field(self, data: str) -> str:
        """One-way hash for sensitive fields"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    def encrypt_transaction(self, transaction: Dict) -> Dict:
        """Encrypt sensitive transaction fields"""
        encrypted = transaction.copy()
        
        sensitive_fields = ['card_number', 'account_number', 'cvv', 'pin']
        
        for field in sensitive_fields:
            if field in encrypted:
                encrypted[field] = self.encrypt_data(str(encrypted[field]))
        
        return encrypted
    
    def decrypt_transaction(self, encrypted_transaction: Dict) -> Dict:
        """Decrypt transaction"""
        decrypted = encrypted_transaction.copy()
        
        sensitive_fields = ['card_number', 'account_number', 'cvv', 'pin']
        
        for field in sensitive_fields:
            if field in decrypted:
                decrypted[field] = self.decrypt_data(decrypted[field])
        
        return decrypted


class FraudDetector:
    """Detect fraudulent transactions"""
    
    def __init__(self):
        self.fraud_indicators = {
            'unusual_amount': 3.0,  # 3x average
            'unusual_location': True,
            'unusual_time': True,
            'rapid_transactions': 5,  # 5 transactions in 10 minutes
            'high_risk_merchant': True
        }
        
        self.high_risk_categories = ['gambling', 'crypto', 'international']
    
    def detect_fraud(self, transaction: Dict, user_profile: Dict) -> Dict[str, Any]:
        """Detect potential fraud in transaction"""
        fraud_score = 0
        alerts = []
        
        amount = transaction.get('amount', 0)
        category = transaction.get('category', '')
        merchant = transaction.get('merchant', '')
        timestamp = transaction.get('timestamp', datetime.now().isoformat())
        
        # Check unusual amount
        avg_transaction = user_profile.get('average_transaction', 1000)
        if amount > avg_transaction * self.fraud_indicators['unusual_amount']:
            fraud_score += 30
            alerts.append(f"Unusually large transaction: ₹{amount:.0f} (avg: ₹{avg_transaction:.0f})")
        
        # Check high-risk category
        if category in self.high_risk_categories:
            fraud_score += 20
            alerts.append(f"High-risk category: {category}")
        
        # Check rapid transactions
        recent_txns = user_profile.get('recent_transactions', [])
        if len(recent_txns) >= self.fraud_indicators['rapid_transactions']:
            fraud_score += 25
            alerts.append(f"Rapid transactions detected: {len(recent_txns)} in short time")
        
        # Check unusual time (late night)
        try:
            txn_time = datetime.fromisoformat(timestamp)
            if txn_time.hour < 6 or txn_time.hour > 23:
                fraud_score += 15
                alerts.append(f"Unusual transaction time: {txn_time.strftime('%I:%M %p')}")
        except:
            pass
        
        # Determine risk level
        if fraud_score >= 70:
            risk_level = 'high'
            action = 'block'
        elif fraud_score >= 40:
            risk_level = 'medium'
            action = 'verify'
        else:
            risk_level = 'low'
            action = 'allow'
        
        return {
            'fraud_score': fraud_score,
            'risk_level': risk_level,
            'recommended_action': action,
            'alerts': alerts,
            'is_suspicious': fraud_score >= 40,
            'requires_verification': fraud_score >= 40
        }
    
    def analyze_spending_pattern(self, transactions: List[Dict]) -> Dict[str, Any]:
        """Analyze spending patterns for anomalies"""
        if not transactions:
            return {'status': 'insufficient_data'}
        
        amounts = [t.get('amount', 0) for t in transactions]
        avg_amount = sum(amounts) / len(amounts)
        
        # Find outliers
        outliers = []
        for txn in transactions:
            amount = txn.get('amount', 0)
            if amount > avg_amount * 3:
                outliers.append({
                    'transaction': txn,
                    'deviation': round((amount / avg_amount), 2)
                })
        
        # Check for duplicate transactions
        duplicates = self._find_duplicates(transactions)
        
        return {
            'average_transaction': round(avg_amount, 2),
            'outliers': outliers,
            'outlier_count': len(outliers),
            'duplicates': duplicates,
            'duplicate_count': len(duplicates),
            'total_transactions': len(transactions),
            'anomaly_rate': round((len(outliers) + len(duplicates)) / len(transactions) * 100, 2)
        }
    
    def _find_duplicates(self, transactions: List[Dict]) -> List[Dict]:
        """Find potential duplicate transactions"""
        duplicates = []
        seen = {}
        
        for txn in transactions:
            key = f"{txn.get('amount')}_{txn.get('merchant')}_{txn.get('timestamp', '')[:10]}"
            if key in seen:
                duplicates.append({
                    'original': seen[key],
                    'duplicate': txn
                })
            else:
                seen[key] = txn
        
        return duplicates
    
    def check_merchant_reputation(self, merchant: str) -> Dict[str, Any]:
        """Check merchant reputation (placeholder)"""
        # In production, integrate with merchant reputation APIs
        suspicious_keywords = ['unknown', 'temp', 'test', 'fake']
        
        is_suspicious = any(keyword in merchant.lower() for keyword in suspicious_keywords)
        
        return {
            'merchant': merchant,
            'reputation_score': 50 if is_suspicious else 85,
            'is_verified': not is_suspicious,
            'risk_level': 'high' if is_suspicious else 'low'
        }


class AuthenticationManager:
    """Manage user authentication and sessions"""
    
    def __init__(self):
        self.sessions = {}
        self.failed_attempts = {}
        self.max_failed_attempts = 3
        self.lockout_duration = 30  # minutes
    
    def create_session(self, user_id: str) -> str:
        """Create new session"""
        session_token = secrets.token_urlsafe(32)
        self.sessions[session_token] = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=24)).isoformat(),
            'active': True
        }
        return session_token
    
    def validate_session(self, session_token: str) -> bool:
        """Validate session token"""
        if session_token not in self.sessions:
            return False
        
        session = self.sessions[session_token]
        
        # Check if expired
        expires_at = datetime.fromisoformat(session['expires_at'])
        if datetime.now() > expires_at:
            session['active'] = False
            return False
        
        return session['active']
    
    def revoke_session(self, session_token: str):
        """Revoke session"""
        if session_token in self.sessions:
            self.sessions[session_token]['active'] = False
    
    def record_failed_attempt(self, user_id: str):
        """Record failed login attempt"""
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = {
                'count': 0,
                'locked_until': None
            }
        
        self.failed_attempts[user_id]['count'] += 1
        
        if self.failed_attempts[user_id]['count'] >= self.max_failed_attempts:
            lockout_until = datetime.now() + timedelta(minutes=self.lockout_duration)
            self.failed_attempts[user_id]['locked_until'] = lockout_until.isoformat()
    
    def is_account_locked(self, user_id: str) -> bool:
        """Check if account is locked"""
        if user_id not in self.failed_attempts:
            return False
        
        locked_until = self.failed_attempts[user_id].get('locked_until')
        if not locked_until:
            return False
        
        return datetime.now() < datetime.fromisoformat(locked_until)
    
    def reset_failed_attempts(self, user_id: str):
        """Reset failed attempts after successful login"""
        if user_id in self.failed_attempts:
            self.failed_attempts[user_id] = {'count': 0, 'locked_until': None}


class DeviceManager:
    """Manage trusted devices"""
    
    def __init__(self):
        self.trusted_devices = {}
    
    def register_device(self, user_id: str, device_info: Dict) -> str:
        """Register new device"""
        device_id = secrets.token_hex(16)
        
        if user_id not in self.trusted_devices:
            self.trusted_devices[user_id] = {}
        
        self.trusted_devices[user_id][device_id] = {
            'device_name': device_info.get('name', 'Unknown'),
            'device_type': device_info.get('type', 'unknown'),
            'registered_at': datetime.now().isoformat(),
            'last_used': datetime.now().isoformat(),
            'trusted': False
        }
        
        return device_id
    
    def is_trusted_device(self, user_id: str, device_id: str) -> bool:
        """Check if device is trusted"""
        if user_id not in self.trusted_devices:
            return False
        
        if device_id not in self.trusted_devices[user_id]:
            return False
        
        return self.trusted_devices[user_id][device_id]['trusted']
    
    def trust_device(self, user_id: str, device_id: str):
        """Mark device as trusted"""
        if user_id in self.trusted_devices and device_id in self.trusted_devices[user_id]:
            self.trusted_devices[user_id][device_id]['trusted'] = True
    
    def get_user_devices(self, user_id: str) -> List[Dict]:
        """Get all user devices"""
        if user_id not in self.trusted_devices:
            return []
        
        return [
            {
                'device_id': did,
                **info
            }
            for did, info in self.trusted_devices[user_id].items()
        ]
    
    def revoke_device(self, user_id: str, device_id: str):
        """Revoke device access"""
        if user_id in self.trusted_devices and device_id in self.trusted_devices[user_id]:
            del self.trusted_devices[user_id][device_id]


class AuditLogger:
    """Log security events for audit"""
    
    def __init__(self):
        self.logs = []
    
    def log_event(self, event_type: str, user_id: str, details: Dict):
        """Log security event"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'details': details,
            'ip_address': details.get('ip_address', 'unknown')
        }
        
        self.logs.append(log_entry)
    
    def get_user_activity(self, user_id: str, days: int = 30) -> List[Dict]:
        """Get user activity logs"""
        cutoff = datetime.now() - timedelta(days=days)
        
        return [
            log for log in self.logs
            if log['user_id'] == user_id and datetime.fromisoformat(log['timestamp']) > cutoff
        ]
    
    def get_suspicious_activity(self) -> List[Dict]:
        """Get suspicious activity"""
        suspicious_events = ['failed_login', 'fraud_detected', 'unusual_transaction']
        
        return [
            log for log in self.logs
            if log['event_type'] in suspicious_events
        ]
    
    def export_logs(self, filename: str = 'audit_log.json'):
        """Export logs to file"""
        with open(filename, 'w') as f:
            json.dump(self.logs, f, indent=2)
