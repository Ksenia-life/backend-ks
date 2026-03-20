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