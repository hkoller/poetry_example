from poetry_example.calculation import Calculator


class TestCalculation:
    @staticmethod
    def test_a_calculation() -> None:
        assert Calculator().calculate(x=10, y=20) == 300.0
