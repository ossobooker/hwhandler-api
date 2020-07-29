import sys
import logging

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
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

# default config file setup
# FIXME: we a need a automatized way to pass the config file
config_file = "https://gitlab.cern.ch/rpcos4ph2setups/dummy-setup/-/raw/master/configuration/config_file.yaml"

# System setup
hw_system = BaseSystem(config_file = config_file)

# API setup
hwhandler_api = FastAPI()

# FSM Model
class FSM(BaseModel):
    state: str = ''
    available_transitions: Optional[List[str]] = []

# Transition Model
class Transition(BaseModel):
    transition: str = ''

# API routes
@hwhandler_api.get("/")
async def root():
    url = hwhandler_api.url_path_for("system_status")
    response = RedirectResponse(url=url)
    return response

@hwhandler_api.get("/status")
async def system_status():
    if hw_system.system_status.status_code == 0:
        return {
            "status": hw_system.system_status.status_code,
            "error_message": hw_system.system_status.error_message,
            }
    else:
        raise HTTPException(status_code=500, detail=f'{hw_system.system_status.error_message} (Internal status code: {hw_system.system_status.status_code})')


@hwhandler_api.get("/fsm", response_model=FSM)
async def fsm_state():
    return FSM(
        state=hw_system.fsm.state,
        available_transitions=hw_system.fsm.available_transitions()
    )

@hwhandler_api.put("/fsm", response_model=FSM)
# @hwhandler_api.put("/fsm")
async def fsm_transition(transition: Transition):
    getattr(hw_system.fsm, transition.transition)()
    return FSM(
        state=hw_system.fsm.state,
        available_transitions=hw_system.fsm.available_transitions()
    )
