import sys
import logging

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from starlette.responses import RedirectResponse

from hwhandler_api.core import BaseSystem
from hwhandler_api.core import hw_system

from hwhandler_api.routers import shelves, boards, system, fsm, feb_control


# logging setup
logging.basicConfig(
    # filename="test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# API setupss
hwhandler_api = FastAPI()

# system check status middleware
@hwhandler_api.middleware("http")
async def check_system_status(request: Request, call_next):
    """Raise an HTTPException (500) if the system is not properly set."""

    if hw_system.system_status.status_code != 0:
        return JSONResponse(
            content=f"{hw_system.system_status.error_message} (Internal status code: {hw_system.system_status.status_code})",
            status_code=500,
        )
    else:
        return await call_next(request)


### API routes
# API status
@hwhandler_api.get("/")
async def root():
    url = hwhandler_api.url_path_for("system_status")
    response = RedirectResponse(url=url)
    return response


# system routes
hwhandler_api.include_router(system.router)

# boards routes
hwhandler_api.include_router(boards.router)

# shelves routes
hwhandler_api.include_router(shelves.router)

# fsm routes
hwhandler_api.include_router(fsm.router)

# fsm routes
hwhandler_api.include_router(feb_control.router)
