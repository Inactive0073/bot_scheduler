import segno
import os
import base64
import io

def generate_token(n_bytes: int = 7) -> str:
    return base64.urlsafe_b64encode(os.urandom(n_bytes)).rstrip(b'=').decode('ascii')


def generate_qrcode(scale: int = 5):
    token = generate_token()
    
    qr = segno.make(token)
    output = io.BytesIO() 
    qr.save(output, kind='png', scale=scale)
    output.seek(0)
    return output