#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)


@app.get("/")
def index():
    return "OK: k8s-test-app is running"


@app.get("/healthz")
def healthz():
    return "healthy"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
