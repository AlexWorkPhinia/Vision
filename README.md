PiZero Vision — Camera barcode/QR + OCR service

Overview

Lightweight Python service for Raspberry Pi Zero 2 W that captures images from a CSI or USB camera, decodes barcodes/QR codes and runs OCR, and exposes structured JSON via a FastAPI HTTP API.

Key features
- Capture from CSI camera (libcamera/Picamera2 preferred) or V4L2 fallback
- Barcode/QR decoding via pyzbar/zbar
- OCR using Tesseract (pytesseract)
- FastAPI HTTP API with /scan and /upload endpoints

Quickstart (development)

1. Clone repository and change to project root
2. Install system deps (Ubuntu/Raspbian):
   sudo apt update && sudo apt install -y python3-venv python3-pip tesseract-ocr libzbar0 libopenblas-dev

3. Run setup script:
   bash scripts/setup_env.sh

4. Start the app:
   . .venv/bin/activate
   bash scripts/run_uvicorn.sh

API examples

- Capture from camera and scan:
  curl http://<pi>:8000/scan

- Upload an image to scan:
  curl -F "image=@tests/fixtures/frame1.jpg" http://<pi>:8000/upload

Notes for Raspberry Pi Zero 2 W
- Pi has 512MB RAM and modest CPU. Prefer system OpenCV (apt) and tesseract via apt. Prebuilt opencv-python wheels may not be compatible; if pip install fails, run: sudo apt install -y python3-opencv
- Tune OCR by resizing regions, using tessdata-lite or limiting page segmentation mode.

Project layout

- src/capture: camera capture helper
- src/processing: barcode and OCR wrappers
- src/api: FastAPI app and endpoints
- scripts/: helper scripts (setup, run)
- tests/: test fixtures and test code

Next steps
- Implement unit and integration tests using recorded frames
- Add systemd unit for automatic start on boot (deploy/vision-app.service)
- Performance-tune pipeline to keep memory <350MB and latency low

