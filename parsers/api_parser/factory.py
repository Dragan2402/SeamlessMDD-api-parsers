from typing import Optional, Union

from .api_parser_interface import IApiParser
from .implementation.http_api_parser import HttpApiParser
from .implementation.lxml_http_api_parser import LxmlHttpApiParser
from .types import ApiParserType


class ApiParserFactory:
    """Factory for creating API parser implementations by type string."""

    @staticmethod
    def create(
        parser_type: Union[str, ApiParserType],
        base_url: Optional[str] = None,
        default_file_path: Optional[str] = None,
    ) -> IApiParser:
        key = (
            (
                parser_type.value
                if isinstance(parser_type, ApiParserType)
                else str(parser_type)
            )
            .strip()
            .lower()
        )
        if key in (ApiParserType.HTTP.value, "httpapi", "http_api"):
            return HttpApiParser(
                base_url=base_url or "http://127.0.0.1:5000",
                default_file_path=default_file_path,
            )
        if key in (ApiParserType.LXML_HTTP.value, "lxml", "lxml_http_api"):
            return LxmlHttpApiParser(
                base_url=base_url or "http://127.0.0.1:8001",
                default_file_path=default_file_path,
            )

        raise ValueError(f"Unknown API parser type: {parser_type}")
