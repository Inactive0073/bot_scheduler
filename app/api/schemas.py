from pydantic import BaseModel


class QRBase(BaseModel):
    user_id: int


class QRCodeScanner(QRBase):
    result_scan: str
