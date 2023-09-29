from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response, JSONResponse


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONResponse(status_code=500, content={'error': str(e)})