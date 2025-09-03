from __future__ import annotations

import json
from typing import Any, Iterable, Tuple, Optional

import requests
from lxml import html as lxml_html

from ..api_parser_interface import IApiParser


class LxmlHttpApiParser(IApiParser):
    """
    HTTP implementation of IApiParser that calls the Flask app endpoints in
    SeamlessMDD-lxml-http-parser/app/app.py.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8001",
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
        try:
            r = self._get("/get-by-id", {"id": id_})
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                # Aligns with check_if_element_exists behavior
                raise
            raise
        data = r.json()
        return data.get("element")

    def check_if_element_exists(self, id_: str) -> Tuple[bool, Optional[Any]]:
        try:
            r = self._get("/get-by-id", {"id": id_})
            data = r.json()
            return True, data.get("element")
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                return False, None
            raise

    def get_element_by_name(self, name: str) -> Any:
        r = self._get("/get-by-name", {"name": name})
        data = r.json()
        return data.get("element")

    def get_element_by_path(self, path: str) -> Any:
        # The LXML server supports getting elements by path (plural). Return first or None.
        r = self._get("/get-elements-by-path", {"path": path})
        data = r.json()
        elements = data.get("elements") or []
        return elements[0] if elements else None

    def get_elements_by_value(self, value: str) -> Iterable[Any]:
        r = self._get("/get-by-value", {"value": value})
        data = r.json()
        return data.get("elements", [])

    def get_elements_by_jinja_variable(self, variable_name: str) -> Iterable[Any]:
        # Best-effort: search anywhere text contains the variable name
        xpath = f"//*[contains(normalize-space(.), '{variable_name}')]"
        r = self._get("/get-elements-by-path", {"path": xpath})
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
        # Emulate update by deleting old then inserting new under parent of old path
        # Parent path derived by trimming the last path segment
        if "/" not in old_element_path:
            raise ValueError("Invalid XPath for update: missing parent segment")
        parent_path = old_element_path.rsplit("/", 1)[0]
        self.delete_elements_by_path(old_element_path)
        self.insert_element_by_path(parent_path, new_element_content)

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
        # Parse node HTML and match on text content
        try:
            node = lxml_html.fromstring(node_html)
            text = (node.text_content() or "").strip()
        except Exception:
            text = node_html.strip()
        pred = (
            f"normalize-space(text())='{text}'"
            if text
            else "string-length(normalize-space(text()))=0"
        )
        path = f"{xpath}[{pred}]"
        r = self._get("/get-elements-by-path", {"path": path})
        data = r.json()
        elements = data.get("elements", [])
        return bool(elements)

    @staticmethod
    def _parse_json_response(response: requests.Response) -> Any:
        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text
