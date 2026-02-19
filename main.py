import asyncio
from time import perf_counter
from typing import List
import os
import json
from datetime import date, datetime
import re

from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

class CalculateRequest(BaseModel):
    numbers: List[float]
    delays: List[float]

class ResultItem(BaseModel):
    number: float
    square: float
    delay: float
    time: float

class CalculateResponse(BaseModel):
    results: List[ResultItem]
    total_time: float
    parallel_faster_than_sequential: bool

async def square_with_delay(number: float, delay: float) -> ResultItem:
    start = perf_counter()
    await asyncio.sleep(delay)
    end = perf_counter()
    return ResultItem(
        number=number,
        square=number ** 2, 
        delay=delay,
        time=round(end - start, 2),
    )


class Appeal(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "last_name": "Иванов",
                "first_name": "Иван",
                "birth_date": "1990-05-15",
                "phone": "+79161234567",
                "email": "ivanov@example.com"
            }
        }
    )
    
    last_name: str = Field(
        ..., 
        description="Фамилия (только кириллица, с заглавной буквы)",
        min_length=2,
        max_length=50
    )
    first_name: str = Field(
        ...,
        description="Имя (только кириллица, с заглавной буквы)",
        min_length=2,
        max_length=50
    )
    birth_date: date = Field(
        description="Дата рождения в формате ГГГГ-ММ-ДД"
    )
    phone: str = Field(
        ...,
        description="Номер телефона",
        min_length=10,
        max_length=20
    )
    email: EmailStr = Field(
        description="Электронная почта"
    )

    @field_validator('last_name')
    @classmethod
    def validate_last_name(cls, v: str) -> str:
        if not re.fullmatch(r'[А-ЯЁ][а-яё]+', v):
            raise ValueError('Фамилия должна содержать только кириллицу и начинаться с заглавной буквы')
        return v

    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls, v: str) -> str:
        if not re.fullmatch(r'[А-ЯЁ][а-яё]+', v):
            raise ValueError('Имя должно содержать только кириллицу и начинаться с заглавной буквы')
        return v

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('Дата рождения не может быть в будущем')
        return v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = re.sub(r'[\s\-\(\)]', '', v)
        if not re.search(r'\d', cleaned):
            raise ValueError('Телефон должен содержать цифры')
        return cleaned

app = FastAPI(
    title="Homework API",
    description="ДЗ1: Асинхронность + ДЗ2: Обращения абонентов",
    version="1.0.0"
)

@app.post("/calculate/", response_model=CalculateResponse, tags=["ДЗ1 - Асинхронность"])
async def calculate(data: CalculateRequest) -> CalculateResponse:
    start_parallel = perf_counter()
    results = await asyncio.gather(
        *(square_with_delay(n, d) for n, d in zip(data.numbers, data.delays))
    )
    parallel_time = perf_counter() - start_parallel

    start_seq = perf_counter()
    for n, d in zip(data.numbers, data.delays):
        await square_with_delay(n, d)
    seq_time = perf_counter() - start_seq

    return CalculateResponse(
        results=results,
        total_time=round(parallel_time, 2),
        parallel_faster_than_sequential=parallel_time < seq_time,
    )

@app.post("/appeal/", tags=["ДЗ2 - Обращения"])
async def create_appeal(appeal: Appeal):
    os.makedirs("appeals", exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"appeal_{timestamp}.json"
    filepath = os.path.join("appeals", filename)
    
    data = appeal.model_dump()
    data['birth_date'] = data['birth_date'].isoformat()  
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return {
        "message": "Обращение успешно сохранено",
        "filename": filename,
        "data": data
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )