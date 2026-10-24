"""Tiny ops-status API. Small on purpose: the point of this repo is the
Docker + Terraform + CI/CD around it, not the app itself."""

import os
import shutil
import socket
import time

from fastapi import FastAPI

APP_VERSION = os.getenv("APP_VERSION", "dev")
START_TIME = time.time()

app = FastAPI(title="ops-status-api")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    # APP_VERSION is injected at build time (git SHA) by the CI pipeline.
    return {"version": APP_VERSION}


@app.get("/status")
def status():
    total, used, free = shutil.disk_usage("/")
    return {
        "hostname": socket.gethostname(),
        "uptime_seconds": int(time.time() - START_TIME),
        "disk": {
            "total_gb": round(total / 1e9, 1),
            "used_percent": round(used / total * 100, 1),
        },
    }
