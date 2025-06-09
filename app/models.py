import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class Prompt(Base):
    __tablename__ = "prompts"
    
    id = Column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        nullable=False
    )
    content = Column(Text, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    def __repr__(self):
        return f"<Prompt(id={self.id}, description='{self.description}')>" 