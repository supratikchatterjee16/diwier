from pydantic import BaseModel


class DatabaseDto(BaseModel):
    name: str
    env: str
    prvdr: str
    host: str
    port: int
    schm: str
    user: str
    psk: str
