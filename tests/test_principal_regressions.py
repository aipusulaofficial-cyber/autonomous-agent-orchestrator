import pytest

from job_runner import Job, JobRunner


def test_completed_job_cannot_run_again():
    calls = []
    runner = JobRunner({"tool": lambda: calls.append("called")})
    job = Job("job", ["tool"])
    runner.run(job)
    with pytest.raises(ValueError):
        runner.run(job)
    assert calls == ["called"]


def test_invalid_action_budget_rejected():
    with pytest.raises(ValueError):
        JobRunner({}, max_actions=0)
