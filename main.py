import asyncio
from time import perf_counter
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


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
        square=number * number,
        delay=delay,
        time=round(end - start, 2),
    )


@app.post("/calculate/", response_model=CalculateResponse)
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
