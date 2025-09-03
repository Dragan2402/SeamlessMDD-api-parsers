from enum import Enum


class ApiParserType(str, Enum):
    HTTP = "http"
    LXML_HTTP = "lxml_http"
