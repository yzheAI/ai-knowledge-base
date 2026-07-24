from sqlalchemy.orm import Session

from app.crud.knowledge_base import create_kb


def test_create_kb(db: Session):

    kb = create_kb(
        db,
        "test_kb"
    )

    assert kb.id is not None
    assert kb.name == "test_kb"
