from validator import Validator
import sys
sys.path.append("..")


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

    def test_eq_0(self):
        rule = '''
                [
                    ["eq", 1, 1]
                ]
            '''
        validator = Validator(rule)
        assert len(validator.validate(self.data)) == 0

    def test_eq_1(self):
        rule = '''
                [
                    ["eq", "$.foo", 1]
                ]
            '''
        validator = Validator(rule)
        assert len(validator.validate(self.data)) == 0

    def test_eq_2(self):
        rule = '''
                [
                    ["eq", "$.foo", "$.bar"]
                ]
            '''
        validator = Validator(rule)
        assert len(validator.validate(self.data)) == 0

    def test_eq_3(self):
        rule = '''
                [
                    ["eq", "$.bar", "$.foo"]
                ]
            '''
        validator = Validator(rule)
        assert len(validator.validate(self.data)) == 0

    def test_eq_4(self):
        rule = '''
                [
                    ["eq", "$.foo", "$.baz.foo.bar"]
                ]
            '''
        validator = Validator(rule)
        assert len(validator.validate(self.data)) == 0

    def test_eq_5(self):
        rule = '''
                [
                    ["eq", "$.foo", "$.foo"]
                ]
            '''
        validator = Validator(rule)
        assert len(validator.validate(self.data)) == 0

    def test_eq_6(self):
        rule = '''
                [
                    ["not", ["eq", "$.foo", "$.baz.foo.baz"]]
                ]
            '''
        validator = Validator(rule)
        assert len(validator.validate(self.data)) == 0
