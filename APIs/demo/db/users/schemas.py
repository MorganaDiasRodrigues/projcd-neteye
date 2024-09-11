from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    first_name: str = Field(..., min_length=1, max_length=250)
    last_name: str = Field(..., min_length=1, max_length=250)
    email: EmailStr


class PatchUser(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    first_name: str | None = Field(None, min_length=1, max_length=250)
    last_name: str | None = Field(None, min_length=1, max_length=250)
    email: EmailStr | None = None
