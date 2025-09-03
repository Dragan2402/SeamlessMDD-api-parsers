import pytest

from parsers.api_parser.factory import ApiParserFactory
from parsers.api_parser.implementation.http_api_parser import HttpApiParser
from parsers.api_parser.types import ApiParserType


def test_factory_http_default():
    parser = ApiParserFactory.create("http")
    assert isinstance(parser, HttpApiParser)


def test_factory_unknown():
    with pytest.raises(ValueError):
        ApiParserFactory.create("unknown")


def test_factory_enum():
    parser = ApiParserFactory.create(ApiParserType.HTTP)
    assert isinstance(parser, HttpApiParser)
