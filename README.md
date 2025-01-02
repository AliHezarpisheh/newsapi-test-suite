# NewsAPI Test Suite

## Overview
The **NewsAPI Test Suite** is an automation testing project designed to validate the functionality, reliability, and robustness of the [NewsAPI](https://newsapi.org/v2). This suite leverages **pytest** for unit testing, smoke testing, and includes a Behavior-Driven Development (BDD) demonstration. Additionally, comprehensive documentation and a Postman collection are provided for further reference.

## Prerequisites
- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) (optional, for dependency management)
- [pip](https://pip.pypa.io/en/stable/) (optional, as an alternative for dependency installation)

## Installation
1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Install Dependencies:**
   - Using Poetry:
     ```bash
     poetry env use 3.13 && poetry install && source .venv/bin/activate
     ```
   - Using pip:
     ```bash
     python3.13 -m virtualenv .venv && source .venv/bin/activate && pip install -r requirements.txt
     ```

3. **Environment Variables:**
   Create a `.env` file in the root directory of the project with the following format:
   ```env
   BASE_URL=https://newsapi.org/v2
   API_KEY=***
   RATE_LIMITED_API_KEY=***
   ```
   Replace `***` with your actual API keys.

## Running Tests

### Directory Structure
The test suite is located in the `tests/` directory and includes the following modules:
- `test_auth.py`: Tests related to authentication.
- `test_everything.py`: Tests for the "everything" endpoint.
- `test_top_headlines.py`: Tests for the "top headlines" endpoint.
- `test_sources.py`: Tests for the "sources" endpoint.

### Run Specific Test Modules
To run a specific test module, use:
```bash
pytest tests/<module_name>.py
```
Example:
```bash
pytest tests/test_auth.py
```

### Run Smoke Tests
Smoke tests are marked with `@pytest.mark.smoke`. To run only smoke tests:
```bash
pytest -m smoke
```

### Run Error Tests
Error cases are marked with `@pytest.mark.error`. To run only error tests:
```bash
pytest -m error
```

### Run BDD Tests
A Behavior-Driven Development (BDD) test is implemented in the `tests_bdd/` directory. To execute it:
```bash
pytest tests_bdd/
```

### Run All Tests
To run all test cases, execute the provided script:
```bash
./scripts/test.sh
```
**Note:** The API rate limit for a single API key in development mode is 186 requests per day. Ensure you have sufficient API keys or manage rate limits appropriately.

## Documentation
The following documents are provided in the `docs/` directory:

1. **Test Case Documentation:**
   - `API-Test-Cases-NewsAPI.xlsx`: Detailed documentation of all test cases.

2. **Additional Documentation:**
   - `metadata.txt`: Personal notes and thoughts during the testing process.
   - `API-Defects-Report.md`: Documentation of identified defects and inconsistencies in the API.

3. **Postman Collection:**
   - `News-API.postman_collection.json`: Exported Postman collection for further API exploration.

For any questions or issues, feel free to reach out me. Happy testing!
