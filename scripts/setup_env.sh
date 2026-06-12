#!/usr/bin/env bash
set -euo pipefail

# Apt dependencies (run as root / sudo)
# Note: On Pi Zero 2W, install system packages for best compatibility
apt update
apt install -y python3-venv python3-pip tesseract-ocr libzbar0 libtiff5 libjpeg8 libopenblas-dev

# Create venv and install python deps
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Note: If opencv-python wheel fails on Pi, install libopencv via apt: apt install -y python3-opencv
echo "Setup complete. Activate with: . .venv/bin/activate" 
