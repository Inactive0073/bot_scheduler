
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from .schemas import QRCodeScanner
from app.setup import DependeciesConfig
from app.config_data.config import load_config, Config

config: Config = load_config()
bot = DependeciesConfig(config=config).setup_bot()

router = APIRouter(prefix="/api", tags=["API"])


@router.post("/send-scaner-info/", response_class=JSONResponse)
async def send_qr_code(request: QRCodeScanner):
    try:
        text = (
            f"🎉 QR-код успешно отсканирован!\n\n"
            f"📄 Результат сканирования:\n\n"
            f"<code><b>{request.result_scan}</b></code> <i>⬅ Код копируется</i>\n\n"
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
