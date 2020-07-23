from typing import Optional

from fastapi import FastAPI

from hwhandler_api.fsm import FSM

hwhandler_api = FastAPI()

system_fsm = FSM("system_fsm")


@hwhandler_api.get("/")
def read_root():
    return {"Is this real?": "33"}

@hwhandler_api.get("/fsm/status")
def fsm_status():
    return {"status": system_fsm.state}

@hwhandler_api.get("/fsm/{transition}")
def fsm_transition(transition: str):
    getattr(system_fsm, transition)()
    return {"status": system_fsm.state}

@hwhandler_api.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}