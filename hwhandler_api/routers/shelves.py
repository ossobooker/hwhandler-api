import logging

from fastapi import APIRouter, HTTPException

from hwhandler_api.core import hw_system

router = APIRouter()


@router.get("/system/shelves")
async def shelves_info():
    # check_system_status(hw_system)
    return hw_system.config["system"]["shelves"]


@router.get("/system/shelves/{shelf_id}")
async def shelf_info(shelf_id: str):
    # check_system_status(hw_system)
    try:
        return next(
            shelf
            for shelf in hw_system.config["system"]["shelves"]
            if shelf["id"] == shelf_id
        )
    except:
        message = f"It was not possible to find the requested shelf ({shelf_id})."
        logging.error(message)
        raise HTTPException(status_code=500, detail=message,)