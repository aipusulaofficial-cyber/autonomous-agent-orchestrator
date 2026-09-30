import pytest

from durable_jobs import DurableJobStore
from job_runner import Job, JobRunner, State


def test_completed_job_cannot_replay_actions():
    invoked = []
    runner = JobRunner({"charge": lambda: invoked.append("charge")})
    job = Job("job-1", ["charge"])
    runner.run(job)
    assert job.state == State.SUCCEEDED
    with pytest.raises(ValueError, match="only planned"):
        runner.run(job)
    assert invoked == ["charge"]


def test_persistent_transition_is_compare_and_swap(tmp_path):
    store = DurableJobStore(str(tmp_path / "jobs.db"))
    store.put("j1", "planned", "data", "t0")
    assert store.transition("j1", "planned", "running", "data", "t1")
    assert not store.transition("j1", "planned", "running", "stale", "t2")
    assert store.transition("j1", "running", "succeeded", "data", "t3")
    with pytest.raises(ValueError):
        store.transition("j1", "succeeded", "running", "data", "t4")
    assert store.get("j1") == ("j1", "succeeded", "data", "t3")


def test_invalid_action_budget_rejected():
    with pytest.raises(ValueError):
        JobRunner({}, max_actions=-1)
