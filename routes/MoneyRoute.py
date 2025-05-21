from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from models.money import MoneyRequest
from services.MoneyService import MoneyService

router = APIRouter(prefix="/money", tags=["money"])


@router.post("/", response_class=HTMLResponse)
async def get_money(
    request: MoneyRequest,
    money_service: MoneyService = Depends(lambda: MoneyService())
) -> HTMLResponse:
    try:
        return await money_service.get_money(request.tableId)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Внутренняя ошибка сервера: {str(e)}"
        )


