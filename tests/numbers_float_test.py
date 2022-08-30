from distutils.log import error
import pytest
from validator import Validator
import sys
sys.path.append("..")


@pytest.mark.benchmark(warmup_iterations=1000, min_time=0.5, max_time=1, min_rounds=5, warmup=True)
class TestFloatsShouldPass:

    data = {
        "foo": 1,
        "bar": 2,
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

    def test_ceil_0(self, benchmark):
        rule = '''
                [
                    {
                        "name": "test ceil equality", 
                        "error_message": "got wrong ceiled value", 
                        "rule": ["eq", 2, ["ceil", 1.1]]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_ceil_1(self, benchmark):
        rule = '''
                [
                    {
                        "name": "test ceil equality 2", 
                        "error_message": "got wrong ceiled value", 
                        "rule": ["eq", "$.bar", ["ceil", 1.1]]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_floor_0(self, benchmark):
        rule = '''
                [
                    {
                        "name": "test ceil equality", 
                        "error_message": "got wrong floor value", 
                        "rule": ["eq", 1, ["floor", 1.1]]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_floor_1(self, benchmark):
        rule = '''
                [
                    {
                        "name": "test ceil equality 2", 
                        "error_message": "got wrong floor value", 
                        "rule": ["eq", "$.foo", ["floor", 1.1]]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_round_0(self, benchmark):
        rule = '''
                [
                    {
                        "name": "test round equality", 
                        "error_message": "got wrong round value", 
                        "rule": ["eq", 1, ["round", 1.1]]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_round_1(self, benchmark):
        rule = '''
                [
                    {
                        "name": "test round equality 2", 
                        "error_message": "got wrong round value", 
                        "rule": ["and", ["eq", "$.foo", ["round", 1.1]], ["eq", "$.bar", ["round", 1.55]]]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_ceil_must_fail_0(self):
        rule = '''
                [
                    {
                        "name": "test ceil equality on non numbers", 
                        "error_message": "got wrong round value", 
                        "rule": ["eq", "$.foo", ["ceil", "foo"]]
                    }
                ]
            '''
        validator = Validator(rule)
        
        errors = validator.validate(self.data)
        assert len(errors) == 1 and errors[0].startswith("validation failed for rule \"test ceil equality on non numbers\"") 
