"""
FastAPI application for Strategy Pattern demonstration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from payment_strategies import (
    ShoppingCart,
    BadShoppingCart,
    CreditCardPayment,
    PayPalPayment,
    BitcoinPayment
)

app = FastAPI(
    title="Strategy Pattern Demo - Payment System",
    description="Demonstrates the Strategy Pattern with different payment methods",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo purposes
carts: Dict[str, ShoppingCart] = {}
bad_carts: Dict[str, BadShoppingCart] = {}


# Pydantic models for request/response
class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str
    image: str


class CartItem(BaseModel):
    name: str
    price: float
    quantity: int = 1


class CreditCardDetails(BaseModel):
    card_number: str
    card_holder: str
    cvv: str
    expiry: str


class PayPalDetails(BaseModel):
    email: str
    password: str


class BitcoinDetails(BaseModel):
    wallet_address: str


class PaymentRequest(BaseModel):
    cart_id: str
    payment_method: str
    credit_card: Optional[CreditCardDetails] = None
    paypal: Optional[PayPalDetails] = None
    bitcoin: Optional[BitcoinDetails] = None
    use_bad_example: bool = False


# Sample products
PRODUCTS = [
    Product(id=1, name="Laptop", price=999.99, description="High-performance laptop", image="💻"),
    Product(id=2, name="Smartphone", price=699.99, description="Latest smartphone", image="📱"),
    Product(id=3, name="Headphones", price=199.99, description="Noise-canceling headphones", image="🎧"),
    Product(id=4, name="Tablet", price=499.99, description="10-inch tablet", image="📱"),
    Product(id=5, name="Smartwatch", price=299.99, description="Fitness tracking smartwatch", image="⌚"),
    Product(id=6, name="Camera", price=799.99, description="Digital camera", image="📷"),
]


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Strategy Pattern Demo API",
        "description": "This API demonstrates the Strategy Pattern using different payment methods",
        "endpoints": {
            "products": "/products - Get available products",
            "cart": "/cart/{cart_id} - Manage shopping cart",
            "checkout": "/checkout - Process payment using Strategy Pattern"
        }
    }


@app.get("/products", response_model=List[Product])
async def get_products():
    """Get list of available products"""
    return PRODUCTS


@app.post("/cart/{cart_id}/add")
async def add_to_cart(cart_id: str, item: CartItem):
    """Add item to cart"""
    if cart_id not in carts:
        carts[cart_id] = ShoppingCart()
        bad_carts[cart_id] = BadShoppingCart()
    
    carts[cart_id].add_item(item.name, item.price, item.quantity)
    bad_carts[cart_id].add_item(item.name, item.price, item.quantity)
    
    return {
        "success": True,
        "message": f"Added {item.name} to cart",
        "total": carts[cart_id].get_total()
    }


@app.get("/cart/{cart_id}")
async def get_cart(cart_id: str):
    """Get cart contents"""
    if cart_id not in carts:
        return {
            "items": [],
            "total": 0.0
        }
    
    cart = carts[cart_id]
    return {
        "items": cart.items,
        "total": cart.get_total()
    }


@app.delete("/cart/{cart_id}")
async def clear_cart(cart_id: str):
    """Clear cart"""
    if cart_id in carts:
        carts[cart_id] = ShoppingCart()
        bad_carts[cart_id] = BadShoppingCart()
    
    return {"success": True, "message": "Cart cleared"}


@app.post("/checkout")
async def checkout(payment_request: PaymentRequest):
    """
    Process checkout using Strategy Pattern (GOOD example) or
    without it (BAD example) based on use_bad_example flag
    """
    cart_id = payment_request.cart_id
    
    if cart_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    # BAD EXAMPLE: Without Strategy Pattern
    if payment_request.use_bad_example:
        bad_cart = bad_carts[cart_id]
        payment_details = {}
        
        if payment_request.payment_method == "credit_card" and payment_request.credit_card:
            payment_details = {
                "card_number": payment_request.credit_card.card_number,
                "card_holder": payment_request.credit_card.card_holder,
                "cvv": payment_request.credit_card.cvv,
                "expiry": payment_request.credit_card.expiry
            }
        elif payment_request.payment_method == "paypal" and payment_request.paypal:
            payment_details = {
                "email": payment_request.paypal.email,
                "password": payment_request.paypal.password
            }
        elif payment_request.payment_method == "bitcoin" and payment_request.bitcoin:
            payment_details = {
                "wallet_address": payment_request.bitcoin.wallet_address
            }
        
        result = bad_cart.checkout(payment_request.payment_method, payment_details)
        result["pattern_used"] = "BAD - Without Strategy Pattern"
        result["problems"] = [
            "All payment logic in one method",
            "Hard to add new payment types",
            "Violates Open/Closed Principle",
            "Difficult to test individual payment methods"
        ]
        return result
    
    # GOOD EXAMPLE: With Strategy Pattern
    cart = carts[cart_id]
    
    # Select payment strategy based on request
    if payment_request.payment_method == "credit_card":
        if not payment_request.credit_card:
            raise HTTPException(status_code=400, detail="Credit card details required")
        strategy = CreditCardPayment(
            card_number=payment_request.credit_card.card_number,
            card_holder=payment_request.credit_card.card_holder,
            cvv=payment_request.credit_card.cvv,
            expiry=payment_request.credit_card.expiry
        )
    elif payment_request.payment_method == "paypal":
        if not payment_request.paypal:
            raise HTTPException(status_code=400, detail="PayPal details required")
        strategy = PayPalPayment(
            email=payment_request.paypal.email,
            password=payment_request.paypal.password
        )
    elif payment_request.payment_method == "bitcoin":
        if not payment_request.bitcoin:
            raise HTTPException(status_code=400, detail="Bitcoin details required")
        strategy = BitcoinPayment(
            wallet_address=payment_request.bitcoin.wallet_address
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unknown payment method: {payment_request.payment_method}")
    
    # Set strategy and checkout
    cart.set_payment_strategy(strategy)
    result = cart.checkout()
    
    result["pattern_used"] = "GOOD - With Strategy Pattern"
    result["benefits"] = [
        "Each payment method is encapsulated in its own class",
        "Easy to add new payment types without modifying existing code",
        "Follows Open/Closed Principle",
        "Easy to test individual payment strategies"
    ]
    
    return result


@app.get("/pattern-info")
async def pattern_info():
    """Get information about the Strategy Pattern"""
    return {
        "name": "Strategy Pattern",
        "category": "Behavioral Pattern",
        "intent": "Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it.",
        "structure": {
            "Strategy": "Common interface for all supported algorithms",
            "ConcreteStrategy": "Implements the algorithm using the Strategy interface",
            "Context": "Uses a Strategy object to execute the algorithm"
        },
        "pros": [
            "Open/Closed Principle - You can introduce new strategies without changing context",
            "Single Responsibility Principle - Isolate algorithm implementation from code that uses it",
            "Replace inheritance with composition",
            "Runtime flexibility - Switch algorithms at runtime"
        ],
        "cons": [
            "Clients must be aware of different strategies",
            "Increases number of objects in the application",
            "Modern languages may use functional programming features instead"
        ],
        "example": {
            "context": "ShoppingCart",
            "strategies": [
                "CreditCardPayment",
                "PayPalPayment",
                "BitcoinPayment"
            ],
            "use_case": "Different payment methods that can be selected at checkout"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
