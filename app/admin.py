import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .database import get_db
from .models import Prompt
from .auth import (
    verify_password, 
    login_user, 
    logout_user, 
    is_authenticated,
    redirect_if_not_authenticated
)

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    """Login form page"""
    if is_authenticated(request):
        return RedirectResponse(url="/admin", status_code=302)
    return templates.TemplateResponse(
        "admin/login.html", 
        {"request": request}
    )

@router.post("/login")
def login(
    request: Request,
    password: str = Form(...)
):
    """Handle login authentication"""
    if verify_password(password):
        login_user(request)
        return RedirectResponse(url="/admin", status_code=302)
    else:
        return templates.TemplateResponse(
            "admin/login.html",
            {"request": request, "error": "Invalid password"}
        )

@router.post("/logout")
def logout(request: Request):
    """Handle logout"""
    logout_user(request)
    return RedirectResponse(url="/admin/login", status_code=302)

@router.get("/", response_class=HTMLResponse)
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db)
):
    """Admin dashboard showing all prompts"""
    # Check authentication
    redirect_response = redirect_if_not_authenticated(request)
    if redirect_response:
        return redirect_response
    
    # Get all prompts
    prompts = db.query(Prompt).order_by(Prompt.created_at.desc()).all()
    
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {"request": request, "prompts": prompts}
    )

@router.get("/prompt/new", response_class=HTMLResponse)
def new_prompt_form(request: Request):
    """Form to create new prompt"""
    redirect_response = redirect_if_not_authenticated(request)
    if redirect_response:
        return redirect_response
    
    return templates.TemplateResponse(
        "admin/prompt_form.html",
        {"request": request, "prompt": None, "action": "Create"}
    )

@router.post("/prompt/new")
def create_prompt(
    request: Request,
    description: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle prompt creation"""
    redirect_response = redirect_if_not_authenticated(request)
    if redirect_response:
        return redirect_response
    
    # Create new prompt
    new_prompt = Prompt(
        description=description,
        content=content
    )
    
    db.add(new_prompt)
    db.commit()
    db.refresh(new_prompt)
    
    return RedirectResponse(url="/admin", status_code=302)

@router.get("/prompt/{prompt_id}/edit", response_class=HTMLResponse)
def edit_prompt_form(
    request: Request,
    prompt_id: str,
    db: Session = Depends(get_db)
):
    """Form to edit existing prompt"""
    redirect_response = redirect_if_not_authenticated(request)
    if redirect_response:
        return redirect_response
    
    try:
        prompt_uuid = uuid.UUID(prompt_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    prompt = db.query(Prompt).filter(Prompt.id == prompt_uuid).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    return templates.TemplateResponse(
        "admin/edit_prompt.html",
        {"request": request, "prompt": prompt, "action": "Update"}
    )

@router.post("/prompt/{prompt_id}/edit")
def update_prompt(
    request: Request,
    prompt_id: str,
    description: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle prompt updates"""
    redirect_response = redirect_if_not_authenticated(request)
    if redirect_response:
        return redirect_response
    
    try:
        prompt_uuid = uuid.UUID(prompt_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    prompt = db.query(Prompt).filter(Prompt.id == prompt_uuid).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Update prompt
    prompt.description = description
    prompt.content = content
    
    db.commit()
    
    return RedirectResponse(url="/admin", status_code=302)

@router.post("/prompt/{prompt_id}/delete")
def delete_prompt(
    request: Request,
    prompt_id: str,
    db: Session = Depends(get_db)
):
    """Handle prompt deletion"""
    redirect_response = redirect_if_not_authenticated(request)
    if redirect_response:
        return redirect_response
    
    try:
        prompt_uuid = uuid.UUID(prompt_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    db.query(Prompt).filter(Prompt.id == prompt_uuid).delete()
    db.commit()
    
    return RedirectResponse(url="/admin", status_code=302) 