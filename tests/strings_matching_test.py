import pytest
from validator import Validator
import sys
sys.path.append("..")


@pytest.mark.benchmark(warmup_iterations=1000, min_time=0.5, max_time=1, min_rounds=5, warmup=True)
class TestStringMatchingsShouldPass:

    data = {
        "foo": "some_string",
    }

    def validate(self, benchmark, rule):
        validator = Validator(rule)
        assert len(benchmark(validator.validate, obj=self.data)) == 0

    def test_eq_string_0(self, benchmark):
        rule = '''
                [
                    ["eq", "$.foo", "some_string"]
                ]
            '''
        self.validate(benchmark, rule)

    def test_starts_with_string_0(self, benchmark):
        rule = '''
                [
                    ["starts-with", "$.foo", "some_"]
                ]
            '''
        self.validate(benchmark, rule)


    def test_ends_with_string_0(self, benchmark):
        rule = '''
                [
                    ["ends-with", "$.foo", "_string"]
                ]
            '''
        self.validate(benchmark, rule)

    def test_contains_string_0(self, benchmark):
        rule = '''
                [
                    ["contains", "$.foo", "me_str"]
                ]
            '''
        self.validate(benchmark, rule)

    def test_split_and_first_0(self, benchmark):
        rule = '''
                [
                    ["eq", ["first", ["split", "$.foo", "_"]], "some"]
                ]
            '''
        self.validate(benchmark, rule)
