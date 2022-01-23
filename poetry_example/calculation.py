from poetry_example.data import CalculationResponse


class Calculator:
    def __init__(self, factor: int = 10):
        self.factor = factor

    def calculate(self, x: int, y: float) -> CalculationResponse:  # pylint: disable=invalid-name
        value = x ** 2 + self.factor * y
        return CalculationResponse(result=value)
