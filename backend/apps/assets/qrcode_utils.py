"""QR code generation for asset labels."""
from io import BytesIO
import qrcode
from django.conf import settings


def generate_asset_qrcode(asset):
    """Generate a QR code PNG for an asset. Returns BytesIO."""
    url = f"{settings.FRONTEND_BASE_URL}/assets/{asset.id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return buf
