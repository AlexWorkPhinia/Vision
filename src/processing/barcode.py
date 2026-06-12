"""
Barcode/QR decoding wrapper using pyzbar.
"""
from typing import List, Dict
from pyzbar import pyzbar
import numpy as np


def decode_barcodes(image: np.ndarray) -> List[Dict]:
    """Decode barcodes and QR codes from BGR OpenCV image.
    Returns list of dicts: {type, data, bbox:{x,y,w,h}, polygon:[{x,y}], raw_bytes}
    """
    results = []
    decoded = pyzbar.decode(image)
    for d in decoded:
        x, y, w, h = d.rect
        poly = [{'x': p.x, 'y': p.y} for p in d.polygon] if d.polygon else []
        try:
            data = d.data.decode('utf-8')
        except Exception:
            data = d.data.hex()
        results.append({
            'type': d.type,
            'data': data,
            'bbox': {'x': x, 'y': y, 'w': w, 'h': h},
            'polygon': poly,
            'raw_bytes': d.data
        })
    return results
