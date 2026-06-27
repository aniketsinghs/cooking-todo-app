"""Gemini AI service for generating personalized meal plans.

This module interfaces with the Google Gemini API to generate
structured meal plans based on user preferences, budget, and context.
"""

import json
import logging
import os
import re

from google import genai

from models.schemas import (
    BudgetBreakdown,
    GroceryItem,
    MealDetail,
    MealPlanRequest,
    MealPlanResponse,
    Substitution,
)

logger = logging.getLogger(__name__)

GEMINI_MODEL: str = "gemini-2.0-flash"


def _build_prompt(request: MealPlanRequest) -> str:
    """Build the prompt for the Gemini API.

    Constructs a detailed prompt that instructs Gemini to return
    a JSON object matching the MealPlanResponse schema.

    Args:
        request: The user's meal plan request with preferences.

    Returns:
        A formatted prompt string ready for the Gemini API.
    """
    return f"""You are a professional meal planner and nutritionist. Generate a complete daily meal plan based on the following requirements:

**Day Type:** {request.day_type}
**Diet:** {request.diet}
**Cuisine:** {request.cuisine}
**Ingredients at Home:** {request.ingredients_at_home}
**Budget:** ₹{request.budget:.2f}
**Number of People:** {request.num_people}

Return ONLY a valid JSON object (no markdown, no code fences, no extra text) with this exact structure:

{{
  "meals": [
    {{
      "meal_type": "breakfast" | "lunch" | "dinner",
      "dish_name": "string",
      "description": "string - brief description with preparation steps",
      "prep_time_minutes": integer,
      "ingredients": ["string", "string"]
    }}
  ],
  "grocery_list": [
    {{
      "name": "string",
      "quantity": "string (e.g., '2 lbs', '500g')",
      "estimated_cost": float,
      "category": "string (e.g., 'produce', 'dairy', 'grains', 'protein', 'pantry')"
    }}
  ],
  "substitutions": [
    {{
      "original": "string",
      "substitute": "string",
      "reason": "string"
    }}
  ],
  "budget_breakdown": {{
    "total_estimated_cost": float,
    "budget": {request.budget},
    "is_within_budget": boolean,
    "savings_tips": ["string"]
  }}
}}

Guidelines:
- Include exactly 3 meals: breakfast, lunch, and dinner.
- Tailor prep times to the day context (e.g., quick meals for busy days).
- Keep the total cost within the stated budget of ₹{request.budget:.2f} for {request.num_people} people.
- Suggest at least 2 practical ingredient substitutions.
- Provide 2-3 savings tips in the budget breakdown.
- All costs should be realistic and in INR (Indian Rupees, ₹).
- Consolidate the grocery list (no duplicate items across meals).
"""


def _strip_code_fences(text: str) -> str:
    """Remove markdown code fences from the response text.

    Gemini sometimes wraps JSON in ```json ... ``` blocks.
    This function strips those fences to extract clean JSON.

    Args:
        text: The raw response text from Gemini.

    Returns:
        The cleaned text with code fences removed.
    """
    cleaned: str = text.strip()
    # Remove ```json ... ``` or ``` ... ``` blocks
    cleaned = re.sub(r"^```(?:json)?\s*\n?", "", cleaned)
    cleaned = re.sub(r"\n?```\s*$", "", cleaned)
    return cleaned.strip()


def _create_fallback_response(request: MealPlanRequest) -> MealPlanResponse:
    """Create a minimal fallback response when Gemini fails.

    Provides a sensible default meal plan so the user still gets
    a usable result even if the AI service is unavailable.

    Args:
        request: The original meal plan request.

    Returns:
        A MealPlanResponse with simple default meals.
    """
    logger.warning("Using fallback meal plan response.")
    return MealPlanResponse(
        meals=[
            MealDetail(
                meal_type="breakfast",
                dish_name="Oatmeal with Fruit",
                description="Quick and nutritious oatmeal topped with seasonal fruit.",
                prep_time_minutes=10,
                ingredients=["oats", "milk", "banana", "honey"],
            ),
            MealDetail(
                meal_type="lunch",
                dish_name="Garden Salad with Grilled Chicken",
                description="Fresh mixed greens with grilled chicken breast and vinaigrette.",
                prep_time_minutes=20,
                ingredients=[
                    "mixed greens",
                    "chicken breast",
                    "tomato",
                    "cucumber",
                    "olive oil",
                    "lemon",
                ],
            ),
            MealDetail(
                meal_type="dinner",
                dish_name="Pasta Primavera",
                description="Penne pasta with sautéed seasonal vegetables in garlic olive oil.",
                prep_time_minutes=25,
                ingredients=[
                    "penne pasta",
                    "bell pepper",
                    "zucchini",
                    "garlic",
                    "olive oil",
                    "parmesan cheese",
                ],
            ),
        ],
        grocery_list=[
            GroceryItem(name="Oats", quantity="500g", estimated_cost=80.00, category="grains"),
            GroceryItem(name="Milk", quantity="1 litre", estimated_cost=60.00, category="dairy"),
            GroceryItem(name="Bananas", quantity="6 pieces", estimated_cost=30.00, category="produce"),
            GroceryItem(name="Chicken Breast", quantity="500g", estimated_cost=180.00, category="protein"),
            GroceryItem(name="Mixed Greens", quantity="200g", estimated_cost=50.00, category="produce"),
            GroceryItem(name="Penne Pasta", quantity="500g", estimated_cost=90.00, category="grains"),
            GroceryItem(name="Assorted Vegetables", quantity="1 kg", estimated_cost=100.00, category="produce"),
        ],
        substitutions=[
            Substitution(
                original="Chicken Breast",
                substitute="Canned Chickpeas",
                reason="More affordable plant-based protein option.",
            ),
            Substitution(
                original="Parmesan Cheese",
                substitute="Nutritional Yeast",
                reason="Dairy-free alternative with a similar savory flavor.",
            ),
        ],
        budget_breakdown=BudgetBreakdown(
            total_estimated_cost=590.00,
            budget=request.budget,
            is_within_budget=590.00 <= request.budget,
            savings_tips=[
                "Buy store-brand staples like oats and pasta to save 20-30%.",
                "Purchase seasonal produce for better prices and freshness.",
                "Consider buying a whole chicken instead of breasts for better value.",
            ],
        ),
    )


async def generate_meal_plan(request: MealPlanRequest) -> MealPlanResponse:
    """Generate a personalized meal plan using the Gemini API.

    Sends the user's preferences to Gemini and parses the structured
    JSON response into a validated MealPlanResponse. Falls back to
    a default plan if the API call or parsing fails.

    Args:
        request: The user's meal plan request containing preferences,
                 budget, number of people, and day context.

    Returns:
        A MealPlanResponse with meals, grocery list, substitutions,
        and budget breakdown.
    """
    api_key: str | None = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable is not set.")
        return _create_fallback_response(request)

    try:
        client = genai.Client(api_key=api_key)
        prompt: str = _build_prompt(request)

        logger.info(
            "Sending meal plan request to Gemini for %d people, budget $%.2f.",
            request.num_people,
            request.budget,
        )

        # The google-genai SDK uses synchronous calls
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )

        raw_text: str = response.text
        cleaned_text: str = _strip_code_fences(raw_text)

        logger.debug("Gemini raw response length: %d characters.", len(raw_text))

        meal_plan_data: dict = json.loads(cleaned_text)
        meal_plan: MealPlanResponse = MealPlanResponse.model_validate(
            meal_plan_data
        )

        logger.info(
            "Successfully generated meal plan with %d meals.",
            len(meal_plan.meals),
        )
        return meal_plan

    except json.JSONDecodeError as exc:
        logger.error(
            "Failed to parse Gemini response as JSON: %s", str(exc)
        )
        return _create_fallback_response(request)
    except Exception as exc:
        logger.error(
            "Unexpected error during meal plan generation: %s", str(exc)
        )
        return _create_fallback_response(request)
