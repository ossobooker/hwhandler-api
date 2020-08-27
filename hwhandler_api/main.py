import sys
import logging

# from functools import wraps


from typing import Optional
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import List, Optional
from starlette.responses import RedirectResponse

from hwhandler_api.core import BaseSystem

# logging setup
logging.basicConfig(
    # filename="test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# default config file setup
# FIXME: we a need a automatized way to pass the config file
config_file = "config_setup/configuration/config_file.yaml"

# System setup
hw_system = BaseSystem(config_file=config_file)

# API setup
hwhandler_api = FastAPI()

### Pydantic Models
# FSM Model
class FSM(BaseModel):
    state: str = ""
    available_transitions: Optional[List[str]] = []


# Transition Model
class Transition(BaseModel):
    transition: str = ""


### API routes

# block the system when it is ERROR
def check_system_status():
    """Block the system when it is ERROR. It should be applied whenever a new route is defined. """
    if hw_system.system_status.status_code != 0:
        raise HTTPException(
            status_code=500,
            detail=f"{hw_system.system_status.error_message} (Internal status code: {hw_system.system_status.status_code})",
        )


# API status
@hwhandler_api.get("/")
async def root():
    url = hwhandler_api.url_path_for("system_status")
    response = RedirectResponse(url=url)
    return response


@hwhandler_api.get("/status")
# @check_system_status
async def system_status():
    check_system_status()
    return {
        "status": hw_system.system_status.status_code,
        "error_message": hw_system.system_status.error_message,
    }


# System Info
@hwhandler_api.get("/system")
async def system_info():
    check_system_status()
    return hw_system.config["system"]


# FSM Stuff
@hwhandler_api.get("/fsm", response_model=FSM)
async def fsm_state():
    check_system_status()
    return FSM(
        state=hw_system.fsm.state,
        available_transitions=hw_system.fsm.available_transitions(),
    )


@hwhandler_api.put("/fsm", response_model=FSM)
async def fsm_transition(transition: Transition):
    check_system_status()
    getattr(hw_system.fsm, transition.transition)()
    return FSM(
        state=hw_system.fsm.state,
        available_transitions=hw_system.fsm.available_transitions(),
    )


# FEB Control Stuff
# @hwhandler_api.put("/febcontrol/configure")
# async def febcontrol_configure(feb_part: FecPart):
#     # executing command
#     # FIXME: Implement FEBControl Command.
#     return { "OK" }
