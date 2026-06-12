from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.api.scan import router as scan_router
from src.api.upload import router as upload_router
from src.api.health import router as health_router

app = FastAPI(title='PiZero Vision API', version='0.1')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app.include_router(scan_router, prefix='')
app.include_router(upload_router, prefix='')
app.include_router(health_router, prefix='')
