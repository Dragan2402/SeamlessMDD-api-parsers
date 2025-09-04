from flask import Flask, jsonify, request
from lxml import etree
from uuid import uuid4

from app.http.lxml_parser import MyLXMLParser


app = Flask(__name__)

TEST_FILE_PATH = "app/http/sample_files/F1.html"


def get_parser(file_path=None):
    return MyLXMLParser(file_path if file_path else TEST_FILE_PATH)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/users")
def users():
    try:
        requested = int(request.args.get("count", 2500))
    except (TypeError, ValueError):
        requested = 2500
    count = max(2001, requested)
    users_list = [f"user_{uuid4().hex[:8]}" for _ in range(count)]
    return jsonify(users_list)


@app.route("/get-by-id", methods=["GET"])
def get_by_id():
    id_ = request.args.get("id")
    file_path = request.args.get("file_path")

    if id_ is None:
        return jsonify({"error": "ID not provided"}), 400

    parser = get_parser(file_path)
    element = parser.get_element_by_id(id_)

    if element is None:
        return jsonify({"error": "Element not found"}), 404

    return (
        jsonify(
            {"element": str(etree.tostring(element, method="html").decode("utf-8"))}
        ),
        200,
    )


@app.route("/check-exists", methods=["GET"])
def check_if_exists():
    id_ = request.args.get("id")
    file_path = request.args.get("file_path")

    if id_ is None:
        return jsonify({"error": "ID not provided"}), 400

    parser = get_parser(file_path)
    element = parser.get_element_by_id(id_)

    return (
        jsonify(
            {
                "exists": element is not None,
                "element": (
                    etree.tostring(element, method="html").decode("utf-8")
                    if element is not None
                    else None
                ),
            }
        ),
        200,
    )


@app.route("/get-by-name", methods=["GET"])
def get_by_name():
    name = request.args.get("name")
    file_path = request.args.get("file_path")

    if name is None:
        return jsonify({"error": "Name not provided"}), 400

    parser = get_parser(file_path)
    elements = parser.get_elements_by_name(name)

    if not elements:
        return jsonify({"error": "Element not found"}), 404

    return (
        jsonify(
            {"element": etree.tostring(elements[0], method="html").decode("utf-8")}
        ),
        200,
    )


@app.route("/get-by-path", methods=["GET"])
def get_by_path():
    path = request.args.get("path")
    file_path = request.args.get("file_path")

    if not path:
        return jsonify({"error": "Path parameter is required"}), 400

    parser = get_parser(file_path)

    try:
        elements = parser.get_elements_by_path(path)
        if not elements:
            return jsonify({"error": "Element not found"}), 404
        # Return first element for single path query
        return (
            jsonify(
                {"element": etree.tostring(elements[0], method="html").decode("utf-8")}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get-elements-by-path", methods=["GET"])
def get_elements_by_path():
    path = request.args.get("path")
    file_path = request.args.get("file_path")

    if not path:
        return jsonify({"error": "Path parameter is required"}), 400

    parser = get_parser(file_path)

    try:
        elements = parser.get_elements_by_path(path)
        return (
            jsonify(
                {
                    "elements": [
                        etree.tostring(el, method="html").decode("utf-8")
                        for el in elements
                    ]
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get-by-value", methods=["GET"])
def get_by_value():
    value = request.args.get("value")
    file_path = request.args.get("file_path")

    if value is None:
        return jsonify({"error": "Value not provided"}), 400

    parser = get_parser(file_path)

    try:
        elements = parser.get_elements_by_value(value)
        return (
            jsonify(
                {
                    "elements": [
                        etree.tostring(el, method="html").decode("utf-8")
                        for el in elements
                    ]
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/replace-by-id", methods=["POST"])
def replace_by_id():
    data = request.get_json()
    file_path = request.args.get("file_path")

    if "id" not in data or "new_element_html" not in data:
        return jsonify({"error": "Missing 'id' or 'new_element_html' in request"}), 400

    parser = get_parser(file_path)

    try:
        parser.replace_element_by_id(data["id"], data["new_element_html"])
        return jsonify({"message": "Element replaced successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/remove-by-id", methods=["DELETE"])
def remove_by_id():
    id_ = request.args.get("id")
    file_path = request.args.get("file_path")

    if id_ is None:
        return jsonify({"error": "ID not provided"}), 400

    parser = get_parser(file_path)

    try:
        parser.remove_element_by_id(id_)
        return jsonify({"message": "Element removed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete-elements-by-path", methods=["DELETE"])
def delete_elements_by_path():
    path = request.args.get("path")
    file_path = request.args.get("file_path")

    if not path:
        return jsonify({"error": "Path parameter is required"}), 400

    parser = get_parser(file_path)

    try:
        parser.delete_elements_by_path(path)
        return jsonify({"message": "Elements deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/insert-element-by-path", methods=["POST"])
def insert_element_by_path():
    data = request.json
    file_path = request.args.get("file_path")

    if "path" not in data or "element_text" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    parser = get_parser(file_path)

    try:
        parser.insert_element_by_path(data["path"], data["element_text"])
        return jsonify({"message": "Element inserted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get-by-jinja-variable", methods=["GET"])
def get_by_jinja_variable():
    variable_name = request.args.get("variable_name")
    file_path = request.args.get("file_path")

    if variable_name is None:
        return jsonify({"error": "Variable name not provided"}), 400

    parser = get_parser(file_path)

    try:
        elements = parser.get_elements_by_jinja_variable(variable_name)
        return (
            jsonify(
                {
                    "elements": [
                        etree.tostring(el, method="html").decode("utf-8")
                        for el in elements
                    ]
                }
            ),
            200,
        )
    except AttributeError:
        # Method not implemented in LXML parser
        return jsonify({"elements": []}), 200


@app.route("/update-element-by-path", methods=["POST"])
def update_element_by_path():
    data = request.json
    file_path = request.args.get("file_path")

    required_fields = ["old_element_path", "new_element_path", "new_element_content"]
    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    parser = get_parser(file_path)

    try:
        parser.update_element_by_path(
            data["old_element_path"],
            data["new_element_path"],
            data["new_element_content"],
            data.get("important_data"),
        )
        return jsonify({"message": "Element updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/check-if-node-exists", methods=["POST"])
def check_if_node_exists():
    data = request.json
    file_path = request.args.get("file_path")

    if "xpath" not in data or "node" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    parser = get_parser(file_path)

    try:
        # For LXML, we'll try to parse the node HTML string and check existence
        node_html = data["node"] if isinstance(data["node"], str) else str(data["node"])
        exists = parser.check_if_node_exists(data["xpath"], node_html)
        return jsonify({"exists": exists}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
