from fastapi import FastAPI
from datetime import datetime
from time import time

app = FastAPI()

@app.get("/health")
async def health():
    return {
        "nama": "Ayesha Nayla",
        "nrp": "5025231195",
        "status": "UP",
        "timestamp": datetime.now(),
        "uptime": time()
    }

