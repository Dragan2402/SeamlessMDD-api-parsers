from pathlib import Path

from parsers.api_parser.implementation.lxml_http_api_parser import LxmlHttpApiParser


def _sample_file_path() -> str:
    project_root = Path(__file__).resolve().parents[3]  # .../SeamlessMDD-api-parsers
    return str(
        project_root
        / "api_helpers"
        / "SeamlessMDD-lxml-http-parser"
        / "app"
        / "http"
        / "sample_files"
        / "F1.html"
    )


def test_get_by_id(lxml_api_server):
    parser = LxmlHttpApiParser(default_file_path=_sample_file_path())
    element = parser.get_element_by_id("1")
    assert element is not None


def test_check_exists_true(lxml_api_server):
    parser = LxmlHttpApiParser(default_file_path=_sample_file_path())
    exists, element = parser.check_if_element_exists("1")
    assert exists is True
    assert element is not None


def test_get_by_name(lxml_api_server):
    parser = LxmlHttpApiParser(default_file_path=_sample_file_path())
    element = parser.get_element_by_name("nesto")
    assert element is not None


def test_get_by_value(lxml_api_server):
    parser = LxmlHttpApiParser(default_file_path=_sample_file_path())
    elements = list(parser.get_elements_by_value("Field (F1)"))
    assert len(elements) >= 1


def test_elements_by_path_and_delete_and_insert(lxml_api_server):
    parser = LxmlHttpApiParser(default_file_path=_sample_file_path())
    path = "//ul/li[@id='2']"
    elements = parser.get_elements_by_path(path)
    assert isinstance(elements, list)

    # Call mutation endpoints (state may not persist across requests)
    parser.delete_elements_by_path(path)
    parser.insert_element_by_path("//ul", '<li id="2">Field (F2)</li>')


def test_update_element_by_path(lxml_api_server):
    parser = LxmlHttpApiParser(default_file_path=_sample_file_path())
    old_path = "//ul/li[@id='1']"
    new_path = "//li[@id='1']"
    new_content = '<li id="1">Field (F1) - Updated</li>'
    parser.update_element_by_path(old_path, new_path, new_content)
    # Ensure read endpoint remains functional
    elements = parser.get_elements_by_path("//ul/li[@id='1']")
    assert isinstance(elements, list)
