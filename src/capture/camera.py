"""
Camera capture helper. Tries Picamera2 (libcamera wrapper) first, then falls back to OpenCV VideoCapture(V4L2).
Returns an OpenCV BGR numpy array.
"""

from typing import Optional
import cv2
import numpy as np


def capture_frame(timeout: int = 5) -> Optional[np.ndarray]:
    """Capture a single frame from the CSI camera or first available camera.
    Returns BGR image (numpy array) or None on failure.
    """
    # Try Picamera2 (libcamera) if installed
    try:
        from picamera2 import Picamera2
        picam = Picamera2()
        # Use a simple preview configuration; Picamera2 will choose defaults for resolution
        picam.configure(picam.create_preview_configuration())
        picam.start()
        frame = picam.capture_array(timeout=timeout)
        picam.stop()
        return frame
    except Exception:
        # Picamera2 not available or failed; fall through to OpenCV
        pass

    # Fallback to OpenCV VideoCapture (V4L2)
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return None
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None
        return frame
    except Exception:
        return None
