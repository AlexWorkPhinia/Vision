from fastapi import APIRouter, HTTPException
from datetime import datetime
import cv2
import logging

from src.capture.camera import capture_frame
from src.processing import barcode as barcode_mod
from src.processing import ocr as ocr_mod

router = APIRouter()


@router.get('/scan')
async def scan_capture():
    """Capture a frame, run barcode/QR decoding and OCR, and return structured JSON."""
    img = capture_frame()
    if img is None:
        raise HTTPException(status_code=503, detail='Camera capture failed')
    detections = []
    # barcodes
    try:
        bars = barcode_mod.decode_barcodes(img)
        for b in bars:
            # attempt OCR on barcode bbox region as well
            ocr_res = ocr_mod.ocr_region(img, b['bbox'])
            detections.append({'kind': 'barcode', 'type': b['type'], 'data': b['data'], 'bbox': b['bbox'], 'ocr': ocr_res})
    except Exception as e:
        logging.exception('Barcode decode failed')

    # full-frame OCR (optional, may be expensive)
    try:
        ocr_full = ocr_mod.ocr_image(img)
        detections.append({'kind': 'ocr_full', 'text': ocr_full['text'], 'mean_conf': ocr_full['mean_conf']})
    except Exception:
        logging.exception('Full-frame OCR failed')

    return {'timestamp': datetime.utcnow().isoformat() + 'Z', 'detections': detections}
