from __future__ import annotations

from pathlib import Path
from typing import Generator

import pytest
from flask import Flask

from app.app import app as flask_app


@pytest.fixture()
def app() -> Generator[Flask, None, None]:
    flask_app.config.update({"TESTING": True})
    yield flask_app


@pytest.fixture()
def client(app: Flask):
    return app.test_client()


@pytest.fixture()
def sample_file_path() -> str:
    return str(
        Path(__file__).resolve().parents[1]
        / "app"
        / "http"
        / "sample_files"
        / "F1.html"
    )
