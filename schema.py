import pydantic
from typing import Optional
from abc import ABC

class AbstractUser(pydantic.BaseModel, ABC):
    name: str
    password: str

    @pydantic.field_validator('password')
    @classmethod
    def check_password(cls, v: str) -> str:
        if len(v) < 5:
            raise ValueError(f'Minimal length password is 5')
        return v


class CreatesUser(AbstractUser):
    name: str
    password: str


class UpdateUser(AbstractUser):
    name: Optional[str] = None
    password: Optional[str] = None
