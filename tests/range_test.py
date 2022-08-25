import pytest
from validator import Validator
import sys
sys.path.append("..")


@pytest.mark.benchmark(warmup_iterations=1000, min_time=0.5, max_time=1, min_rounds=5, warmup=True)
class TestRangesShouldPass:

    data = {
        "foo": 1,
        "bar": -1
    }

    def validate(self, benchmark, rule):
        validator = Validator(rule)
        assert len(benchmark(validator.validate, obj=self.data)) == 0

    def test_in_range_0(self, benchmark):
        rule = '''
                [
                    {
                        "name": "simple in range on integers",
                        "rule": ["in-range", 1, 1, 1]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_in_range_1(self, benchmark):
        rule = '''
                [
                    {
                        "name": "simple in range on float and JSON path vars",
                        "rule": ["in-range", 0.5, "$.bar", "$.foo"]
                    }
                ]
            '''
        self.validate(benchmark, rule)

