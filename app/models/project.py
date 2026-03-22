from uuid import uuid4
from sqlalchemy import (
    Column,
    UUID,
    DateTime,
    ForeignKey,
    String,
    ARRAY,
    func,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    status = Column(String, default="active")
    stack = Column(ARRAY(String), nullable=False)
    github_url = Column(String, nullable=True)
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    started_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    owner = relationship("User", back_populates="projects")
    adrs = relationship("ADR", back_populates="project")
