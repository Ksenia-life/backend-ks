from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String, nullable=False, index=True)
    first_name = Column(String, nullable=False, index=True)
    faculty = Column(String, nullable=False, index=True)
    course = Column(String, nullable=False, index=True)
    grade = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_logged_in = Column(Boolean, nullable=False, default=False)