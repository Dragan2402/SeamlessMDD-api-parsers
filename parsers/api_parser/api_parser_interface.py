from abc import ABCMeta, abstractmethod
from typing import Any, Iterable, Tuple, Optional


class IApiParser(metaclass=ABCMeta):
    """
    Interface for API-backed parsers. Implementations should communicate with
    external services (e.g., HTTP APIs) but normalize return types to the
    structures defined here so that callers depend only on this interface.
    """

    # Retrieval
    @abstractmethod
    def get_element_by_id(self, id_: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def check_if_element_exists(self, id_: str) -> Tuple[bool, Optional[Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_element_by_name(self, name: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_element_by_path(self, path: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_elements_by_value(self, value: str) -> Iterable[Any]:
        raise NotImplementedError

    @abstractmethod
    def get_elements_by_jinja_variable(self, variable_name: str) -> Iterable[Any]:
        raise NotImplementedError

    # Mutation
    @abstractmethod
    def replace_element_by_id(self, id_: str, new_element_html: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def remove_element_by_id(self, id_: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_element_by_path(
        self,
        old_element_path: str,
        new_element_path: str,
        new_element_content: str,
        important_data: Optional[Iterable[str]] = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_elements_by_path(self, path: str) -> Iterable[Any]:
        raise NotImplementedError

    @abstractmethod
    def delete_elements_by_path(self, path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def insert_element_by_path(self, path: str, element_text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def check_if_node_exists(self, xpath: str, node_html: str) -> bool:
        """
        node_html is a string representation of a node to be checked within
        the xpath context. Implementations should perform the appropriate
        normalization necessary for the underlying API.
        """
        raise NotImplementedError
