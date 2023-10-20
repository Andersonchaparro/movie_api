from pydantic import BaseModel

class User(BaseModel):
    email: str = "admin@gmail.com"
    password: str = "admin"