from pydantic import BaseModel

class to_do(BaseModel):
    id: int
    name: str
    description: str
    complete: bool