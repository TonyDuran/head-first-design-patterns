# head-first-design-patterns
Design Pattern Examples to Reinforce concepts

## 📚 Overview

This repository contains interactive web applications demonstrating various design patterns. Each pattern has its own self-contained folder with a complete example implementation, showing both the **correct usage** (GOOD) and **anti-patterns** (BAD) for educational comparison.

## 🎯 Design Patterns

### 1. Strategy Pattern
📁 **Folder:** `strategy-pattern/`

**What it demonstrates:** The Strategy Pattern with a payment processing system in an e-commerce store.

**Technologies:** FastAPI (Python) + Vue.js + Docker

**Key Features:**
- Multiple payment strategies (Credit Card, PayPal, Bitcoin)
- Interactive comparison between good and bad implementations
- Live web application with product catalog and checkout
- Educational tooltips and pattern explanations

**Run it:**
```bash
cd strategy-pattern
./run.sh
# Or using Docker:
docker-compose up
```

**Learn more:** See [strategy-pattern/README.md](strategy-pattern/README.md)

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

- [Head First Design Patterns Book](https://www.oreilly.com/library/view/head-first-design/0596007124/)
- [Refactoring Guru](https://refactoring.guru/design-patterns)
- [Design Patterns on Wikipedia](https://en.wikipedia.org/wiki/Design_Patterns)

## 📝 License

Educational use - See individual pattern folders for details.
