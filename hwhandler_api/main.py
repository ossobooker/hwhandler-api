import sys
import logging

from typing import Optional
from fastapi import FastAPI

from hwhandler_api.fsm import FSM
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

# API routes
@hwhandler_api.get("/")
async def read_root():
    return {"Is this real?": "33"}


@hwhandler_api.get("/fsm/state")
async def fsm_state():
    return {"state": hw_system.fsm.state}


@hwhandler_api.get("/fsm/{transition}")
async def fsm_transition(transition: str):
    getattr(hw_system.fsm, transition)()
    return {"state": hw_system.fsm.state}

# DUMMY
# FIXME: remove!
@hwhandler_api.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
