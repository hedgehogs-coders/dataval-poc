from typing import List

from handlers import _all, _if, _not, contains, ends_with, eq, eq_delta, first, last, length, neq, none, path, some, split, starts_with


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
                "name": leaf._expression,
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


def get_handlers(node: TreeNode):
    result = []
    for leaf in node._leafs:
        result.append(get_handler_for(leaf)(leaf))

    return result

def is_path_node(value: TreeNode):
    expr = value._expression
    return isinstance(expr, str) and expr.startswith('$.') and not hasattr(value, '_leafs')


def is_primitive_node(value: TreeNode):
    expr = value._expression
    return isinstance(expr, (str, int, float, bool)) and not hasattr(value, '_leafs')


def is_function_node(leaf: TreeNode):
    expr = leaf._expression
    return expr in [
        "eq",
        "eq_delta",
        "neq",
        "split",
        "length",
        "not",
        "starts-with",
        "ends-with",
        "contains",
        "first",
        "last",
        "all",
        "some",
        "none",
        "and",
        "or",
        "if"
    ]


def get_function_handler(node: TreeNode):
    if node._expression == "eq":
        return eq_handler
    if node._expression == "eq_delta":
        return eq_delta_handler
    if node._expression == "neq":
        return neq_handler
    if node._expression == "length":
        return length_handler
    if node._expression == "split":
        return split_handler
    if node._expression == "not":
        return not_handler
    if node._expression == "starts-with":
        return starts_with_handler
    if node._expression == "ends-with":
        return ends_with_handler
    if node._expression == "contains":
        return contains_handler
    if node._expression == "first":
        return first_handler
    if node._expression == "last":
        return last_handler
    if node._expression in ["all", "and"]:
        return all_handler
    if node._expression in ["some", "or"]:
        return some_handler
    if node._expression == "none":
        return none_handler
    if node._expression == "if":
        return if_handler

    raise Exception(f'handler {node._expression} not implemented or unknown')


def eq_handler(node: TreeNode):
    ensure_leafs(node, 2)
    args = get_handlers(node)
    return lambda data: eq(data, *args)


def eq_delta_handler(node: TreeNode):
    ensure_leafs(node, 3)
    args = get_handlers(node)
    return lambda data: eq_delta(data, *args)


def neq_handler(node: TreeNode):
    ensure_leafs(node, 2)
    args = get_handlers(node)
    return lambda data: neq(data, *args)


def length_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: length(data, *args)


def path_handler(node: TreeNode):
    def extract_single(obj: list):
        return obj[0] if len(obj) == 1 else obj
    return lambda data: extract_single([match.value for match in path(node._expression)(data)])


def split_handler(node: TreeNode):
    ensure_leafs(node, 2)
    args = get_handlers(node)
    return lambda data: split(data, *args)


def literal_handler(node: TreeNode):
    return lambda _: node._expression


def not_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: _not(data, *args)


def starts_with_handler(node: TreeNode):
    ensure_leafs(node, 2)
    args = get_handlers(node)
    return lambda data: starts_with(data, *args)


def ends_with_handler(node: TreeNode):
    ensure_leafs(node, 2)
    args = get_handlers(node)
    return lambda data: ends_with(data, *args)


def contains_handler(node: TreeNode):
    ensure_leafs(node, 2)
    args = get_handlers(node)
    return lambda data: contains(data, *args)


def first_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: first(data, *args)


def last_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: last(data, *args)


def all_handler(node: TreeNode):
    args = get_handlers(node)
    return lambda data: _all(data, *args)


def some_handler(node: TreeNode):
    args = get_handlers(node)
    return lambda data: some(data, *args)


def none_handler(node: TreeNode):
    args = get_handlers(node)
    return lambda data: none(data, *args)


def if_handler(node: TreeNode):
    if 2 > len(node._leafs) > 3:
        raise Exception(
            f"if expects 2 or 3 arguments while {len(node._leafs)} were provided")
    args = get_handlers(node)
    return lambda data: _if(data, *args)
