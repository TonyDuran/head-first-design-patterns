# Strategy Pattern - Payment Processing Example

## 🎯 Overview

This example demonstrates the **Strategy Pattern**, a behavioral design pattern that lets you define a family of algorithms, encapsulate each one, and make them interchangeable. The Strategy pattern lets the algorithm vary independently from clients that use it.

## 🏗️ Pattern Structure

### Components

1. **Strategy Interface** (`PaymentStrategy`): Defines the common interface for all payment methods
2. **Concrete Strategies** (`CreditCardPayment`, `PayPalPayment`, `BitcoinPayment`): Implement specific payment algorithms
3. **Context** (`ShoppingCart`): Uses a Strategy to execute the payment algorithm

## 📚 What You'll Learn

### ✅ Good Pattern Implementation
- **Encapsulation**: Each payment method is isolated in its own class
- **Open/Closed Principle**: Easy to add new payment types without modifying existing code
- **Single Responsibility**: Each class has one reason to change
- **Testability**: Easy to test each payment strategy independently
- **Runtime Flexibility**: Can switch payment methods at runtime

### ❌ Bad Pattern (Anti-pattern)
The example also shows a BAD implementation without the Strategy Pattern to highlight common problems:
- All payment logic crammed into one method with if/else statements
- Violates Open/Closed Principle (must modify code to add new payment types)
- Tight coupling between cart and payment logic
- Difficult to test individual payment methods
- Hard to maintain and extend

## 🚀 Running the Application

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

### Option 2: Running Locally

#### Backend (FastAPI)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the backend
cd backend
python main.py

# Or use uvicorn directly
uvicorn main:app --reload
```

#### Frontend (Vue)
```bash
# Serve the frontend (simple HTTP server)
cd frontend
python -m http.server 8080

# Access at http://localhost:8080
```

## 🎮 How to Use

1. **Browse Products**: View available products in the store
2. **Add to Cart**: Click "Add to Cart" on products you want to purchase
3. **Select Payment Method**: Choose from Credit Card, PayPal, or Bitcoin
4. **Enter Payment Details**: Fill in the required information for your chosen method
5. **Toggle Pattern Mode**: Check the box to see the BAD example (without Strategy Pattern)
6. **Checkout**: Click "Checkout Now" to process the payment
7. **View Results**: See the transaction details and pattern comparison

## 🏛️ Architecture

```
strategy-pattern/
├── backend/
│   ├── main.py                    # FastAPI application with REST endpoints
│   └── payment_strategies.py     # Strategy Pattern implementation
├── frontend/
│   └── index.html                 # Vue.js single-page application
├── Dockerfile                     # Container configuration
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🔌 API Endpoints

- `GET /` - API information
- `GET /products` - List all products
- `POST /cart/{cart_id}/add` - Add item to cart
- `GET /cart/{cart_id}` - Get cart contents
- `DELETE /cart/{cart_id}` - Clear cart
- `POST /checkout` - Process payment
- `GET /pattern-info` - Get Strategy Pattern information

## 🎓 Educational Features

### Interactive Comparison
The application allows you to toggle between:
- **GOOD Example**: Using Strategy Pattern with proper encapsulation
- **BAD Example**: Without Strategy Pattern using if/else conditionals

### Real-time Feedback
After checkout, the application shows:
- Transaction details
- Which pattern was used
- Benefits (Good) or Problems (Bad) of the approach
- Educational insights about the pattern

### Code Structure Demonstration
The backend code clearly shows:
- Abstract Strategy interface
- Multiple concrete strategy implementations
- Context class using strategies
- Anti-pattern comparison for learning

## 🎯 Key Takeaways

1. **When to Use Strategy Pattern**:
   - Multiple algorithms for a specific task
   - Need to switch algorithms at runtime
   - Want to isolate algorithm implementation details
   - Have conditional statements selecting behavior

2. **Benefits**:
   - Eliminates conditional statements
   - Makes code more maintainable
   - Easier to add new algorithms
   - Better testability
   - Follows SOLID principles

3. **Trade-offs**:
   - Increases number of classes
   - Clients must be aware of different strategies
   - Communication overhead between strategy and context

## 🛠️ Technologies Used

- **Backend**: FastAPI (Python) - Modern, fast web framework
- **Frontend**: Vue.js 3 - Progressive JavaScript framework
- **Containerization**: Docker - For easy deployment
- **API Documentation**: Automatic with FastAPI (Swagger/OpenAPI)

## 📖 Further Reading

- [Head First Design Patterns Book](https://www.oreilly.com/library/view/head-first-design/0596007124/)
- [Refactoring Guru - Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
- [Strategy Pattern - Wikipedia](https://en.wikipedia.org/wiki/Strategy_pattern)

## 🤝 Contributing

This is an educational example. Feel free to:
- Add more payment strategies
- Enhance the UI
- Add more educational features
- Improve documentation

## 📝 License

Part of the Head First Design Patterns educational repository.
