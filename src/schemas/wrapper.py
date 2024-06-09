from typing import Any, Optional

from pydantic import BaseModel


class SuccessResponseSchema(BaseModel):
    status: int = 200
    data: Any
    detail: Optional[str]
