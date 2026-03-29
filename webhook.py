import logging
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sync import sync_grist_to_radicale
import time
from datetime import datetime
import threading
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app)
app.config["APPLICATION_ROOT"] = "/webhook"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_prefix=1)

last_sync = 0.0
timer = None
lock = threading.Lock()
sync_lock = threading.Lock()

DEBOUNCE_SECONDS = 10


def sync_data():
    global last_sync
    last_sync = time.time()
    with sync_lock:
        logging.info("Syncing grist to radicale now..")
        sync_grist_to_radicale()


def run_sync():
    global timer
    with lock:
        timer = None
    sync_data()


@app.get("/health")
def health():
    return jsonify(
        {
            "ok": True,
            "last_sync": datetime.fromtimestamp(last_sync).strftime(
                "%d.%m.%Y %H:%M:%S"
            ),
        }
    )


@app.post("/webhook")
def webhook():
    global timer
    with lock:
        if timer is not None:
            timer.cancel()
        timer = threading.Timer(DEBOUNCE_SECONDS, run_sync)
        timer.start()
    return jsonify({"ok": True})
