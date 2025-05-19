import segno
import os
import base64
import io


class QRCode:
    @staticmethod
    def generate_token(n_bytes: int = 2) -> int:
        # Генерация токена
        token_bytes = base64.urlsafe_b64encode(os.urandom(n_bytes)).rstrip(b"=")

        # Преобразование токена из байтов в целое число
        token_int = int.from_bytes(token_bytes, byteorder="big")
        return token_int

    @staticmethod
    def generate_qrcode(token=None, scale: int = 50) -> io.BytesIO:
        qr = segno.make_qr(token, error='H')
        output = io.BytesIO()
        qr.save(output, kind="png", scale=scale)
        output.seek(0)
        return output
