"""Main application entry point for the AI Cooking To-Do List.

This module configures the FastAPI application, registers middleware,
mounts static files, and includes API routers.
"""

import logging
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routes.meal_planner import router as meal_planner_router

# ---------------------------------------------------------------------------
# Load environment variables from .env file if python-dotenv is available
# ---------------------------------------------------------------------------
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv is optional; environment vars can be set directly

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Application setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="AI Cooking To-Do List",
    description=(
        "An AI-powered meal planner that generates personalized daily "
        "meal plans, grocery lists, and budget breakdowns using the "
        "Google Gemini API."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS middleware (allow all origins for development — restrict in production)
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Include API routers
# ---------------------------------------------------------------------------
app.include_router(meal_planner_router)

# ---------------------------------------------------------------------------
# Static files
# ---------------------------------------------------------------------------
STATIC_DIR: Path = Path(__file__).resolve().parent / "static"

if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    logger.info("Mounted static files from %s.", STATIC_DIR)
else:
    logger.warning(
        "Static directory not found at %s. Static files will not be served.",
        STATIC_DIR,
    )


# ---------------------------------------------------------------------------
# Root route — serves the frontend
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
async def root() -> FileResponse:
    """Serve the main index.html page.

    Returns the single-page application entry point from the
    static files directory.

    Returns:
        A FileResponse serving index.html.
    """
    index_path: Path = STATIC_DIR / "index.html"
    if index_path.is_file():
        return FileResponse(str(index_path))
    return FileResponse(
        str(index_path),
        status_code=404,
    )


if __name__ == "__main__":
    import uvicorn

    port: int = int(os.environ.get("PORT", "8000"))
    logger.info("Starting server on port %d.", port)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
