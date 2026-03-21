from uuid import uuid4

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, Uuid
from sqlalchemy.orm import relationship

from app.core.database import Base


class ADR(Base):
    __tablename__ = "adrs"
    id = Column(Uuid, primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    context = Column(String, nullable=False)
    decision = Column(String, nullable=False)
    consequences = Column(String, nullable=False)
    status = Column(String, default="proposed")
    version = Column(Integer, default=1)
    project_id = Column(Uuid, ForeignKey("projects.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    project = relationship("Project", back_populates="adrs")
