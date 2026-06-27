"""Pydantic models for the AI Cooking To-Do List application.

This module defines all request and response schemas used throughout
the application, including meal plan requests, grocery items,
substitutions, and budget breakdowns.
"""

from pydantic import BaseModel, Field


class MealPlanRequest(BaseModel):
    """Request schema for generating a personalized meal plan.

    Contains user preferences, budget constraints, and contextual
    information to tailor the generated meal plan.
    """

    dietary_preferences: str = Field(
        ...,
        max_length=500,
        description="Dietary preferences or restrictions (e.g., 'vegetarian, gluten-free').",
    )
    budget: float = Field(
        ...,
        gt=0,
        description="Total budget for groceries in the user's local currency.",
    )
    num_people: int = Field(
        ...,
        ge=1,
        le=20,
        description="Number of people to plan meals for (1-20).",
    )
    day_context: str = Field(
        ...,
        max_length=1000,
        description="Context about the day to help tailor meals (e.g., 'busy workday, need quick meals').",
    )


class GroceryItem(BaseModel):
    """A single item on the generated grocery list.

    Represents an ingredient needed for the meal plan, including
    its quantity, estimated cost, and grocery store category.
    """

    name: str = Field(..., description="Name of the grocery item.")
    quantity: str = Field(
        ..., description="Quantity needed (e.g., '2 lbs', '500g', '1 dozen')."
    )
    estimated_cost: float = Field(
        ..., ge=0, description="Estimated cost of this item."
    )
    category: str = Field(
        ...,
        description="Grocery category (e.g., 'produce', 'dairy', 'grains').",
    )


class Substitution(BaseModel):
    """A suggested ingredient substitution.

    Provides an alternative ingredient when the original may be
    unavailable, too expensive, or unsuitable for dietary needs.
    """

    original: str = Field(..., description="The original ingredient.")
    substitute: str = Field(
        ..., description="The suggested substitute ingredient."
    )
    reason: str = Field(
        ...,
        description="Why this substitution is recommended (e.g., 'cheaper', 'allergen-free').",
    )


class MealDetail(BaseModel):
    """Details for a single meal in the plan.

    Contains the meal type, dish information, preparation time,
    and a list of required ingredients.
    """

    meal_type: str = Field(
        ...,
        description="Type of meal: 'breakfast', 'lunch', or 'dinner'.",
    )
    dish_name: str = Field(..., description="Name of the dish.")
    description: str = Field(
        ..., description="Brief description of the dish and how to prepare it."
    )
    prep_time_minutes: int = Field(
        ..., ge=0, description="Estimated preparation time in minutes."
    )
    ingredients: list[str] = Field(
        ..., description="List of ingredients required for this dish."
    )


class BudgetBreakdown(BaseModel):
    """Budget analysis for the generated meal plan.

    Compares the estimated grocery cost against the user's budget
    and provides actionable savings tips if over budget.
    """

    total_estimated_cost: float = Field(
        ..., ge=0, description="Total estimated cost of all grocery items."
    )
    budget: float = Field(..., gt=0, description="The user's stated budget.")
    is_within_budget: bool = Field(
        ...,
        description="Whether the total estimated cost is within the budget.",
    )
    savings_tips: list[str] = Field(
        default_factory=list,
        description="Tips to reduce costs if over budget.",
    )


class MealPlanResponse(BaseModel):
    """Complete response containing the generated meal plan.

    Aggregates meals for the day, a consolidated grocery list,
    ingredient substitutions, and a budget breakdown.
    """

    meals: list[MealDetail] = Field(
        ..., description="List of meals planned for the day."
    )
    grocery_list: list[GroceryItem] = Field(
        ..., description="Consolidated grocery list for all meals."
    )
    substitutions: list[Substitution] = Field(
        default_factory=list,
        description="Suggested ingredient substitutions.",
    )
    budget_breakdown: BudgetBreakdown = Field(
        ..., description="Budget analysis for the meal plan."
    )
