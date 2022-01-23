class Calculator:
    def __init__(self, factor: int = 10):
        self.factor = factor

    def calculate(self, x: int, y: float) -> float:  # pylint: disable=invalid-name
        return x ** 2 + self.factor * y
