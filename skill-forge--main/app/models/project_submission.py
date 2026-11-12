from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.postgres import Base


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    repository_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(30), default="submitted", nullable=False)
    score = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    reviewed_at = Column(DateTime, nullable=True)

    project = relationship("Project")
    user = relationship("User")