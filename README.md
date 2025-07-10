# 🧪 Cart Offer System – Automated Test Suite

This repository contains a robust, scalable, and backend-agnostic test automation suite for a **Zomato-like Cart Offer System**. It validates the correct application of **FLATX** and **FLAT%** offers based on user segments, cart value, and restaurant mappings.

---

## 📦 Project Structure

```
.
├── README.md
├── config.yaml
├── conftest.py
├── library
│   ├── __init__.py
│   ├── api_client.py
│   ├── mockserver.py
│   ├── services
│   │   ├── __init__.py
│   │   └── cart_offer_services.py
│   └── util.py
├── pytest.ini
├── requirements.txt
└── tests
    ├── test_business_logic_validation.py
    ├── test_contract_validation.py
    └── test_discount_logic.py
---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/your-org/cart-offer-tests.git
cd cart-offer-tests
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Copy and update the `.local.env` with correct base URL and other credentials:

> You can also override config in `config.yaml` for reusable test constants.

## 🧪 Running Tests

### Run all tests

```bash
pytest --alluredir=reports/
```

### Run a specific suite

```bash
pytest tests/test_cart_offer_flat.py
```

### Run with environment

```bash
pytest --alluredir=allure-report --envfile=.local.env
```

---

## 📊 Allure Report

Generate and open an Allure HTML report:

```bash
 allure serve --host 0.0.0.0
```

## ⚙️ Features

- ✅ Backend-agnostic: Works for both Java Spring Boot and FastAPI
- ✅ Pytest-based with clean parameterization
- ✅ Allure integration with titles, features, and dynamic reporting
- ✅ Segment mocking using `MockServer`
- ✅ Supports command-line execution for CI/CD pipelines