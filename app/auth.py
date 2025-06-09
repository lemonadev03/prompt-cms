import os
import hashlib
import secrets
from typing import Optional
from fastapi import Request, HTTPException, status, Depends
from starlette.responses import RedirectResponse

# Admin password from environment variable
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))

def verify_password(password: str) -> bool:
    """Verify admin password"""
    return password == ADMIN_PASSWORD

def create_session_token() -> str:
    """Create a session token"""
    return secrets.token_urlsafe(32)

def is_authenticated(request: Request) -> bool:
    """Check if user is authenticated via session"""
    return request.session.get("authenticated", False)

def require_auth(request: Request):
    """Dependency to require authentication for admin routes"""
    if not is_authenticated(request):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    return True

def optional_auth(request: Request) -> bool:
    """Optional authentication check"""
    return is_authenticated(request)

def login_user(request: Request):
    """Log in user by setting session"""
    request.session["authenticated"] = True
    request.session["token"] = create_session_token()

def logout_user(request: Request):
    """Log out user by clearing session"""
    request.session.clear()

def redirect_if_not_authenticated(request: Request, target_url: str = "/admin/login"):
    """Redirect to login if not authenticated"""
    if not is_authenticated(request):
        return RedirectResponse(url=target_url, status_code=302)
    return None 