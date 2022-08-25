import pytest
from validator import Validator
import sys
sys.path.append("..")


@pytest.mark.benchmark(warmup_iterations=1000, min_time=0.5, max_time=1, min_rounds=5, warmup=True)
class TestAggregationsShouldPass:

    data = {
        "foo": True,
        "bar": False,
        "baz": False
    }

    def validate(self, benchmark, rule):
        validator = Validator(rule)
        assert len(benchmark(validator.validate, obj=self.data)) == 0

    def test_all_0(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["all", true, ["not", false]]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_all_1(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["all", "$.foo", ["not", "$.bar"], ["not", "$.baz"]]
                    }
                ]
            '''
        self.validate(benchmark, rule)


    def test_some_0(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["some", true, false]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_some_1(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["some", "$.foo", "$.bar", "$.baz"]
                    }
                ]
            '''
        self.validate(benchmark, rule)
