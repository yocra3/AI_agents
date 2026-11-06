# Bash testing with bats

Use the repository's test layout and command when defined; otherwise follow these conventions.

- Layout: one `<slug>.bats` file per component or behavior in the test folder, with
  `@test "<description>" { ... }` blocks. Invoke commands with `run` and assert on `$status` and
  `$output`.
- Shared setup: `setup` and `teardown` run around each test; `setup_file` and `teardown_file` run
  once per `.bats` file. Load shared helpers with `load <helper>`.
- Session-level setup: put work that must run once per test session in `setup_suite`, defined in
  `setup_suite.bash` next to the `.bats` files, with cleanup in `teardown_suite`. `export` the
  variables that tests need.
- Temporary files: use `$BATS_TEST_TMPDIR` or `$BATS_FILE_TMPDIR`.
- Skip: `skip "<reason>"` at the point in the test to skip.
- Run: `bats <dir>` (add `-r` for subfolders), which exits with a non-zero status when a test
  fails.

Official reference: [bats-core](https://bats-core.readthedocs.io/).
