from pydantic import BaseModel
from typing import Any, Optional

class BaseResponse(BaseModel):
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None