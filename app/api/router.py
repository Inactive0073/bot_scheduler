import base64

from aiogram.types import BufferedInputFile
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from .schemas import QRCodeScanner
from app.main import bot


router = APIRouter(prefix="/api", tags=["API"])


@router.post("/send-scaner-info/", response_class=JSONResponse)
async def send_qr_code(request: QRCodeScanner):
    try:
        text = (
            f"🎉 QR-код успешно отсканирован!\n\n"
            f"📄 Результат сканирования:\n\n"
            f"<code><b>{request.result_scan}</b></code>\n\n"
        )
        await bot.send_message(chat_id=request.user_id, text=text)
        return JSONResponse(
            content={
                "message": "QR-код успешно просканирован, а данные отправлены в Telegram"
            },
            status_code=200,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
