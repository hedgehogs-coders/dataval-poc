import pytest
from validator import Validator
import sys
sys.path.append("..")


@pytest.mark.benchmark(warmup_iterations=1000, min_time=0.5, max_time=1, min_rounds=5, warmup=True)
class TestExists:

    data = {
        "foo": 1,
        "bar": "$.",
        "baz": []
    }

    def validate(self, benchmark, rule):
        validator = Validator(rule)
        assert len(benchmark(validator.validate, obj=self.data)) == 0

    def test_exists_0(self, benchmark):
        rule = '''
                [
                    {
                        "name": "Simple path exists test",
                        "rule": ["exists", "$.foo"]
                    }
                ]
            '''
        self.validate(benchmark, rule)

    def test_exists_1(self, benchmark):
        rule = '''
                [
                    {
                        "name": "Concatenated path exists test",
                        "rule": ["exists", ["lookup", ["concat", "$.bar", "foo"]]]
                    }
                ]
            '''
        self.validate(benchmark, rule)


    def test_exists_2(self, benchmark):
        rule = '''
                [
                    {
                        "name": "Concatenated path exists test",
                        "rule": ["exists", ["lookup", ["concat", "$.bar", "baz"]]]
                    }
                ]
            '''
        self.validate(benchmark, rule)


