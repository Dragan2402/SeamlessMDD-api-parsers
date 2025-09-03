from __future__ import annotations

from flask.testing import FlaskClient


def test_root(client: FlaskClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Hello, World!" in resp.get_data(as_text=True)


def test_get_by_id_success(client: FlaskClient, sample_file_path: str):
    resp = client.get(
        "/get-by-id", query_string={"id": "1", "file_path": sample_file_path}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data and "element" in data
    assert "Field (F1)" in data["element"]


def test_get_by_id_missing_param(client: FlaskClient):
    resp = client.get("/get-by-id")
    assert resp.status_code == 400


def test_get_by_id_not_found(client: FlaskClient, sample_file_path: str):
    resp = client.get(
        "/get-by-id", query_string={"id": "999", "file_path": sample_file_path}
    )
    assert resp.status_code == 404


def test_get_by_name_success(client: FlaskClient, sample_file_path: str):
    resp = client.get(
        "/get-by-name", query_string={"name": "nesto", "file_path": sample_file_path}
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data and "element" in data
    assert 'class="container"' in data["element"] or "<div" in data["element"]


def test_get_by_name_missing_param(client: FlaskClient):
    resp = client.get("/get-by-name")
    assert resp.status_code == 400


def test_get_by_value_success(client: FlaskClient, sample_file_path: str):
    resp = client.get(
        "/get-by-value",
        query_string={"value": "Field (F1)", "file_path": sample_file_path},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data and "elements" in data and isinstance(data["elements"], list)
    assert any("Field (F1)" in el for el in data["elements"])


def test_get_by_value_missing_param(client: FlaskClient):
    resp = client.get("/get-by-value")
    assert resp.status_code == 400


def test_get_elements_by_path_success(client: FlaskClient, sample_file_path: str):
    resp = client.get(
        "/get-elements-by-path",
        query_string={"path": "/html/body/div", "file_path": sample_file_path},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data and "elements" in data and isinstance(data["elements"], list)
    assert len(data["elements"]) >= 1


def test_delete_elements_by_path_success(client: FlaskClient, sample_file_path: str):
    resp = client.delete(
        "/delete-elements-by-path",
        query_string={"path": "/html/body/div[1]", "file_path": sample_file_path},
    )
    assert resp.status_code == 200
    assert resp.get_json().get("message") == "Elements deleted successfully"


def test_insert_element_by_path_success(client: FlaskClient, sample_file_path: str):
    payload = {
        "path": "/html/body/div/ul",
        "element_text": '<li id="3">New Inserted Element</li>',
    }
    resp = client.post(
        "/insert-element-by-path",
        json=payload,
        query_string={"file_path": sample_file_path},
    )
    assert resp.status_code == 200
    assert resp.get_json().get("message") == "Element inserted successfully"
