from poetry_example.data import CalculationRequest


def test_request() -> None:
    req = CalculationRequest(x=10, y=0.5)
    assert req.x == 10
    assert req.y == 0.5
