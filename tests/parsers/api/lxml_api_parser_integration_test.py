from pathlib import Path

import pytest
from parsers.api_parser.implementation.lxml_http_api_parser import LxmlHttpApiParser


def _sample_file_path() -> str:
    project_root = Path(__file__).resolve().parents[3]
    workspace_root = project_root.parent
    return str(
        workspace_root
        / "SeamlessMDD-lxml-http-parser"
        / "app"
        / "http"
        / "sample_files"
        / "F1.html"
    )


def _make_parser() -> LxmlHttpApiParser:
    return LxmlHttpApiParser(
        base_url="http://127.0.0.1:8001", default_file_path=_sample_file_path()
    )


def test_get_by_id(lxml_api_server):
    parser = _make_parser()
    element = parser.get_element_by_id("1")
    assert element is not None


def test_check_exists_true(lxml_api_server):
    parser = _make_parser()
    exists, element = parser.check_if_element_exists("1")
    assert exists is True
    assert element is not None


def test_get_by_name(lxml_api_server):
    parser = _make_parser()
    element = parser.get_element_by_name("nesto")
    assert element is not None


def test_elements_by_path_and_delete_and_insert(lxml_api_server):
    parser = _make_parser()
    path = "//ul/li[@id='2']"
    elements = parser.get_elements_by_path(path)
    assert isinstance(elements, list)

    parser.delete_elements_by_path(path)
    parser.insert_element_by_path("//ul", '<li id="2">Field (F2)</li>')


def test_update_element_by_path(lxml_api_server):
    parser = _make_parser()
    old_path = "//ul/li[@id='1']"
    new_content = '<li id="1">Field (F1) - Updated</li>'
    parser.update_element_by_path(old_path, "//li[@id='1']", new_content)
    elements = parser.get_elements_by_path("//ul/li[@id='1']")
    assert isinstance(elements, list)


def test_get_by_id_not_found_raises(lxml_api_server):
    parser = _make_parser()
    with pytest.raises(Exception):
        parser.get_element_by_id("999")
