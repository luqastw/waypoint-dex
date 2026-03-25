from uuid import UUID, uuid4
from sqlalchemy import String, Column, Text, ForeignKey, Enum as SAEnum, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.enums import TaskStatus, TaskPriority

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SAEnum(TaskStatus, name="taskstatus"), default=TaskStatus.TODO)
    priority = Column(SAEnum(TaskPriority, name="taskpriority"), default=TaskPriority.MEDIUM)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    deadline = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    project = relationship("Project", back_populates="tasks")