import pytest
from validator import Validator
import sys
sys.path.append("..")


@pytest.mark.benchmark(warmup_iterations=1000, min_time=0.5, max_time=1, min_rounds=5, warmup=True)
class TestNumbersShouldPass:

    data = {
        "foo": 1,
        "bar": 1,
        "baz": {
            "foo": {
                "bar": 1,
                "baz": 2
            }
        }
    }

    def validate(self, benchmark, rule):
        validator = Validator(rule)
        assert len(benchmark(validator.validate, obj=self.data)) == 0

    def test_eq_0(self, benchmark):
        rule = '''
                [
                    {
                        "name": "test integer equality", 
                        "error_message": "they are not equal", 
                        "rule": ["eq", 1, 1]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_eq_1(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["eq", "$.foo", 1]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_eq_2(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["eq", "$.foo", "$.bar"]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_eq_3(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["eq", "$.bar", "$.foo"]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_eq_4(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["eq", "$.foo", "$.baz.foo.bar"]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_eq_5(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["eq", "$.foo", "$.foo"]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_eq_6(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["not", ["eq", "$.foo", "$.baz.foo.baz"]]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_eq_7(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["neq", "$.foo", "$.baz.foo.baz"]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_eq_delta_0(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["eq_delta", 0.1, 0.11, 0.099]
                    },
                    {
                        "rule": ["eq_delta", 1.1, 1.11, 0.01]
                    }
                ]
        '''
        self.validate(benchmark, rule)

    def test_abs_0(self, benchmark):
        rule = '''
                [
                    {
                        "rule": ["eq", 1, ["abs", -1]]
                    }
                ]
        '''
        self.validate(benchmark, rule)
