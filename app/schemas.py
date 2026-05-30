from pydantic import BaseModel, ConfigDict, Field, field_validator


class StudentBase(BaseModel):
    last_name: str = Field(min_length=1, max_length=50)
    first_name: str = Field(min_length=1, max_length=50)
    faculty: str = Field(min_length=1, max_length=100)
    course: str = Field(min_length=1, max_length=100)
    grade: int = Field(ge=0, le=100)

    @field_validator("last_name", "first_name", "faculty", "course")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty")

        return value


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Username cannot be empty")

        return value


class UserRegister(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserLogin(UserBase):
    password: str = Field(min_length=6, max_length=128)


class UserResponse(UserBase):
    id: int
    is_logged_in: bool

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    message: str
    user_id: int


class StudentDeleteList(BaseModel):
    student_ids: list[int] = Field(min_length=1)

    @field_validator("student_ids")
    @classmethod
    def validate_student_ids(cls, value: list[int]) -> list[int]:
        for student_id in value:
            if student_id <= 0:
                raise ValueError("Student id must be positive")

        return value