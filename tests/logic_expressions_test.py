import pytest
from validator import Validator
import sys
sys.path.append("..")


@pytest.mark.benchmark(warmup_iterations=1000, min_time=0.5, max_time=1, min_rounds=5, warmup=True)
class TestLogicExpressionsShouldPass:

    data = {
        "foo": True,
        "bar": False,
        "baz": False
    }

    def validate(self, benchmark, rule):
        validator = Validator(rule)
        assert len(benchmark(validator.validate, obj=self.data)) == 0

    def test_and_0(self, benchmark):
        rule = '''
                [
                    ["and", true, ["not", false]]
                ]
            '''
        self.validate(benchmark, rule)

    def test_and_1(self, benchmark):
        rule = '''
                [
                    ["and", "$.foo", ["and", ["not", "$.bar"], ["not", "$.baz"]]]
                ]
            '''
        self.validate(benchmark, rule)

    def test_if_0(self, benchmark):
        rule = '''
            [
                ["if", "$.foo", ["eq", "$.bar", false]]
            ]
        '''
        self.validate(benchmark, rule)

    def test_if_1(self, benchmark):
        rule = '''
            [
                ["if", ["not","$.foo"], ["eq", "$.bar", true], ["and", ["eq", "$.baz", false], ["eq", "$.bar", false]]]
            ]
        '''
        self.validate(benchmark, rule)
