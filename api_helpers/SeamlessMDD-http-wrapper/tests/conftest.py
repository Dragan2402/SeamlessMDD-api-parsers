from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
import types
import pytest


@pytest.fixture(scope="session")
def wrapper_root() -> Path:
    # tests/ -> SeamlessMDD-http-wrapper/
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def app(wrapper_root):
    """Load the Flask app from its file path so the hyphen in the folder name is not an issue."""
    app_path = wrapper_root / "app" / "app.py"
    # Ensure "app" package (inside SeamlessMDD-http-wrapper) is importable
    wrapper_root_str = str(wrapper_root)
    if wrapper_root_str not in sys.path:
        sys.path.insert(0, wrapper_root_str)
    spec = importlib.util.spec_from_file_location("wrapper_app", str(app_path))
    module = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    assert spec and spec.loader, "Unable to create module spec for app.py"
    spec.loader.exec_module(module)  # type: ignore[assignment]
    flask_app = module.app
    flask_app.config.update(TESTING=True)
    return flask_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def sample_file_path(wrapper_root) -> str:
    return str(wrapper_root / "app" / "http" / "sample_files" / "F1.html")
