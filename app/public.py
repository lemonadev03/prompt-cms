import uuid
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .database import get_db
from .models import Prompt

router = APIRouter()

@router.get("/prompt/{prompt_id}")
def get_prompt(
    prompt_id: str,
    db: Session = Depends(get_db)
):
    """Get raw markdown content by UUID"""
    try:
        # Parse UUID
        prompt_uuid = uuid.UUID(prompt_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Query database
    prompt = db.query(Prompt).filter(Prompt.id == prompt_uuid).first()
    
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    # Return raw markdown content
    return Response(
        content=prompt.content,
        media_type="text/plain; charset=utf-8"
    ) 