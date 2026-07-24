from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database.session import Base


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String(255),
        unique=True,
        nullable=False
    )

    description = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


knowledge_base = KnowledgeBase()

