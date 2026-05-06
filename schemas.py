from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ChoiceBase(BaseModel):
    choice: str

class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    email: EmailStr = Field(max_length=120)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int