from __future__ import annotations

from pathlib import Path
import pytest
import requests

from parsers.api_parser.implementation.http_api_parser import HttpApiParser


def _sample_file_path() -> str:
    project_root = Path(__file__).resolve().parents[3]
    workspace_root = project_root.parent
    return str(
        workspace_root
        / "SeamlessMDD-http-wrapper"
        / "app"
        / "http"
        / "sample_files"
        / "F1.html"
    )


def _make_parser() -> HttpApiParser:
    return HttpApiParser(default_file_path=_sample_file_path())


def test_get_element_by_path_not_implemented(api_server):
    parser = _make_parser()
    with pytest.raises(NotImplementedError):
        parser.get_element_by_path("/html/body/div")


def test_replace_and_remove_by_id(api_server):
    parser = _make_parser()
    parser.replace_element_by_id("1", "<div>New Content</div>")
    parser.remove_element_by_id("1")


def test_check_if_node_exists_true(api_server):
    parser = _make_parser()
    exists = parser.check_if_node_exists("/html/body/div/ul/li", "<li>Field (F1)</li>")
    assert exists is True


def test_check_if_node_exists_false(api_server):
    parser = _make_parser()
    exists = parser.check_if_node_exists("/html/body/div/ul/li", "<li>Not There</li>")
    assert exists is False


def test_get_elements_by_path_success(api_server):
    parser = _make_parser()
    elements = list(parser.get_elements_by_path("//ul/li"))
    assert isinstance(elements, list) and len(elements) >= 1


def test_delete_elements_by_path_success(api_server):
    parser = _make_parser()
    parser.delete_elements_by_path("//ul/li[@id='2']")


def test_insert_element_by_path_success(api_server):
    parser = _make_parser()
    parser.insert_element_by_path("//ul", '<li id="3">Inserted</li>')


def test_get_by_id_not_found_raises(api_server):
    parser = _make_parser()
    with pytest.raises(requests.HTTPError):
        parser.get_element_by_id("999")


def test_get_by_value_contains_expected(api_server):
    parser = _make_parser()
    elements = list(parser.get_elements_by_value("Field (F1)"))
    assert any("Field (F1)" in str(e) for e in elements)


def test_get_elements_by_jinja_variable_returns_list(api_server):
    parser = _make_parser()
    elements = list(parser.get_elements_by_jinja_variable("does_not_exist"))
    assert isinstance(elements, list)
