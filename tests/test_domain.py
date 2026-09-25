import pytest

from agent_domain import Task, TaskState, enforce_step_budget


def test_task_lifecycle_and_attempt_count() -> None:
    task = Task("task-1")
    task.start()
    assert task.state is TaskState.RUNNING
    assert task.attempts == 1
    task.finish(True)
    assert task.state is TaskState.SUCCEEDED


def test_task_rejects_invalid_transitions() -> None:
    task = Task("task-1")
    with pytest.raises(ValueError):
        task.finish(True)
    task.start()
    with pytest.raises(ValueError):
        task.start()
    task.finish(False)
    with pytest.raises(ValueError):
        task.cancel()


def test_task_cancellation() -> None:
    task = Task("task-1")
    task.cancel()
    assert task.state is TaskState.CANCELLED


@pytest.mark.parametrize(("completed", "limit"), [(0, 1), (4, 5)])
def test_step_budget_allows_work_below_limit(completed: int, limit: int) -> None:
    enforce_step_budget(completed, limit)


def test_step_budget_is_bounded() -> None:
    with pytest.raises(RuntimeError):
        enforce_step_budget(5, 5)


@pytest.mark.parametrize(("completed", "limit"), [(-1, 5), (0, 0), (1, 0)])
def test_step_budget_rejects_invalid_configuration(completed: int, limit: int) -> None:
    with pytest.raises(ValueError):
        enforce_step_budget(completed, limit)


def test_task_requires_id() -> None:
    with pytest.raises(ValueError):
        Task(" ")
