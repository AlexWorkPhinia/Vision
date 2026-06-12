from fastapi import APIRouter
import time
import psutil

router = APIRouter()
_start = time.time()


@router.get('/health')
async def health():
    mem = psutil.virtual_memory()
    return {'status': 'ok', 'uptime_seconds': int(time.time() - _start), 'memory_total_mb': int(mem.total / 1024 / 1024), 'memory_available_mb': int(mem.available / 1024 / 1024)}
