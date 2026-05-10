## Plan: Add backend FastAPI tests in a separate tests directory

TL;DR: Create a new `tests/` directory with pytest-based coverage for the FastAPI backend in `src/app.py`, add `pytest` to project dependencies, and verify with `pytest`.

**Steps**
1. Create `tests/` and add a test module:
   - `tests/__init__.py` (optional but conventional)
   - `tests/test_app.py`
2. In `tests/test_app.py`, import `TestClient` from `fastapi.testclient` and the `app` object from `src.app`.
3. Add tests for the backend endpoints using the AAA (Arrange-Act-Assert) pattern:
   - `GET /activities` returns all activities and includes expected fields
   - `POST /activities/{activity_name}/signup` adds a participant and returns success
   - `DELETE /activities/{activity_name}/participants/{email}` removes a participant and returns success
   - Error cases for missing activity and missing participant
4. Update `requirements.txt` to include `pytest` if it is not already installed in the environment.
5. Ensure `pytest.ini` stays in place; it already sets `pythonpath = .`, which supports importing `src.app` from tests.

**Verification**
1. Run `pytest` from repository root.
2. Confirm tests pass for normal signup and delete flows.
3. Confirm error cases also produce expected HTTP status codes.
4. Optionally run `python -m pytest -q` to verify the whole suite.

**Decisions**
- Use `fastapi.testclient.TestClient` for backend coverage rather than browser/UI testing.
- Keep tests separate from frontend static assets in a dedicated `tests/` directory.
- Do not modify frontend files as part of this backend-testing task.