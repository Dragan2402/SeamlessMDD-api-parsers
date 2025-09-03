import os
import sys
import threading
import time
from pathlib import Path

import pytest
import requests


def _run_flask_app():
    # Ensure the Flask app module is importable
    project_root = Path(__file__).resolve().parents[3]  # .../SeamlessMDD
    workspace_root = project_root.parent  # .../Master Rad
    wrapper_app_root = workspace_root / "api_helpers/SeamlessMDD-http-wrapper"
    sys.path.insert(0, str(wrapper_app_root))
    from app.api.app import create_app  # type: ignore

    app = create_app()
    app.run(host="127.0.0.1", port=8000, debug=False, use_reloader=False)


@pytest.fixture(scope="session", autouse=True)
def api_server():
    # Start server once for the test session
    thread = threading.Thread(target=_run_flask_app, daemon=True)
    thread.start()

    # Wait for server readiness
    base_url = "http://127.0.0.1:8000/"
    for _ in range(100):
        try:
            requests.get(base_url, timeout=0.2)
            break
        except Exception:
            time.sleep(0.05)
    yield


def _run_lxml_flask_app():
    # Ensure the LXML Flask app module is importable
    project_root = Path(__file__).resolve().parents[3]  # .../SeamlessMDD
    workspace_root = project_root.parent  # .../Master Rad
    wrapper_app_root = workspace_root / "api_helpers/SeamlessMDD-lxml-http-parser"
    sys.path.insert(0, str(wrapper_app_root))
    from app.api.app import create_app  # type: ignore

    app = create_app()
    app.run(host="127.0.0.1", port=8001, debug=False, use_reloader=False)


@pytest.fixture(scope="session")
def lxml_api_server():
    # Start LXML server once for the test session
    thread = threading.Thread(target=_run_lxml_flask_app, daemon=True)
    thread.start()

    # Wait for server readiness
    base_url = "http://127.0.0.1:8001/"
    for _ in range(100):
        try:
            requests.get(base_url, timeout=0.2)
            break
        except Exception:
            time.sleep(0.05)
    yield
