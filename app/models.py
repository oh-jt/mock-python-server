from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    """Validated payload for creating a user. Role and tenant are never client-controlled."""

    email: EmailStr
    display_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=12, max_length=128)


class UserOut(BaseModel):
    id: int
    tenant_id: int
    email: str
    display_name: str
    role: str
    created_at: str
