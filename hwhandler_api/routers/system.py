from fastapi import APIRouter, HTTPException

from hwhandler_api.core import hw_system

router = APIRouter()


@router.get("/status")
async def system_status():
    # check_system_status(hw_system)
    return {
        "status": hw_system.system_status.status_code,
        "error_message": hw_system.system_status.error_message,
    }


# System Info
@router.get("/system")
async def system_info():
    # check_system_status(hw_system)
    return hw_system.config["system"]
