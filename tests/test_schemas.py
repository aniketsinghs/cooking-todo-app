"""Unit tests for the Pydantic schema models.

Tests cover model validation, field constraints, and
proper rejection of invalid inputs.
"""

import pytest

from pydantic import ValidationError

from models.schemas import (
    BudgetBreakdown,
    GroceryItem,
    MealDetail,
    MealPlanRequest,
    MealPlanResponse,
    Substitution,
)


class TestMealPlanRequest:
    """Tests for the MealPlanRequest model validation."""

    def test_valid_request(self) -> None:
        """A fully valid request should be created without errors."""
        request = MealPlanRequest(
            day_type="Busy workday",
            diet="Vegetarian",
            cuisine="Indian",
            budget=500.0,
            num_people=2,
            ingredients_at_home="rice, dal",
        )
        assert request.diet == "Vegetarian"
        assert request.budget == 500.0
        assert request.num_people == 2

    def test_budget_must_be_positive(self) -> None:
        """Budget of zero or negative should be rejected."""
        with pytest.raises(ValidationError):
            MealPlanRequest(
                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=0,
                num_people=2,
            )

    def test_budget_negative_rejected(self) -> None:
        """Negative budget should be rejected."""
        with pytest.raises(ValidationError):
            MealPlanRequest(
                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=-100,
                num_people=2,
            )

    def test_num_people_minimum(self) -> None:
        """Number of people below 1 should be rejected."""
        with pytest.raises(ValidationError):
            MealPlanRequest(
                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=500,
                num_people=0,
            )

    def test_num_people_maximum(self) -> None:
        """Number of people above 20 should be rejected."""
        with pytest.raises(ValidationError):
            MealPlanRequest(
                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=500,
                num_people=21,
            )

    def test_ingredients_max_length(self) -> None:
        """Ingredients exceeding 1000 characters should be rejected."""
        with pytest.raises(ValidationError):
            MealPlanRequest(
                day_type="Busy workday",
                diet="Any",
                cuisine="Any",
                budget=500,
                num_people=2,
                ingredients_at_home="x" * 1001,
            )




class TestGroceryItem:
    """Tests for the GroceryItem model."""

    def test_valid_item(self) -> None:
        """A valid grocery item should be created successfully."""
        item = GroceryItem(
            name="Rice",
            quantity="1 kg",
            estimated_cost=60.0,
            category="grains",
        )
        assert item.name == "Rice"
        assert item.estimated_cost == 60.0

    def test_negative_cost_rejected(self) -> None:
        """Negative cost should be rejected."""
        with pytest.raises(ValidationError):
            GroceryItem(
                name="Rice",
                quantity="1 kg",
                estimated_cost=-10.0,
                category="grains",
            )


class TestMealPlanResponse:
    """Tests for the complete MealPlanResponse model."""

    def test_valid_full_response(self) -> None:
        """A fully populated response should be created successfully."""
        response = MealPlanResponse(
            meals=[
                MealDetail(
                    meal_type="breakfast",
                    dish_name="Oatmeal",
                    description="Simple oatmeal with honey",
                    prep_time_minutes=10,
                    ingredients=["oats", "milk", "honey"],
                )
            ],
            grocery_list=[
                GroceryItem(
                    name="Oats",
                    quantity="500g",
                    estimated_cost=80.0,
                    category="grains",
                )
            ],
            substitutions=[
                Substitution(
                    original="Honey",
                    substitute="Jaggery",
                    reason="More affordable and locally sourced",
                )
            ],
            budget_breakdown=BudgetBreakdown(
                total_estimated_cost=80.0,
                budget=500.0,
                is_within_budget=True,
                savings_tips=["Buy in bulk"],
            ),
        )
        assert len(response.meals) == 1
        assert response.meals[0].meal_type == "breakfast"
        assert response.budget_breakdown.is_within_budget is True

    def test_empty_substitutions_allowed(self) -> None:
        """Substitutions list can be empty (has default_factory)."""
        response = MealPlanResponse(
            meals=[
                MealDetail(
                    meal_type="lunch",
                    dish_name="Dal",
                    description="Yellow lentil dal",
                    prep_time_minutes=30,
                    ingredients=["lentils", "turmeric"],
                )
            ],
            grocery_list=[
                GroceryItem(
                    name="Lentils",
                    quantity="500g",
                    estimated_cost=70.0,
                    category="pulses",
                )
            ],
            budget_breakdown=BudgetBreakdown(
                total_estimated_cost=70.0,
                budget=500.0,
                is_within_budget=True,
            ),
        )
        assert response.substitutions == []
