from fastapi import APIRouter, HTTPException

from pydantic import BaseModel
from typing import List, Optional

from hwhandler_api.core import hw_system

### Pydantic Models
# FSM Model
class FSM(BaseModel):
    state: str = ""
    available_transitions: Optional[List[str]] = []


# Transition Model
class Transition(BaseModel):
    transition: str = ""


router = APIRouter()


@router.get("/fsm", response_model=FSM)
async def fsm_state():
    return FSM(
        state=hw_system.fsm.state,
        available_transitions=hw_system.fsm.available_transitions(),
    )


@router.put("/fsm", response_model=FSM)
async def fsm_transition(transition: Transition):
    getattr(hw_system.fsm, transition.transition)()
    return FSM(
        state=hw_system.fsm.state,
        available_transitions=hw_system.fsm.available_transitions(),
    )