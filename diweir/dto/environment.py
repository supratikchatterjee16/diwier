from pydantic import BaseModel


class EnvironmentDto(BaseModel):
    name: str
    desc : str
