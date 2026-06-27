"""Meal planner API routes for the AI Cooking To-Do List application.

This module defines the FastAPI router for meal plan generation
and health check endpoints.
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status

from models.schemas import MealPlanRequest, MealPlanResponse
from services.gemini_service import generate_meal_plan

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Meal Planner"])


def _validate_input_lengths(request: MealPlanRequest) -> None:
    """Validate that request fields don't contain excessively long content.

    Performs additional server-side validation beyond Pydantic's
    field-level constraints to catch edge cases.

    Args:
        request: The incoming meal plan request to validate.

    Raises:
        HTTPException: If any field exceeds its allowed length.
    """
    if len(request.day_type.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Day type cannot be empty.",
        )
    if len(request.diet.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Diet cannot be empty.",
        )
    if len(request.cuisine.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Cuisine cannot be empty.",
        )


@router.post(
    "/generate-meal-plan",
    response_model=MealPlanResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a personalized meal plan",
    description="Accepts dietary preferences, budget, and context to "
    "generate an AI-powered daily meal plan with grocery list "
    "and budget breakdown.",
)
async def create_meal_plan(request: MealPlanRequest) -> MealPlanResponse:
    """Generate a personalized meal plan via the Gemini API.

    Validates the incoming request, calls the Gemini service to
    generate a structured meal plan, and returns the result.

    Args:
        request: The meal plan request body.

    Returns:
        A MealPlanResponse with meals, grocery list, substitutions,
        and budget breakdown.

    Raises:
        HTTPException: On validation failure or internal errors.
    """
    _validate_input_lengths(request)

    logger.info(
        "Received meal plan request: %d people, budget $%.2f, preferences='%s'.",
        request.num_people,
        request.budget,
        request.diet[:50],
    )

    try:
        meal_plan: MealPlanResponse = await generate_meal_plan(request)
        logger.info(
            "Meal plan generated successfully with %d meals.",
            len(meal_plan.meals),
        )
        return meal_plan
    except Exception as exc:
        logger.error("Failed to generate meal plan: %s", str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while generating the meal plan. "
            "Please try again later.",
        ) from exc


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Returns the current health status of the API.",
)
async def health_check() -> dict[str, str]:
    """Return the health status of the application.

    Provides a simple liveness check for monitoring and
    deployment health probes.

    Returns:
        A dictionary with status and timestamp.
    """
    return {
        "status": "healthy",
        "service": "AI Cooking To-Do List",
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
