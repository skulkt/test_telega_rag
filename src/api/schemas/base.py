from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class ApiResponseBase(BaseModel, Generic[T]):
    code: int = 0
    message: str = None
    data: T = []
