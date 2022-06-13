import json
from tree import as_tree


class Validator:
    def __init__(self, rules: str) -> None:
        self.val_tree = as_tree(json.loads(rules)).as_validation_tree()

    def validate(self, obj: dict) -> list:
        errors = []
        for validation_rule in self.val_tree:
            try:
                result = validation_rule['validate'](obj)
                if not result:
                    raise Exception("something failed, and I need to provide enough context for response")
            except Exception as e:
                errors.append(f"validation failed due to: {e}")

        return errors
