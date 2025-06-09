import os
import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates

from .database import create_tables, close_db
from .admin import router as admin_router
from .public import router as public_router
from .auth import SECRET_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def startup_event():
    """Startup event handler"""
    logger.info("Starting up...")
    try:
        create_tables()
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        raise

def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down...")
    close_db()

# Create FastAPI app
app = FastAPI(
    title="Prompt CMS",
    description="FastAPI-based Content Management System for Markdown Prompts",
    version="1.0.0"
)

# Add event handlers
app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=86400,  # 24 hours
    same_site="lax",
    https_only=False  # Set to True in production with HTTPS
)

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Get the base directory (where this file is located)
import pathlib
BASE_DIR = pathlib.Path(__file__).parent

# Mount static files with absolute path
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Setup templates with absolute path
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Include routers
app.include_router(admin_router)
app.include_router(public_router)

# Error handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )
    elif exc.status_code == 500:
        return templates.TemplateResponse(
            "500.html",
            {"request": request},
            status_code=500
        )
    else:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "error": exc.detail, "status_code": exc.status_code},
            status_code=exc.status_code
        )

# Root redirect
@app.get("/", response_class=HTMLResponse)
async def root():
    """Redirect root to admin"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/admin", status_code=302)

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Debug endpoint for checking static files
@app.get("/debug/static")
async def debug_static():
    """Debug static file paths"""
    import os
    static_dir = BASE_DIR / "static"
    css_file = static_dir / "css" / "admin.css"
    js_file = static_dir / "js" / "admin.js"
    
    return {
        "base_dir": str(BASE_DIR),
        "static_dir": str(static_dir),
        "static_dir_exists": static_dir.exists(),
        "css_file_exists": css_file.exists(),
        "js_file_exists": js_file.exists(),
        "css_file_path": str(css_file),
        "static_files": [f.name for f in static_dir.rglob("*") if f.is_file()] if static_dir.exists() else []
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 