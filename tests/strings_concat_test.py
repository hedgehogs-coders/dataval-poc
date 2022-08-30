import pytest
from validator import Validator
import sys
sys.path.append("..")


@pytest.mark.benchmark(warmup_iterations=1000, min_time=0.5, max_time=1, min_rounds=5, warmup=True)
class TestStringConcat:

    data = {
        "foo": "foo",
        "bar": "bar"
    }

    def validate(self, benchmark, rule):
        validator = Validator(rule)
        assert len(benchmark(validator.validate, obj=self.data)) == 0

    def test_concat_0(self, benchmark):
        rule = '''
                [
                    {
                        "name": "Simple string concat test",
                        "rule": ["eq", "foo_bar", ["concat", "foo", "_", "bar"]]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_concat_1(self, benchmark):
        rule = '''
                [
                    {
                        "name": "Simple string concat test",
                        "rule": ["eq", "foo_bar", ["concat", "$.foo", "_", "$.bar"]]
                    }
                ]
            '''
        self.validate(benchmark, rule)



