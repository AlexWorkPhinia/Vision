"""
Simple OCR wrapper using pytesseract. Returns text and confidence.
"""
from typing import Tuple, Dict
import pytesseract
from PIL import Image
import numpy as np
import cv2


def _to_pil(image: np.ndarray) -> Image.Image:
    # OpenCV BGR -> RGB
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def ocr_image(image: np.ndarray, lang: str = 'eng') -> Dict:
    """Run Tesseract OCR on an OpenCV image. Returns {text, mean_conf, words: [{text, conf, bbox}]}
    """
    pil = _to_pil(image)
    data = pytesseract.image_to_data(pil, lang=lang, output_type=pytesseract.Output.DICT)
    words = []
    confidences = []
    n = len(data.get('text', []))
    for i in range(n):
        txt = data['text'][i].strip()
        if not txt:
            continue
        conf = int(data['conf'][i]) if data['conf'][i].isdigit() else -1
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        words.append({'text': txt, 'conf': conf, 'bbox': {'x': x, 'y': y, 'w': w, 'h': h}})
        if conf >= 0:
            confidences.append(conf)
    mean_conf = int(sum(confidences) / len(confidences)) if confidences else -1
    return {'text': '\n'.join(w['text'] for w in words), 'mean_conf': mean_conf, 'words': words}


def ocr_region(image: np.ndarray, bbox: Dict, lang: str = 'eng') -> Dict:
    x, y, w, h = bbox['x'], bbox['y'], bbox['w'], bbox['h']
    h_img, w_img = image.shape[:2]
    # clip
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(w_img, x + w)
    y1 = min(h_img, y + h)
    region = image[y0:y1, x0:x1]
    return ocr_image(region, lang=lang)
