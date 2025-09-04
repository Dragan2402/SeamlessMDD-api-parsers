# SeamlessMDD API Parsers

This repository is a fork of SeamlessMDD that introduces a generic API parsing service layer. The project extends the original functionality by adding HTTP API-based parsers and testing infrastructure.

## Project Overview

### API Parser Service (`parsers/api_parser/`)

The core addition is a generic API parser service that provides a standardized interface for HTML document manipulation through HTTP APIs. The service is designed to be extensible and implementation-agnostic, allowing different HTML parsing strategies to be used interchangeably.

#### Interface Overview (`api_parser_interface.py`)

The `IApiParser` interface defines a comprehensive set of operations for HTML document manipulation:

1. **Element Retrieval Methods**

   ```python
   def get_element_by_id(self, id_: str) -> Any
   def get_element_by_name(self, name: str) -> Any
   def get_element_by_path(self, path: str) -> Any
   def get_elements_by_value(self, value: str) -> Iterable[Any]
   def get_elements_by_jinja_variable(self, variable_name: str) -> Iterable[Any]
   ```

   These methods provide various ways to locate and retrieve HTML elements using different selectors.

2. **Element Existence Checking**

   ```python
   def check_if_element_exists(self, id_: str) -> Tuple[bool, Optional[Any]]
   def check_if_node_exists(self, xpath: str, node_html: str) -> bool
   ```

   Methods to verify element existence without necessarily retrieving them.

3. **Element Manipulation**

   ```python
   def replace_element_by_id(self, id_: str, new_element_html: str) -> None
   def remove_element_by_id(self, id_: str) -> None
   def update_element_by_path(
       self,
       old_element_path: str,
       new_element_path: str,
       new_element_content: str,
       important_data: Optional[Iterable[str]] = None
   ) -> None
   ```

   Methods for modifying existing elements in the document.

4. **Path-based Operations**

   ```python
   def get_elements_by_path(self, path: str) -> Iterable[Any]
   def delete_elements_by_path(self, path: str) -> None
   def insert_element_by_path(self, path: str, element_text: str) -> None
   ```

   XPath-based operations for more complex document traversal and manipulation.

#### Implementation Strategy

The interface is implemented by two different parsers:

1. **HTML Parser Implementation** - Uses Python's built-in HTML parser
2. **LXML Parser Implementation** - Uses the lxml library for more robust parsing

Each implementation:

- Provides consistent return types regardless of underlying parser
- Handles error cases gracefully
- Supports both synchronous and asynchronous operations
- Maintains document integrity during operations

### API Helper Services (`api_helpers/`)

To demonstrate and test the API parser functionality, two Flask applications were created that expose the parsing functionality through RESTful endpoints:

#### 1. SeamlessMDD-http-wrapper

- Located in `api_helpers/SeamlessMDD-http-wrapper/`
- Implements HTML parsing using Python's built-in HTML parser
- Provides a complete test suite
- Runs on port 8000 by default

**Key Endpoints:**

```
GET  /get-by-id            - Retrieve element by ID
GET  /get-by-name          - Retrieve element by name
GET  /get-by-path          - Retrieve single element by XPath
GET  /get-elements-by-path - Retrieve multiple elements by XPath
GET  /check-exists         - Check if element exists
POST /update-element       - Update element content
POST /insert-element       - Insert new element at path
```

#### 2. SeamlessMDD-lxml-http-parser

- Located in `api_helpers/SeamlessMDD-lxml-http-parser/`
- Implements parsing using the lxml library for enhanced XPath support
- Provides identical REST interface with lxml-based implementation
- Runs on port 8001 by default

**Additional Features:**

- More robust HTML parsing through lxml
- Better handling of malformed HTML
- Enhanced XPath functionality
- Improved performance for large documents

**Common API Features:**

- All endpoints accept `file_path` parameter to specify target HTML file
- POST endpoints accept JSON body with operation details
- Responses return HTML content as strings for maximum compatibility
- Error responses include detailed messages for debugging
- Support for both relative and absolute XPath expressions

### Integration Tests

The project includes comprehensive integration tests that verify:

- Individual functionality of both HTTP and LXML parsers
- Compatibility between different parser implementations
- Correct handling of HTML documents through the API layer

Tests are located in:

- `tests/parsers/api/` - Core API parser tests
- Individual test suites in each helper service

## Project Setup

### Prerequisites

1. Python 3.x
2. Virtual environment
3. Git

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd SeamlessMDD-api-parsers
```

2. Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Unix/macOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r venv/requirements.txt
```

### Development Environment

The project includes a VS Code launch configuration (`launch.json.example`) that sets up:

1. **HTTP Parser Development Server**
   - Port: 8000
   - Debug enabled
   - Hot reload disabled

2. **LXML Parser Development Server**
   - Port: 8001
   - Debug enabled
   - Hot reload disabled

3. **Test Configurations**
   - HTTP Parser tests
   - LXML Parser tests
   - Combined parser integration tests

To use the launch configuration:

1. Copy `launch.json.example` to `.vscode/launch.json`
2. Adjust Python paths as needed for your environment
3. Use VS Code's Run and Debug feature to launch servers or run tests

## Running Tests

The project uses pytest for testing. To run tests:

```bash
# Run all tests
pytest

# Run specific test suites
pytest tests/parsers/api/  # API parser tests
pytest api_helpers/SeamlessMDD-http-wrapper/tests/  # HTTP parser tests
pytest api_helpers/SeamlessMDD-lxml-http-parser/tests/  # LXML parser tests
```
