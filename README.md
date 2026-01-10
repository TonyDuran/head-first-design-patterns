# head-first-design-patterns
Design Pattern Examples to Reinforce concepts

## 📚 Overview

This repository contains **AI-generated interactive web applications** demonstrating various design patterns from the Head First Design Patterns book. Each pattern has its own self-contained folder with a complete example implementation, showing both the **correct usage** (GOOD) and **anti-patterns** (BAD) for educational comparison.

These examples are designed to **supplement and reinforce** the patterns you learn from the book through hands-on, interactive demonstrations.

### 📖 Based On

**Head First Design Patterns** (2nd Edition)
- **Authors:** Eric Freeman, Elisabeth Robson, Bert Bates, Kathy Sierra
- **ISBN:** 9781492077992
- **Publisher:** O'Reilly Media
- **Link:** [O'Reilly Learning Platform](https://learning.oreilly.com/library/view/head-first-design/9781492077992/)

**Note:** These examples are **AI-generated implementations** created to help you practice and understand the patterns in action. They complement the book by providing interactive, runnable code for the design patterns discussed.

## 🎯 Design Patterns

### 1. Strategy Pattern
📁 **Folder:** `strategy-pattern/`

**What it demonstrates:** The Strategy Pattern with a payment processing system in an e-commerce store.

**Technologies:** FastAPI (Python) + Vue.js 3 + Docker

**Key Features:**
- Multiple payment strategies (Credit Card, PayPal, Bitcoin)
- Interactive comparison between good and bad implementations
- Live web application with product catalog and checkout
- Dynamic payment method registration at runtime
- Educational tooltips and pattern explanations
- Pre-filled forms to save testing time

**Learn more:** See [strategy-pattern/README.md](strategy-pattern/README.md) for:
- Detailed explanation of the pattern
- Code snippets showing GOOD vs BAD implementations
- How to run the example
- Educational features and interactive demo

**Run it:**
```bash
cd strategy-pattern
./run.sh
# Or using Docker:
docker-compose up
```

---

## 🚀 Quick Start

Each pattern folder is self-contained and can be run independently:

1. Navigate to the pattern folder
2. Follow the README instructions
3. Most examples can run with Docker or locally

## 🛠️ Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** Vue.js 3
- **Containerization:** Docker
- **Documentation:** Markdown with interactive examples

## 📖 Learning Approach

Each example includes:
- ✅ **GOOD implementation** - Proper use of the pattern
- ❌ **BAD implementation** - Anti-pattern for comparison
- 📝 **Detailed explanations** - When to use and when to avoid
- 🎮 **Interactive demos** - Learn by doing
- 🧪 **Working code** - Real, runnable examples

## 🤝 Contributing

This is an educational project. Contributions are welcome:
- Add more design patterns
- Improve existing examples
- Enhance documentation
- Fix bugs

## 📚 Resources

- **Head First Design Patterns (2nd Edition)** - O'Reilly Media - [ISBN: 9781492077992](https://learning.oreilly.com/library/view/head-first-design/9781492077992/)
- [Refactoring Guru - Design Patterns](https://refactoring.guru/design-patterns)
- [Design Patterns on Wikipedia](https://en.wikipedia.org/wiki/Design_Patterns)

## 💡 How to Use This Repository

1. **Read the book**: Study the design patterns in Head First Design Patterns
2. **Explore examples**: Clone this repo and explore the interactive implementations
3. **Run the code**: Try running the examples with the provided instructions
4. **Experiment**: Modify the examples to deepen your understanding
5. **Compare**: Look at both GOOD and BAD implementations to understand trade-offs

## ⚠️ Disclaimer

These code examples are **AI-generated** and created as educational supplements to the Head First Design Patterns book. While they demonstrate the core concepts correctly, they should be:
- Used for learning purposes
- Reviewed before use in production
- Combined with the detailed explanations in the original book
- Adapted to your specific needs and coding standards

The patterns themselves are from the seminal design patterns work, but the implementations here are new examples created specifically for interactive learning.

## 📝 License

Educational use - These are curated examples to help learn design patterns from Head First Design Patterns.
