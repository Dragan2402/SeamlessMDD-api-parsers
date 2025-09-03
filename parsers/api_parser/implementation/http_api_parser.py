from __future__ import annotations
import json
from typing import Any, Iterable, Tuple, Optional

import requests

from ..api_parser_interface import IApiParser


class HttpApiParser(IApiParser):
    """
    HTTP implementation of IApiParser that calls the Flask app endpoints in
    SeamlessMDD-http-wrapper/app/app.py. It encapsulates the base URL and file
    path handling so callers only provide semantic parameters.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
        default_file_path: Optional[str] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.default_file_path = default_file_path

    # Internal helpers
    def _params(self, extra: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if self.default_file_path:
            params["file_path"] = self.default_file_path
        if extra:
            params.update({k: v for k, v in extra.items() if v is not None})
        return params

    def _get(
        self, path: str, params: Optional[dict[str, Any]] = None
    ) -> requests.Response:
        url = f"{self.base_url}{path}"
        response = requests.get(url, params=self._params(params))
        response.raise_for_status()
        return response

    def _post(self, path: str, json_body: dict[str, Any]) -> requests.Response:
        url = f"{self.base_url}{path}"
        response = requests.post(url, params=self._params(), json=json_body)
        response.raise_for_status()
        return response

    def _delete(
        self, path: str, params: Optional[dict[str, Any]] = None
    ) -> requests.Response:
        url = f"{self.base_url}{path}"
        response = requests.delete(url, params=self._params(params))
        response.raise_for_status()
        return response

    # Retrieval
    def get_element_by_id(self, id_: str) -> Any:
        r = self._get("/get-by-id", {"id": id_})
        data = r.json()
        return data.get("element")

    def check_if_element_exists(self, id_: str) -> Tuple[bool, Optional[Any]]:
        r = self._get("/check-exists", {"id": id_})
        data = r.json()
        return bool(data.get("exists")), data.get("element")

    def get_element_by_name(self, name: str) -> Any:
        r = self._get("/get-by-name", {"name": name})
        data = r.json()
        return data.get("element")

    def get_element_by_path(self, path: str) -> Any:
        try:
            r = self._get("/get-by-path", {"path": path})
            data = r.json()
            return data.get("element")
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 501:
                raise NotImplementedError("get_element_by_path not supported by API")
            raise

    def get_elements_by_value(self, value: str) -> Iterable[Any]:
        r = self._get("/get-by-value", {"value": value})
        data = r.json()
        return data.get("elements", [])

    def get_elements_by_jinja_variable(self, variable_name: str) -> Iterable[Any]:
        r = self._get("/get-by-jinja-variable", {"variable_name": variable_name})
        data = r.json()
        return data.get("elements", [])

    # Mutation
    def replace_element_by_id(self, id_: str, new_element_html: str) -> None:
        body = {"id": id_, "new_element_html": new_element_html}
        self._post("/replace-by-id", body)

    def remove_element_by_id(self, id_: str) -> None:
        self._delete("/remove-by-id", {"id": id_})

    def update_element_by_path(
        self,
        old_element_path: str,
        new_element_path: str,
        new_element_content: str,
        important_data: Optional[Iterable[str]] = None,
    ) -> None:
        body = {
            "old_element_path": old_element_path,
            "new_element_path": new_element_path,
            "new_element_content": new_element_content,
        }
        if important_data is not None:
            body["important_data"] = list(important_data)
        self._post("/update-element-by-path", body)

    def get_elements_by_path(self, path: str) -> Iterable[Any]:
        r = self._get("/get-elements-by-path", {"path": path})
        data = r.json()
        return data.get("elements", [])

    def delete_elements_by_path(self, path: str) -> None:
        self._delete("/delete-elements-by-path", {"path": path})

    def insert_element_by_path(self, path: str, element_text: str) -> None:
        body = {"path": path, "element_text": element_text}
        self._post("/insert-element-by-path", body)

    def check_if_node_exists(self, xpath: str, node_html: str) -> bool:
        body = {"xpath": xpath, "node": node_html}
        r = self._post("/check-if-node-exists", body)
        data = r.json()
        return bool(data.get("exists", False))

    @staticmethod
    def _parse_json_response(response: requests.Response) -> Any:
        try:
            return response.json()
        except json.JSONDecodeError:
            # Fall back to raw text if not JSON (Flask returns strings as JSON
            # encoded strings, which .json() handles; this is a safety net).
            return response.text
