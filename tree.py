from typing import List

from handlers import _not, eq, length, path, split


class TreeNode:
    _expression: str
    _leafs: List['TreeNode']

    def __init__(self, obj: list, is_parent=False):
        if not is_parent:
            self._expression = obj[0] if isinstance(obj, list) else obj
            if isinstance(obj, list) and len(obj) > 1:
                self._leafs: list[TreeNode] = [
                    as_tree(item, is_parent) for item in obj[1:]]
        else:
            self._leafs = [as_tree(leaf, False) for leaf in obj]

    def as_validation_tree(self):
        result = []
        for leaf in self._leafs:
            handler = get_handler_for(leaf)
            result.append({
                "validate": handler(leaf)
            })

        return result


def as_tree(obj: list, is_parent=True) -> TreeNode:
    return TreeNode(obj, is_parent)


def ensure_leafs(node: TreeNode, n):
    if len(node._leafs) != n:
        raise Exception(
            f"{node._expression} expects {n} arguments while {len(node._leafs)} were provided")


def get_handler_for(node: TreeNode):
    if is_path_node(node):
        return path_handler
    if is_primitive_node(node):
        return literal_handler
    if is_function_node(node):
        return get_function_handler(node)

    raise Exception(f'Unsupported expression {node._expression}')


def is_path_node(value: TreeNode):
    expr = value._expression
    return isinstance(expr, str) and expr.startswith('$.') and not hasattr(value, '_leafs')


def is_primitive_node(value: TreeNode):
    expr = value._expression
    return isinstance(expr, (str, int, float, bool)) and not hasattr(value, '_leafs')


def is_function_node(leaf: TreeNode):
    expr = leaf._expression
    return expr in ["eq", "split", "length", "not"]


def get_function_handler(node: TreeNode):
    if node._expression == "eq":
        return eq_handler
    if node._expression == "length":
        return length_handler
    if node._expression == "split":
        return split_handler
    if node._expression == "not":
        return not_handler

    raise Exception(f'handler {node._expression} not implemented or unknown')


def eq_handler(node: TreeNode):
    ensure_leafs(node, 2)

    first_arg = get_handler_for(node._leafs[0])(node._leafs[0])
    second_arg = get_handler_for(node._leafs[1])(node._leafs[1])

    return lambda data: eq(data, first_arg, second_arg)


def length_handler(node: TreeNode):
    ensure_leafs(node, 1)

    first_arg = get_handler_for(node._leafs[0])(node._leafs[0])

    return lambda data: length(data, first_arg)


def path_handler(node: TreeNode):
    def extract_single(obj: list):
        return obj[0] if len(obj) == 1 else obj
    return lambda data: extract_single([match.value for match in path(node._expression)(data)])


def split_handler(node: TreeNode):
    ensure_leafs(node, 2)

    first_arg = get_handler_for(node._leafs[0])(node._leafs[0])
    second_arg = get_handler_for(node._leafs[1])(node._leafs[1])

    return lambda data: split(data, first_arg, second_arg)


def literal_handler(node: TreeNode):
    return lambda _: node._expression

def not_handler(node: TreeNode):
    ensure_leafs(node, 1)
    
    first_arg = get_handler_for(node._leafs[0])(node._leafs[0])

    return lambda data: _not(data, first_arg)
