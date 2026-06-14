from typing import Optional, Generic, TypeVar
from pydantic import BaseModel
T = TypeVar('T')


class ResponseModel(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None


