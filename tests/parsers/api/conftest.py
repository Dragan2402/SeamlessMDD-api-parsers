import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest
import requests


def _run_flask_app():
    # Run HTTP wrapper Flask app as a separate process
    project_root = Path(__file__).resolve().parents[3]  # .../SeamlessMDD-api-parsers
    wrapper_app_root = project_root / "api_helpers/SeamlessMDD-http-wrapper"
    app_file = wrapper_app_root / "app/app.py"

    # Set environment variables
    env = os.environ.copy()
    env["FLASK_APP"] = str(app_file)
    env["PYTHONPATH"] = str(wrapper_app_root)

    # Run Flask app as subprocess
    process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            f"import sys; sys.path.insert(0, r'{wrapper_app_root}'); from app.app import app; app.run(host='127.0.0.1', port=8000, debug=False, use_reloader=False)",
        ],
        env=env,
        cwd=str(wrapper_app_root),
    )

    # Store process for cleanup (though it will be daemon)
    _run_flask_app.process = process


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
    # Run LXML parser Flask app as a separate process
    project_root = Path(__file__).resolve().parents[3]  # .../SeamlessMDD-api-parsers
    lxml_app_root = project_root / "api_helpers/SeamlessMDD-lxml-http-parser"
    app_file = lxml_app_root / "app/app.py"

    # Set environment variables
    env = os.environ.copy()
    env["FLASK_APP"] = str(app_file)
    env["PYTHONPATH"] = str(lxml_app_root)

    # Run Flask app as subprocess
    process = subprocess.Popen(
        [
            sys.executable,
            "-c",
            f"import sys; sys.path.insert(0, r'{lxml_app_root}'); from app.app import app; app.run(host='127.0.0.1', port=8001, debug=False, use_reloader=False)",
        ],
        env=env,
        cwd=str(lxml_app_root),
    )

    # Store process for cleanup (though it will be daemon)
    _run_lxml_flask_app.process = process


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
