# 🧪 Trello API Test Automation Framework (Pytest)

A Python-based API testing framework built with **pytest** to validate Trello's REST API.

This project demonstrates real-world QA automation practices by combining:
- Factory-based test setup
- Parametrized negative testing
- End-to-end workflow validation
- Clean debugging and logging

---

## 🚀 Features

- ✅ Full CRUD testing for Trello resources (Boards, Lists, Cards)
- ✅ Factory-based test data creation (board_factory, list_factory, card_factory)
- ✅ Parametrized negative tests (invalid/missing auth)
- ✅ Structured validation approach:
  - Structure
  - Schema
  - Data Integrity
  - Business Rules
- ✅ End-to-end workflow test:
  - Create → Update → Move → Delete card
- ✅ Debug helpers with safe credential handling

---

## 🛠 Tech Stack

- Python
- Pytest
- Requests
- Trello REST API

---

## ⚙️ Setup

### 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git  
cd YOUR_REPO  

### 2. Install dependencies
pip install -r requirements.txt  

### 3. Add your Trello credentials

Create a `config.py` file:

TRELLO_KEY = "your_key"  
TRELLO_TOKEN = "your_token"  
BASE_URL = "https://api.trello.com/1"  

---

## ▶️ Running Tests

Run all tests:  
pytest -v  

Run with debug output:  
pytest -v -s  

---

## 🧪 Test Coverage

### Positive Tests

- Create Board / List / Card
- Validate response structure and schema
- Verify data integrity
- Validate business rules (default states, relationships)

### Negative Tests

- Missing token/key
- Invalid token/key
- Invalid list IDs

### Workflow Test

End-to-end scenario:

1. Create board  
2. Create lists (To Do / Done)  
3. Create card with description  
4. Update description  
5. Move card between lists  
6. Delete card  
7. Validate deletion  

---

## 💡 Key Design Decisions

### Factory Pattern

Reusable fixtures generate test data dynamically:

board_factory()  
list_factory()  
card_factory()  

---

### Parametrized Testing

Used to efficiently test multiple failure scenarios.

---

### Debug Strategy

Custom debug helpers provide structured output without exposing secrets.

---

## 📌 Future Improvements

- Add schema validation with JSON Schema  
- Integrate CI/CD (GitHub Actions)  
- Add HTML reporting (pytest-html or Allure)  
- Expand negative test coverage  

---

## 🎯 Purpose

This project demonstrates:

- Real-world API testing strategies  
- Strong understanding of test design principles  
- Translation of Postman testing into automated frameworks  
- Clean, maintainable test architecture  

---

## 🔗 Author

Tomas Amaya