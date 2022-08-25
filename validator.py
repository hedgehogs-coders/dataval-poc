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
                    raise Exception(f"validation failed for rule {validation_rule['name']} with message: {validation_rule['error_message']}")
            except Exception as e:
                errors.append(e)

        return errors
