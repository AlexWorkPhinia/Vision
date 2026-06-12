from fastapi import APIRouter, File, UploadFile, HTTPException
import numpy as np
import cv2
from datetime import datetime
import logging

from src.processing import barcode as barcode_mod
from src.processing import ocr as ocr_mod

router = APIRouter()


@router.post('/upload')
async def upload_image(image: UploadFile = File(...)):
    contents = await image.read()
    arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail='Invalid image')
    detections = []
    try:
        bars = barcode_mod.decode_barcodes(img)
        for b in bars:
            ocr_res = ocr_mod.ocr_region(img, b['bbox'])
            detections.append({'kind': 'barcode', 'type': b['type'], 'data': b['data'], 'bbox': b['bbox'], 'ocr': ocr_res})
    except Exception:
        logging.exception('Barcode decode failed')
    try:
        ocr_full = ocr_mod.ocr_image(img)
        detections.append({'kind': 'ocr_full', 'text': ocr_full['text'], 'mean_conf': ocr_full['mean_conf']})
    except Exception:
        logging.exception('Full-frame OCR failed')
    return {'timestamp': datetime.utcnow().isoformat() + 'Z', 'detections': detections}
