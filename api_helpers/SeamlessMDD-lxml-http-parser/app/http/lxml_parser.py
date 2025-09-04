from __future__ import annotations

from lxml import html, etree


class MyLXMLParser:
    def __init__(self, file_path: str | None = None):
        if file_path:
            try:
                # Try to read the file content first, then parse it
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.tree = html.fromstring(content)
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                # Fallback to empty HTML
                self.tree = html.fromstring("<html></html>")
        else:
            self.tree = html.fromstring("<html></html>")

    def get_element_by_id(self, id_: str):
        root = (
            self.tree.getroot()
            if isinstance(self.tree, etree._ElementTree)
            else self.tree
        )
        try:
            return root.get_element_by_id(str(id_), None)
        except KeyError:
            return None

    def get_elements_by_name(self, name: str):
        root = (
            self.tree.getroot()
            if isinstance(self.tree, etree._ElementTree)
            else self.tree
        )
        return root.xpath("//*[@name='%s']" % name)

    def get_elements_by_path(self, path: str):
        root = (
            self.tree.getroot()
            if isinstance(self.tree, etree._ElementTree)
            else self.tree
        )
        return root.xpath(path)

    def get_elements_by_value(self, value: str):
        root = (
            self.tree.getroot()
            if isinstance(self.tree, etree._ElementTree)
            else self.tree
        )
        matched = []
        for el in root.iter():
            try:
                text = el.text_content()  # type: ignore[attr-defined]
            except Exception:
                # Fallback for non-HTML elements
                text = el.text or ""
            if text and value in text:
                matched.append(el)
        return matched

    def replace_element_by_id(self, id_: str, new_element_html: str):
        root = (
            self.tree.getroot()
            if isinstance(self.tree, etree._ElementTree)
            else self.tree
        )
        element_to_replace = self.get_element_by_id(id_)
        if element_to_replace is None:
            raise ValueError("Element not found")
        new_element = html.fromstring(new_element_html)
        element_to_replace.addnext(new_element)
        parent = element_to_replace.getparent()
        parent.remove(element_to_replace)

    def remove_element_by_id(self, id_: str):
        element_to_remove = self.get_element_by_id(id_)
        if element_to_remove is None:
            raise ValueError("Element not found")
        parent = element_to_remove.getparent()
        parent.remove(element_to_remove)

    def delete_elements_by_path(self, path: str):
        for el in self.get_elements_by_path(path):
            parent = el.getparent()
            if parent is not None:
                parent.remove(el)

    def insert_element_by_path(self, path: str, element_text: str):
        root = (
            self.tree.getroot()
            if isinstance(self.tree, etree._ElementTree)
            else self.tree
        )
        targets = root.xpath(path)
        if not targets:
            raise ValueError("Path not found")
        container = targets[0]
        new_el = html.fromstring(element_text)
        container.append(new_el)

    def tostring(self) -> str:
        root = (
            self.tree.getroot()
            if isinstance(self.tree, etree._ElementTree)
            else self.tree
        )
        return etree.tostring(root, pretty_print=True, method="html").decode("utf-8")
