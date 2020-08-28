from fastapi import APIRouter, HTTPException

from hwhandler_api.core import hw_system

router = APIRouter()


@router.get("/feb-control/configure")
async def feb_control_configure():
    return {}


@router.get("/feb-control/monitor")
async def feb_control_monitor():
    return {}


# FEB Control Stuff
# @hwhandler_api.put("/febcontrol/configure")
# async def febcontrol_configure(feb_part: FecPart):
#     # executing command
#     # FIXME: Implement FEBControl Command.
#     return { "OK" }
