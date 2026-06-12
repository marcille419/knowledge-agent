from datetime import datetime
from pydantic import BaseModel

class DocumentInfo(BaseModel):
    id: int
    filename: str
    file_size: int
    file_type: str
    created_at: datetime

    model_config = {
        "from_attributes" : True
    }