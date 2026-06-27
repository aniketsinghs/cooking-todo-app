"""Budget analysis service for the AI Cooking To-Do List application.

This module provides functions to analyze grocery costs against
the user's budget and generate actionable savings tips.
"""

from models.schemas import BudgetBreakdown, GroceryItem


def get_cost_tier(cost: float) -> str:
    """Classify a cost value into a spending tier.

    Args:
        cost: The total estimated cost to classify.

    Returns:
        A string tier label: 'budget', 'moderate', or 'premium'.
    """
    if cost < 300.0:
        return "budget"
    elif cost < 800.0:
        return "moderate"
    else:
        return "premium"


def _generate_savings_tips(
    total_cost: float,
    budget: float,
    num_people: int,
    grocery_items: list[GroceryItem],
) -> list[str]:
    """Generate contextual savings tips when the plan exceeds the budget.

    Tips are tailored based on how far over budget the plan is
    and the types of items in the grocery list.

    Args:
        total_cost: The total estimated grocery cost.
        budget: The user's stated budget.
        num_people: Number of people the plan serves.
        grocery_items: The list of grocery items for analysis.

    Returns:
        A list of actionable savings tip strings.
    """
    tips: list[str] = []
    overage: float = total_cost - budget
    overage_percent: float = (overage / budget) * 100 if budget > 0 else 0

    tips.append(
        f"You're \u20b9{overage:.2f} ({overage_percent:.0f}%) over budget. "
        "Consider the following adjustments."
    )

    # Suggest buying in bulk for larger groups
    if num_people >= 4:
        tips.append(
            "Buy staples like rice, pasta, and beans in bulk to save "
            "significantly for larger groups."
        )

    # Identify the most expensive items
    sorted_items: list[GroceryItem] = sorted(
        grocery_items, key=lambda item: item.estimated_cost, reverse=True
    )
    if sorted_items:
        most_expensive: GroceryItem = sorted_items[0]
        tips.append(
            f"Consider a cheaper alternative for '{most_expensive.name}' "
            f"(\u20b9{most_expensive.estimated_cost:.2f}) \u2014 it's the most "
            "expensive item on your list."
        )

    # General tips
    tips.append("Check for store-brand alternatives and weekly sales.")
    tips.append(
        "Buy seasonal produce — it's fresher and typically 20-40% cheaper."
    )

    if overage_percent > 30:
        tips.append(
            "Consider reducing the number of dishes or simplifying "
            "recipes to bring costs down significantly."
        )

    return tips


def analyze_budget(
    grocery_items: list[GroceryItem],
    budget: float,
    num_people: int,
) -> BudgetBreakdown:
    """Analyze the grocery list against the user's budget.

    Calculates the total estimated cost, determines whether the plan
    fits within budget, and generates savings tips if it does not.

    Args:
        grocery_items: The list of grocery items to analyze.
        budget: The user's total grocery budget.
        num_people: Number of people the meal plan serves.

    Returns:
        A BudgetBreakdown with cost analysis and optional savings tips.
    """
    total_estimated_cost: float = sum(
        item.estimated_cost for item in grocery_items
    )
    is_within_budget: bool = total_estimated_cost <= budget

    savings_tips: list[str] = []
    if not is_within_budget:
        savings_tips = _generate_savings_tips(
            total_cost=total_estimated_cost,
            budget=budget,
            num_people=num_people,
            grocery_items=grocery_items,
        )
    else:
        remaining: float = budget - total_estimated_cost
        savings_tips.append(
            f"Great news! You're \u20b9{remaining:.2f} under budget."
        )
        if remaining > budget * 0.3:
            savings_tips.append(
                "You have room to add a treat or upgrade an ingredient!"
            )

    return BudgetBreakdown(
        total_estimated_cost=round(total_estimated_cost, 2),
        budget=budget,
        is_within_budget=is_within_budget,
        savings_tips=savings_tips,
    )
