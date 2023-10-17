from pydantic import BaseModel

class UserIn(BaseModel):
    username: str
    age: int

class UserOut(UserIn):
    id: int
    
    class Config:
        orm_mode = True
