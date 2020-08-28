import logging

from fastapi import APIRouter, HTTPException

from hwhandler_api.core import hw_system

router = APIRouter()


@router.get("/system/data-clock-managers")
async def data_clock_managers_info():
    return hw_system.config["system"]["data-clock-managers"]


@router.get("/system/data-clock-managers/{dcm_id}")
async def board_info(dcm_id: str):
    try:
        return next(
            dcm
            for dcm in hw_system.config["system"]["data-clock-managers"]
            if dcm["id"] == dcm_id
        )
    except:
        message = f"It was not possible to find the requested data-clock-manager ({dcm_id})."
        logging.error(message)
        raise HTTPException(status_code=500, detail=message,)

