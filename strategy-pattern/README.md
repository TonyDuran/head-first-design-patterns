# Strategy Pattern - Payment Processing Example

## 🎯 Overview

This example demonstrates the **Strategy Pattern**, a behavioral design pattern that lets you define a family of algorithms, encapsulate each one, and make them interchangeable. The Strategy pattern lets the algorithm vary independently from clients that use it.

**Real-World Example**: A shopping cart that supports multiple payment methods (Credit Card, PayPal, Bitcoin, Apple Pay, Google Pay, etc.)

## 🏗️ Pattern Structure

### Components

1. **Strategy Interface** (`PaymentStrategy`): Defines the common interface for all payment methods
2. **Concrete Strategies** (`CreditCardPayment`, `PayPalPayment`, `BitcoinPayment`, `DynamicPaymentStrategy`): Implement specific payment algorithms
3. **Context** (`ShoppingCart`): Uses a Strategy to execute the payment algorithm

## 📊 Good vs Bad Implementation

### ✅ GOOD: Using Strategy Pattern

**Location**: `backend/payment_strategies.py` (Lines 13-130)

```python
# Abstract Strategy Interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_payment_details(self) -> str:
        pass

# Concrete Strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, card_holder: str, cvv: str, expiry: str):
        self.card_number = card_number
        self.card_holder = card_holder
        self.cvv = cvv
        self.expiry = expiry

    def pay(self, amount: float) -> Dict[str, Any]:
        masked_card = f"****-****-****-{self.card_number[-4:]}"
        return {
            "success": True,
            "method": "Credit Card",
            "amount": amount,
            "transaction_id": f"CC-{datetime.now().timestamp()}",
            "details": f"Charged {masked_card}",
            "timestamp": datetime.now().isoformat()
        }

# Context uses Strategy
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy: PaymentStrategy = None

    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy

    def checkout(self) -> Dict[str, Any]:
        total = self.get_total()
        payment_result = self.payment_strategy.pay(total)
        return {**payment_result, "items": self.items, "total": total}
```

**Advantages**:
- ✅ **Encapsulation**: Each payment method in its own class
- ✅ **Open/Closed Principle**: Add new methods without modifying existing code
- ✅ **Single Responsibility**: One class per payment algorithm
- ✅ **Easy Testing**: Test each strategy independently
- ✅ **Runtime Flexibility**: Switch payment methods at runtime
- ✅ **No Conditional Logic**: Eliminates if/else chains

### ❌ BAD: Without Strategy Pattern (Anti-pattern)

**Location**: `backend/payment_strategies.py` (Lines 147-213)

```python
# Everything in ONE class with conditionals
class BadShoppingCart:
    def __init__(self):
        self.items = []

    def checkout(self, payment_type: str, payment_details: Dict[str, str]) -> Dict[str, Any]:
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
        # ... more elif statements for each payment type
        else:
            return {"success": False, "error": f"Unknown payment type: {payment_type}"}
```

**Problems**:
- ❌ **God Class**: All payment logic in one massive method
- ❌ **Violates Open/Closed**: Must modify class to add new payment types
- ❌ **Tight Coupling**: Payment logic tightly coupled to cart
- ❌ **Hard to Test**: Can't test payment methods in isolation
- ❌ **Complex Logic**: Large if/else or switch statements
- ❌ **Difficult Maintenance**: Changes to one payment affect the whole class
- ❌ **Code Duplication**: Similar logic repeated for each payment type

## 🚀 Running the Application

### Prerequisites

```bash
pip install -r requirements.txt
```

**Requirements**: FastAPI, Uvicorn, Python 3.7+

### Option 1: Using Docker (Recommended)

```bash
# Build the Docker image
docker build -t strategy-pattern-demo .

# Run the container
docker run -p 8000:8000 -p 8080:8080 strategy-pattern-demo

# Access the application
# Frontend: http://localhost:8080
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Using the Run Script

```bash
cd strategy-pattern
./run.sh

# Frontend: http://localhost:8080
# Backend API: http://localhost:8000
```

### Option 3: Running Locally

#### Backend (FastAPI)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the backend
cd backend
python main.py

# Backend will run on http://localhost:8000
```

#### Frontend (Vue.js)
```bash
# In a separate terminal, serve the frontend
cd frontend
python -m http.server 8080

# Access at http://localhost:8080
```

## 🎮 How to Use

1. **Browse Products**: View the 6 available products (Laptop, Smartphone, Headphones, Tablet, Smartwatch, Camera)
2. **Add to Cart**: Click "Add to Cart" on items you want to purchase
3. **Try the Live Demo**: Click the "Add New Payment Method" buttons (Apple Pay, Google Pay, Stripe, Square)
   - **GOOD Example**: Watch how new payment methods are added instantly at runtime!
   - **BAD Example**: See why it's impossible without modifying and restarting the server
4. **Select Payment Method**: Choose from Credit Card, PayPal, Bitcoin, or any dynamically added methods
5. **Enter Payment Details**: Form fields are pre-filled with fake data to save time
6. **Toggle Pattern Mode**: Check the box to compare GOOD vs BAD implementations side-by-side
7. **Checkout**: Click "Checkout Now" to process the payment
8. **View Results**: See transaction details and educational insights about the pattern

## 🏛️ Architecture

```
strategy-pattern/
├── backend/
│   ├── main.py                    # FastAPI application with REST endpoints
│   ├── payment_strategies.py      # Strategy Pattern implementation (GOOD & BAD)
│   └── __pycache__/               # Python cache
├── frontend/
│   ├── index.html                 # Vue.js single-page application
│   └── intro.html                 # Redirect to index.html
├── Dockerfile                     # Container configuration
├── docker-compose.yml             # Docker Compose setup
├── requirements.txt               # Python dependencies (FastAPI, Uvicorn)
├── run.sh                         # Convenient startup script
└── README.md                      # This file
```

## 🔌 API Endpoints

### Products & Cart
- `GET /` - API information and available endpoints
- `GET /products` - List all products
- `POST /cart/{cart_id}/add` - Add item to cart
- `GET /cart/{cart_id}` - Get cart contents
- `DELETE /cart/{cart_id}` - Clear cart
- `POST /checkout` - Process payment with selected strategy

### Educational Features
- `GET /available-payment-methods` - List available and registered payment methods
- `POST /add-payment-method` - Dynamically add a new payment method (shows pattern benefits)
- `GET /fake-data` - Get pre-filled test data for forms
- `GET /pattern-info` - Get detailed information about the Strategy Pattern

## 🎓 Educational Features

### Interactive Comparison
Toggle between implementations to see:
- **✅ GOOD Example**: Strategy Pattern with proper encapsulation
- **❌ BAD Example**: Without Strategy Pattern showing problems

### Live Pattern Demonstration
- **Add Payment Methods at Runtime**: Click buttons to add Apple Pay, Google Pay, Stripe, Square
  - GOOD: Works instantly, no server restart!
  - BAD: Requires code modification and server restart
- See the Open/Closed Principle in action
- Understand extensibility vs tight coupling

### Code Structure Demonstration
View in `backend/payment_strategies.py`:
- Abstract Strategy interface (lines 13-20)
- Concrete payment strategies (lines 23-119)
- Context class using strategies (lines 122-130)
- Anti-pattern comparison (lines 147-213)

### Educational UI
- Form fields auto-filled with fake data
- Pattern benefits/problems shown after transactions
- Side-by-side GOOD vs BAD comparison
- Inline explanations of why each approach matters

## 🛠️ Technologies Used

- **Backend**: FastAPI - Modern, fast, easy-to-use Python web framework
- **Frontend**: Vue.js 3 - Progressive JavaScript framework with reactive data binding
- **HTTP Client**: Axios - Promise-based HTTP client for API communication
- **Containerization**: Docker - Containerize the entire application
- **Server**: Uvicorn - ASGI web server for FastAPI
- **API Documentation**: Automatic Swagger/OpenAPI documentation at `/docs`

## 🎯 Key Takeaways

### When to Use Strategy Pattern
- Multiple algorithms for the same task
- Need to switch algorithms at runtime
- Want to isolate algorithm implementation
- Currently using conditional statements to select behavior
- Each algorithm is used in different contexts

### Benefits of Strategy Pattern
- Eliminates conditional statements
- Makes code more modular and maintainable
- Easier to add new algorithms/strategies
- Better code organization and testability
- Follows SOLID principles (Open/Closed, Single Responsibility)
- Enables runtime algorithm selection

### Trade-offs & When NOT to Use
- Increases number of classes
- Clients must be aware of different strategies
- Communication overhead between strategy and context
- Overkill for simple, rarely-changing algorithms
- Modern languages may use functions/lambdas instead

## 📖 Further Reading

- [Head First Design Patterns Book](https://www.oreilly.com/library/view/head-first-design/0596007124/)
- [Refactoring Guru - Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
- [Strategy Pattern - Wikipedia](https://en.wikipedia.org/wiki/Strategy_pattern)
- [SOLID Principles - Open/Closed Principle](https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle)

## 🤝 Contributing

This is an educational example. Feel free to:
- Add more payment strategies (Apple Pay, Google Pay, etc.)
- Enhance the UI and interactivity
- Add more educational features
- Improve documentation and code comments
- Add unit tests for each strategy

## 📝 License

Part of the Head First Design Patterns educational repository.

