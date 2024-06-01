import time
from fastapi import Request


async def time_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    duration = end_time - start_time
    print(f"Request took {duration} seconds")
    response.headers["X-Response-Time"] = str(duration)
    return response
