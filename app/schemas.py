from pydantic import BaseModel, ConfigDict


class StudentBase(BaseModel):
    last_name: str
    first_name: str
    faculty: str
    course: str
    grade: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    username: str


class UserRegister(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_logged_in: bool

    model_config = ConfigDict(from_attributes=True)


class LoginResponse(BaseModel):
    message: str
    user_id: int
    
class StudentDeleteList(BaseModel):
    student_ids: list[int]