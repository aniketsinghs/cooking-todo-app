# 🧪 Testing Guide

This guide explains how to run, understand, and extend the test suite for the **AI Cooking To-Do List** app.

---

## 📋 Overview

The project includes **23 automated unit tests** organized into 2 test files:

| Test File | Tests | What It Covers |
|-----------|-------|----------------|
| `tests/test_budget.py` | 12 | Budget analysis, cost tiers, savings tips |
| `tests/test_schemas.py` | 11 | Pydantic model validation, input constraints |

**Test framework**: [pytest](https://docs.pytest.org/) — the most popular Python testing framework.

---

## 🚀 Running Tests

### Prerequisites

Make sure you have the project dependencies installed:

```bash
cd cooking-todo-app
pip install -r requirements.txt
pip install pytest
```

### Run All Tests

```bash
python -m pytest tests/ -v
```

The `-v` flag enables **verbose output**, showing each test name and its result.

### Expected Output

```
============================= test session starts ==============================
platform darwin -- Python 3.12.0, pytest-9.1.1
collecting ... collected 23 items

tests/test_budget.py::TestGetCostTier::test_budget_tier_low_cost PASSED  [  4%]
tests/test_budget.py::TestGetCostTier::test_budget_tier_zero PASSED      [  8%]
tests/test_budget.py::TestGetCostTier::test_moderate_tier PASSED         [ 13%]
tests/test_budget.py::TestGetCostTier::test_moderate_tier_boundary PASSED [ 17%]
tests/test_budget.py::TestGetCostTier::test_premium_tier PASSED          [ 21%]
tests/test_budget.py::TestGetCostTier::test_premium_tier_boundary PASSED [ 26%]
tests/test_budget.py::TestAnalyzeBudget::test_within_budget PASSED       [ 30%]
tests/test_budget.py::TestAnalyzeBudget::test_over_budget PASSED         [ 34%]
tests/test_budget.py::TestAnalyzeBudget::test_exact_budget PASSED        [ 39%]
tests/test_budget.py::TestAnalyzeBudget::test_empty_grocery_list PASSED  [ 43%]
tests/test_budget.py::TestAnalyzeBudget::test_large_group_savings_tips PASSED [ 47%]
tests/test_budget.py::TestAnalyzeBudget::test_under_budget_message PASSED [ 52%]
tests/test_schemas.py::TestMealPlanRequest::test_valid_request PASSED    [ 56%]
tests/test_schemas.py::TestMealPlanRequest::test_budget_must_be_positive PASSED [ 60%]
tests/test_schemas.py::TestMealPlanRequest::test_budget_negative_rejected PASSED [ 65%]
tests/test_schemas.py::TestMealPlanRequest::test_num_people_minimum PASSED [ 69%]
tests/test_schemas.py::TestMealPlanRequest::test_num_people_maximum PASSED [ 73%]
tests/test_schemas.py::TestMealPlanRequest::test_day_context_max_length PASSED [ 78%]
tests/test_schemas.py::TestMealPlanRequest::test_dietary_preferences_max_length PASSED [ 82%]
tests/test_schemas.py::TestGroceryItem::test_valid_item PASSED           [ 86%]
tests/test_schemas.py::TestGroceryItem::test_negative_cost_rejected PASSED [ 91%]
tests/test_schemas.py::TestMealPlanResponse::test_valid_full_response PASSED [ 95%]
tests/test_schemas.py::TestMealPlanResponse::test_empty_substitutions_allowed PASSED [100%]

============================== 23 passed in 0.07s ==============================
```

✅ **All 23 tests should pass.** If any test fails, check the error message for details.

---

## 📂 Test Files Explained

### `tests/test_budget.py` — Budget Service Tests

This file tests the budget analysis logic in `services/budget_service.py`.

#### `TestGetCostTier` (6 tests)

The `get_cost_tier()` function classifies a total grocery cost into spending tiers:

| Test | Input | Expected Output | What It Checks |
|------|-------|-----------------|----------------|
| `test_budget_tier_low_cost` | ₹100 | `"budget"` | Costs below ₹300 are "budget" |
| `test_budget_tier_zero` | ₹0 | `"budget"` | Zero cost edge case |
| `test_moderate_tier` | ₹500 | `"moderate"` | Mid-range costs |
| `test_moderate_tier_boundary` | ₹300 | `"moderate"` | Boundary: exactly ₹300 |
| `test_premium_tier` | ₹1000 | `"premium"` | High costs |
| `test_premium_tier_boundary` | ₹800 | `"premium"` | Boundary: exactly ₹800 |

#### `TestAnalyzeBudget` (6 tests)

The `analyze_budget()` function compares grocery costs against the user's budget:

| Test | Scenario | What It Checks |
|------|----------|----------------|
| `test_within_budget` | Total ₹320, Budget ₹500 | `is_within_budget` is `True`, amounts correct |
| `test_over_budget` | Total ₹320, Budget ₹200 | `is_within_budget` is `False`, savings tips present |
| `test_exact_budget` | Total = Budget (₹320) | Exactly on budget still counts as "within" |
| `test_empty_grocery_list` | No items | Zero cost, within budget |
| `test_large_group_savings_tips` | 5 people, over budget | Suggests bulk buying for large groups |
| `test_under_budget_message` | Total ₹320, Budget ₹1000 | Positive "under budget" message in tips |

---

### `tests/test_schemas.py` — Schema Validation Tests

This file tests the Pydantic models in `models/schemas.py` to ensure they properly validate and reject invalid inputs.

#### `TestMealPlanRequest` (7 tests)

| Test | What It Checks |
|------|----------------|
| `test_valid_request` | A complete, valid request creates successfully |
| `test_budget_must_be_positive` | Budget of `0` is rejected |
| `test_budget_negative_rejected` | Negative budget is rejected |
| `test_num_people_minimum` | `0` people is rejected (min is 1) |
| `test_num_people_maximum` | `21` people is rejected (max is 20) |
| `test_day_context_max_length` | >1000 characters is rejected |
| `test_dietary_preferences_max_length` | >500 characters is rejected |

#### `TestGroceryItem` (2 tests)

| Test | What It Checks |
|------|----------------|
| `test_valid_item` | A valid grocery item creates correctly |
| `test_negative_cost_rejected` | Negative `estimated_cost` is rejected |

#### `TestMealPlanResponse` (2 tests)

| Test | What It Checks |
|------|----------------|
| `test_valid_full_response` | Complete response with all fields works |
| `test_empty_substitutions_allowed` | Omitting substitutions uses empty list default |

---

## 🎯 Useful pytest Commands

### Run a specific test file

```bash
python -m pytest tests/test_budget.py -v
```

### Run a specific test class

```bash
python -m pytest tests/test_budget.py::TestGetCostTier -v
```

### Run a single test

```bash
python -m pytest tests/test_budget.py::TestGetCostTier::test_budget_tier_zero -v
```

### Show print/log output during tests

```bash
python -m pytest tests/ -v -s
```

### Run with short summary on failure

```bash
python -m pytest tests/ --tb=short
```

### Run and stop at first failure

```bash
python -m pytest tests/ -x
```

---

## 🔍 Manual Testing

In addition to automated tests, here's how to manually verify the app works correctly:

### 1. Start the App

```bash
python main.py
```

Open **http://localhost:8000** in your browser.

### 2. Test the Form

| Field | Test Value |
|-------|-----------|
| **Day context** | "Busy workday, need quick and healthy meals" |
| **Dietary preferences** | "vegetarian, no nuts" |
| **Budget** | 500 |
| **People** | 2 |

Click **"✨ Generate Meal Plan"** and verify:

- [ ] Three meal cards appear (breakfast, lunch, dinner)
- [ ] Each card shows dish name, description, prep time, and ingredients
- [ ] Grocery list table populates with items, quantities, costs, and categories
- [ ] Substitution cards are displayed
- [ ] Budget progress bar animates and shows correct percentage
- [ ] Savings tips are listed if applicable

### 3. Test Input Validation

Try these to verify the app handles bad input gracefully:

| Test | Expected |
|------|----------|
| Submit with empty "day context" | Error: "Please describe your day…" |
| Set budget to `0` | Error: "Please enter a valid budget…" |
| Set people to `0` | Error: "Number of people must be between 1 and 20" |
| Set people to `25` | Error: "Number of people must be between 1 and 20" |

### 4. Test Keyboard Shortcut

1. Fill in the form
2. Press `Ctrl+Enter` (or `Cmd+Enter` on Mac)
3. The form should submit automatically

### 5. Test the Health Endpoint

```bash
curl http://localhost:8000/api/health
```

Expected:
```json
{
  "status": "healthy",
  "service": "AI Cooking To-Do List",
  "timestamp": "2026-06-27T05:30:00+00:00"
}
```

### 6. Test the API Directly

```bash
curl -X POST http://localhost:8000/api/generate-meal-plan \
  -H "Content-Type: application/json" \
  -d '{
    "dietary_preferences": "vegetarian",
    "budget": 500,
    "num_people": 2,
    "day_context": "Work from home day"
  }'
```

### 7. Test Accessibility

- [ ] **Tab navigation**: All form fields and buttons are reachable via Tab key
- [ ] **Screen reader**: Labels and ARIA attributes are present on all interactive elements
- [ ] **Contrast**: Text is easily readable against the dark background
- [ ] **Responsive**: Resize the browser to mobile width — layout adapts correctly

---

## 🐛 Troubleshooting Test Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: No module named 'models'` | Running pytest from wrong directory | Run from the project root: `cd cooking-todo-app` |
| `ModuleNotFoundError: No module named 'pydantic'` | Dependencies not installed | Run `pip install -r requirements.txt` |
| `ImportError: cannot import name 'BudgetBreakdown'` | Schema file modified | Check `models/schemas.py` hasn't been changed |
| `AssertionError` on a specific test | Logic changed | Review the corresponding service/model for changes |

---

## ➕ Adding New Tests

To add a new test, follow this pattern:

```python
"""Describe what this test file covers."""

import pytest
from models.schemas import MealPlanRequest  # Import what you need


class TestYourFeature:
    """Group related tests in a class."""

    def test_descriptive_name(self) -> None:
        """One-line docstring explaining what this tests."""
        # Arrange
        request = MealPlanRequest(
            dietary_preferences="vegan",
            budget=300.0,
            num_people=1,
            day_context="Lazy Sunday",
        )

        # Act
        result = some_function(request)

        # Assert
        assert result.is_valid is True
```

### Tips for Writing Good Tests

1. **One assertion per test** — Each test should check one thing
2. **Descriptive names** — `test_budget_negative_rejected` is better than `test_budget_2`
3. **Use docstrings** — Explain *what* the test verifies, not *how*
4. **Test edge cases** — Zero values, max values, empty strings
5. **Use fixtures** — Share setup code with `@pytest.fixture`
6. **Type hints** — Add return type `-> None` to all test functions

---

*Happy testing! 🎉*
