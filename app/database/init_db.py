from app.database.session import engine, Base

# 必须导入模型
from app.models.knowledge_base import KnowledgeBase


Base.metadata.create_all(bind=engine)