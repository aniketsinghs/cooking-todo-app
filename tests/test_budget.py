"""Unit tests for the budget analysis service.

Tests cover budget calculation, cost tier classification,
and savings tip generation for various scenarios.
"""

import pytest

from models.schemas import BudgetBreakdown, GroceryItem
from services.budget_service import analyze_budget, get_cost_tier


class TestGetCostTier:
    """Tests for the get_cost_tier function."""

    def test_budget_tier_low_cost(self) -> None:
        """Costs below ₹300 should be classified as 'budget'."""
        assert get_cost_tier(100.0) == "budget"

    def test_budget_tier_zero(self) -> None:
        """Zero cost should be classified as 'budget'."""
        assert get_cost_tier(0.0) == "budget"

    def test_moderate_tier(self) -> None:
        """Costs between ₹300 and ₹800 should be 'moderate'."""
        assert get_cost_tier(500.0) == "moderate"

    def test_moderate_tier_boundary(self) -> None:
        """Exactly ₹300 should be 'moderate'."""
        assert get_cost_tier(300.0) == "moderate"

    def test_premium_tier(self) -> None:
        """Costs ₹800 and above should be 'premium'."""
        assert get_cost_tier(1000.0) == "premium"

    def test_premium_tier_boundary(self) -> None:
        """Exactly ₹800 should be 'premium'."""
        assert get_cost_tier(800.0) == "premium"


class TestAnalyzeBudget:
    """Tests for the analyze_budget function."""

    @pytest.fixture
    def sample_grocery_items(self) -> list[GroceryItem]:
        """Create a sample grocery list for testing."""
        return [
            GroceryItem(name="Rice", quantity="1 kg", estimated_cost=60.0, category="grains"),
            GroceryItem(name="Chicken", quantity="500g", estimated_cost=180.0, category="protein"),
            GroceryItem(name="Vegetables", quantity="1 kg", estimated_cost=80.0, category="produce"),
        ]

    def test_within_budget(self, sample_grocery_items: list[GroceryItem]) -> None:
        """When total cost is within budget, is_within_budget should be True."""
        result: BudgetBreakdown = analyze_budget(
            grocery_items=sample_grocery_items,
            budget=500.0,
            num_people=2,
        )
        assert result.is_within_budget is True
        assert result.total_estimated_cost == 320.0
        assert result.budget == 500.0

    def test_over_budget(self, sample_grocery_items: list[GroceryItem]) -> None:
        """When total cost exceeds budget, is_within_budget should be False."""
        result: BudgetBreakdown = analyze_budget(
            grocery_items=sample_grocery_items,
            budget=200.0,
            num_people=2,
        )
        assert result.is_within_budget is False
        assert len(result.savings_tips) > 0

    def test_exact_budget(self, sample_grocery_items: list[GroceryItem]) -> None:
        """When total cost equals budget exactly, should be within budget."""
        result: BudgetBreakdown = analyze_budget(
            grocery_items=sample_grocery_items,
            budget=320.0,
            num_people=2,
        )
        assert result.is_within_budget is True

    def test_empty_grocery_list(self) -> None:
        """An empty grocery list should have zero total cost."""
        result: BudgetBreakdown = analyze_budget(
            grocery_items=[],
            budget=500.0,
            num_people=2,
        )
        assert result.total_estimated_cost == 0.0
        assert result.is_within_budget is True

    def test_large_group_savings_tips(self, sample_grocery_items: list[GroceryItem]) -> None:
        """Over-budget plans for 4+ people should suggest bulk buying."""
        result: BudgetBreakdown = analyze_budget(
            grocery_items=sample_grocery_items,
            budget=100.0,
            num_people=5,
        )
        bulk_tips = [tip for tip in result.savings_tips if "bulk" in tip.lower()]
        assert len(bulk_tips) > 0

    def test_under_budget_message(self, sample_grocery_items: list[GroceryItem]) -> None:
        """When under budget, savings tips should include positive message."""
        result: BudgetBreakdown = analyze_budget(
            grocery_items=sample_grocery_items,
            budget=1000.0,
            num_people=2,
        )
        assert any("under budget" in tip.lower() for tip in result.savings_tips)
