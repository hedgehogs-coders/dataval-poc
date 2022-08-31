import pytest
from validator import Validator
import sys
sys.path.append("..")


@pytest.mark.benchmark(warmup_iterations=1000, min_time=0.5, max_time=1, min_rounds=5, warmup=True)
class TestIsFunctions:

    data = {
        "foo": 1,
        "bar": 1.1,
        "baz": "foo"
    }

    def validate(self, benchmark, rule):
        validator = Validator(rule)
        assert len(benchmark(validator.validate, obj=self.data)) == 0

    def test_exists_0(self, benchmark):
        rule = '''
                [
                    {
                        "name": "is_number test",
                        "rule": ["and", ["is_number", "$.foo"],["is_number", "$.bar"]]
                    }
                ]
            '''
        self.validate(benchmark, rule)



