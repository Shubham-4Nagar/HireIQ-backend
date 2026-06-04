import uuid
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database.database import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    job_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        nullable=False
    )

    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    job_description = Column(Text, nullable=False)

    match_score = Column(String(10), nullable=True)
    analysis = Column(
        Text, nullable=True
    )

    status = Column(
        String(50),
        default="Applied"
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=True
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    deleted_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    
