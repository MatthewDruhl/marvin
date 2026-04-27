"""Exclude fixture project from pytest collection.

This file prevents pytest from trying to collect/import test files
in the fixture project, which exist as harden audit targets — not
as runnable tests.
"""

collect_ignore_glob = ["**/*.py"]
