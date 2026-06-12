#!/usr/bin/env bash
# Run the FastAPI app locally
PYTHONPATH="$(pwd)" exec .venv/bin/uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 1
