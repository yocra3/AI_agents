# Python testing with pytest

Use the repository's test layout and command when defined; otherwise follow these conventions.

- Layout: one `test_<slug>.py` file per component or behavior in the test folder, with `test_*`
  functions and plain `assert` statements.
- Shared setup: define fixtures in `conftest.py` in the test folder. pytest discovers them without
  imports.
- Session-level setup: put work that must run once per test session in a fixture declared with
  `@pytest.fixture(scope="session")`, requested by the tests that need it or marked
  `autouse=True`. Code after its `yield` runs as teardown.
- Temporary files: use the `tmp_path` fixture, or `tmp_path_factory` in session-scoped fixtures.
- Skip: `@pytest.mark.skipif(<condition>, reason="<reason>")`, or `pytest.skip("<reason>")` inside
  a test or fixture.
- Run: `python3 -m pytest <dir>`, which exits with a non-zero status when a test fails.

Official reference: [pytest](https://docs.pytest.org/).
