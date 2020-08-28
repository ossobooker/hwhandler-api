from fastapi import APIRouter, HTTPException

from hwhandler_api.core import hw_system

router = APIRouter()


@router.get("/system/boards")
async def boards_info():
    # check_system_status(hw_system)
    return hw_system.config["system"]["boards"]


@router.get("/system/boards/{board_id}")
async def board_info(board_id: str):
    # check_system_status(hw_system)
    try:
        return next(
            board
            for board in hw_system.config["system"]["boards"]
            if board["id"] == board_id
        )
    except:
        raise HTTPException(
            status_code=500,
            detail=f"It was not possible to find the requested board ({board_id}).",
        )