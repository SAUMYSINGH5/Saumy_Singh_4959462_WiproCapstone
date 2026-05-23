# BDD BestBuy — Selenium Automation Framework

A Behavior-Driven Development (BDD) test automation framework for [BestBuy.com](https://www.bestbuy.com), built with Python, Behave, and Selenium WebDriver. Tests cover the **Deal of the Day** feature, including full end-to-end checkout flows, and generate rich Allure reports with screenshots.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Scenarios](#test-scenarios)
- [Reports](#reports)
- [Logging](#logging)

---

## Project Structure

```
BDD_BestBuy/
├── behave.ini                  # Behave runner configuration (Allure formatter)
├── config/
│   └── config.ini              # Base URL and browser settings
├── data/
│   └── test_data.csv           # Test data (valid/invalid emails)
├── features/
│   ├── deal_of_day.feature     # Positive & negative functional scenarios
│   ├── end_to_end.feature      # End-to-end checkout scenarios
│   ├── environment.py          # Hooks (browser setup/teardown, Allure attachments)
│   └── steps/
│       └── deal_of_day_steps.py  # Step definitions
├── locators/
│   └── bestbuy_locators.py     # Centralised element locators
├── logs/
│   └── automation.log          # Runtime logs
├── pages/
│   ├── base_page.py            # Base page with shared WebDriver utilities
│   ├── home_page.py            # Home page actions
│   ├── deal_of_day_page.py     # Deal of the Day page actions
│   ├── product_page.py         # Product detail page actions
│   ├── cart_page.py            # Cart page actions
│   └── checkout_page.py        # Checkout page actions
└── reports/
    └── allure-report/          # Generated Allure HTML report
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Primary language |
| Selenium 4.x | Browser automation |
| Behave | BDD test runner (Gherkin syntax) |
| Allure-Behave | Rich HTML reporting |
| python-dotenv | Environment variable management |
| WebDriver Manager | Auto-manages ChromeDriver |

---

## Prerequisites

- Python 3.11+
- Google Chrome browser
- [Allure CLI](https://allurereport.org/docs/install/) (for viewing reports)

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd BDD_BestBuy
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

Edit `config/config.ini` to change the target URL or browser:

```ini
[common info]
base_url = https://www.bestbuy.com
browser  = chrome
```

Test data (valid/invalid email addresses) is stored in `data/test_data.csv`.

---

## Running Tests

Run the full test suite:
```bash
behave
```

Run tests by tag:
```bash
behave --tags=smoke          # Smoke tests only
behave --tags=positive       # All positive scenarios
behave --tags=negative       # All negative scenarios
behave --tags=e2e            # End-to-end scenarios
```

Run a specific feature file:
```bash
behave features/deal_of_day.feature
```

---

## Test Scenarios

### Deal of the Day — Functional Tests (`deal_of_day.feature`)

| ID | Tag | Description |
|---|---|---|
| TC01 | `@positive @smoke` | Open Deal of the Day page |
| TC02 | `@positive` | Select the first product from the deal list |
| TC03 | `@positive` | Add a deal product to the cart |
| TC04 | `@positive` | Proceed to checkout from the cart |
| TC05 | `@negative` | Checkout rejects an invalid email address |
| TC06 | `@negative` | Cart is empty when no product has been added |

### End-to-End Tests (`end_to_end.feature`)

| ID | Tag | Description |
|---|---|---|
| TC07 | `@e2e` | Full flow: Deal of the Day → Add to Cart → Checkout with valid email |



