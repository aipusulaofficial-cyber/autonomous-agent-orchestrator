from job_runner import *
import pytest


def test_success_audit():
    j = Job("1", ["a", "b"])
    JobRunner({"a": lambda: None, "b": lambda: None}).run(j)
    assert j.state is State.SUCCEEDED and j.audit[-1] == "completed"


def test_allowlist():
    with pytest.raises(KeyError):
        JobRunner({}).run(Job("1", ["x"]))


def test_budget():
    with pytest.raises(ValueError):
        JobRunner({}, 1).run(Job("1", ["a", "b"]))
