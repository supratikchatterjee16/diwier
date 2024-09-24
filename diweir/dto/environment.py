from pydantic import BaseModel, Field
from typing import Optional

class EnvironmentDto(BaseModel):
    name: str = Field(..., example="production")  # Required field
    desc: Optional[str] = Field(None, example="Production environment")
