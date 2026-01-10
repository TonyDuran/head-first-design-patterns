"""
Payment Strategy Pattern Implementation

This module demonstrates the Strategy Pattern with different payment methods.
The Strategy Pattern defines a family of algorithms, encapsulates each one,
and makes them interchangeable.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime


class PaymentStrategy(ABC):
    """Abstract base class for payment strategies (The Strategy Interface)"""
    
    @abstractmethod
    def pay(self, amount: float) -> Dict[str, Any]:
        """Process payment and return result"""
        pass
    
    @abstractmethod
    def get_payment_details(self) -> str:
        """Get human-readable payment method details"""
        pass


class CreditCardPayment(PaymentStrategy):
    """Concrete Strategy: Credit Card Payment"""
    
    def __init__(self, card_number: str, card_holder: str, cvv: str, expiry: str):
        self.card_number = card_number
        self.card_holder = card_holder
        self.cvv = cvv
        self.expiry = expiry
    
    def pay(self, amount: float) -> Dict[str, Any]:
        # Simulate payment processing
        masked_card = f"****-****-****-{self.card_number[-4:]}"
        return {
            "success": True,
            "method": "Credit Card",
            "amount": amount,
            "transaction_id": f"CC-{datetime.now().timestamp()}",
            "details": f"Charged {masked_card}",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_payment_details(self) -> str:
        masked_card = f"****-****-****-{self.card_number[-4:]}"
        return f"Credit Card ending in {self.card_number[-4:]}"


class PayPalPayment(PaymentStrategy):
    """Concrete Strategy: PayPal Payment"""
    
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    
    def pay(self, amount: float) -> Dict[str, Any]:
        # Simulate PayPal payment processing
        return {
            "success": True,
            "method": "PayPal",
            "amount": amount,
            "transaction_id": f"PP-{datetime.now().timestamp()}",
            "details": f"Charged PayPal account {self.email}",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_payment_details(self) -> str:
        return f"PayPal account {self.email}"


class BitcoinPayment(PaymentStrategy):
    """Concrete Strategy: Bitcoin Payment"""
    
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
    
    def pay(self, amount: float) -> Dict[str, Any]:
        # Simulate Bitcoin payment processing
        btc_amount = amount / 45000  # Fake conversion rate
        return {
            "success": True,
            "method": "Bitcoin",
            "amount": amount,
            "btc_amount": round(btc_amount, 8),
            "transaction_id": f"BTC-{datetime.now().timestamp()}",
            "details": f"Transferred {btc_amount:.8f} BTC to {self.wallet_address[:8]}...",
            "timestamp": datetime.now().isoformat()
        }
    
    def get_payment_details(self) -> str:
        return f"Bitcoin wallet {self.wallet_address[:8]}...{self.wallet_address[-4:]}"


class ShoppingCart:
    """Context class that uses a PaymentStrategy"""
    
    def __init__(self):
        self.items = []
        self.payment_strategy: PaymentStrategy = None
    
    def add_item(self, name: str, price: float, quantity: int = 1):
        """Add item to cart"""
        self.items.append({
            "name": name,
            "price": price,
            "quantity": quantity
        })
    
    def get_total(self) -> float:
        """Calculate total price"""
        return sum(item["price"] * item["quantity"] for item in self.items)
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        """Set the payment strategy (Strategy Pattern in action!)"""
        self.payment_strategy = strategy
    
    def checkout(self) -> Dict[str, Any]:
        """Process checkout using the selected payment strategy"""
        if not self.payment_strategy:
            return {
                "success": False,
                "error": "No payment method selected"
            }
        
        if not self.items:
            return {
                "success": False,
                "error": "Cart is empty"
            }
        
        total = self.get_total()
        payment_result = self.payment_strategy.pay(total)
        
        return {
            **payment_result,
            "items": self.items,
            "total": total
        }


# BAD EXAMPLE: Without Strategy Pattern (for comparison)
class BadShoppingCart:
    """
    This is a BAD example showing what happens WITHOUT the Strategy Pattern.
    
    Problems:
    1. Violates Open/Closed Principle - need to modify class to add new payment methods
    2. Tight coupling between cart and payment methods
    3. Hard to test individual payment methods
    4. Large, complex conditional logic
    """
    
    def __init__(self):
        self.items = []
    
    def add_item(self, name: str, price: float, quantity: int = 1):
        self.items.append({"name": name, "price": price, "quantity": quantity})
    
    def get_total(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items)
    
    def checkout(self, payment_type: str, payment_details: Dict[str, str]) -> Dict[str, Any]:
        """
        BAD: All payment logic in one method with if/else statements
        Adding new payment types requires modifying this method
        """
        if not self.items:
            return {"success": False, "error": "Cart is empty"}
        
        total = self.get_total()
        
        # BAD: Large conditional block for each payment type
        if payment_type == "credit_card":
            card_number = payment_details.get("card_number", "")
            masked_card = f"****-****-****-{card_number[-4:]}"
            return {
                "success": True,
                "method": "Credit Card",
                "amount": total,
                "transaction_id": f"CC-{datetime.now().timestamp()}",
                "details": f"Charged {masked_card}",
                "timestamp": datetime.now().isoformat()
            }
        elif payment_type == "paypal":
            email = payment_details.get("email", "")
            return {
                "success": True,
                "method": "PayPal",
                "amount": total,
                "transaction_id": f"PP-{datetime.now().timestamp()}",
                "details": f"Charged PayPal account {email}",
                "timestamp": datetime.now().isoformat()
            }
        elif payment_type == "bitcoin":
            wallet = payment_details.get("wallet_address", "")
            btc_amount = total / 45000
            return {
                "success": True,
                "method": "Bitcoin",
                "amount": total,
                "btc_amount": round(btc_amount, 8),
                "transaction_id": f"BTC-{datetime.now().timestamp()}",
                "details": f"Transferred {btc_amount:.8f} BTC",
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {"success": False, "error": f"Unknown payment type: {payment_type}"}
