from fastapi.testclient import TestClient
from hypothesis import given, strategies as st

from service import app

client = TestClient(app)


def test_contract() -> None:
    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").status_code == 200


@given(st.text(min_size=1, max_size=32).filter(lambda value: value.strip()))
def test_task_contract(value: str) -> None:
    response = client.post(
        "/v1/tasks",
        json={"key": value, "payload": {}},
    )
    assert response.status_code == 200, response.text
    assert response.json()["state"] == "running"
