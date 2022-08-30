from functools import lru_cache
from typing import List, Optional

from handlers import _abs, _all, _if, _not, _round, ceil, concat, contains, ends_with, eq, eq_delta, exists, first, floor, in_range, last, length, lookup, neq, none, path, some, split, starts_with


class TreeNode:
    _name: Optional[str]
    _error_message: Optional[str]
    _expression: Optional[str]
    _leafs: List['TreeNode']

    def __init__(self, obj: list, is_parent=False):
        if not is_parent:
            self._expression = obj[0] if isinstance(
                obj, list) else None if isinstance(obj, dict) else obj
            if isinstance(obj, list) and len(obj) > 1:
                self._leafs: list[TreeNode] = [
                    as_tree(item, is_parent) for item in obj[1:]]
            elif isinstance(obj, dict) and "rule" in obj and isinstance(obj['rule'], list):
                self._name = obj.get(
                    'name', f'validation rule: {obj["rule"][0]}')
                self._error_message = obj.get(
                    'error_message', f'error in rule: {obj["rule"][0]}')
                self._leafs: list[TreeNode] = [as_tree(obj['rule'], is_parent)]
        else:
            self._leafs = [as_tree(leaf, False) for leaf in obj]

    def as_validation_tree(self):
        result = []
        for leaf in self._leafs:
            handler = rule_node_handler(leaf)
            result.append({
                "name": leaf._name or leaf._expression,
                "error_message": leaf._error_message,
                "validate": handler(leaf._leafs[0])
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
    if is_function_node(node._expression):
        return get_function_handler(node._expression)
    if is_root_rule_node(node):
        return rule_node_handler(node)

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

# in case we are going to support nested rules sometime


def is_root_rule_node(value: TreeNode):
    return value._expression is None and isinstance(value._name, str) and isinstance(value._error_message, str)


def is_function_node(expr: str):
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
        "if",
        "in-range",
        "abs",
        "ceil",
        "floor",
        "round",
        "exists",
        "concat",
        "lookup"
    ]


@lru_cache(500)
def get_function_handler(node_expression: str):
    if node_expression == "eq":
        return eq_handler
    if node_expression == "eq_delta":
        return eq_delta_handler
    if node_expression == "neq":
        return neq_handler
    if node_expression == "length":
        return length_handler
    if node_expression == "split":
        return split_handler
    if node_expression == "not":
        return not_handler
    if node_expression == "starts-with":
        return starts_with_handler
    if node_expression == "ends-with":
        return ends_with_handler
    if node_expression == "contains":
        return contains_handler
    if node_expression == "first":
        return first_handler
    if node_expression == "last":
        return last_handler
    if node_expression in ["all", "and"]:
        return all_handler
    if node_expression in ["some", "or"]:
        return some_handler
    if node_expression == "none":
        return none_handler
    if node_expression == "if":
        return if_handler
    if node_expression == "in-range":
        return in_range_handler
    if node_expression == "abs":
        return abs_handler
    if node_expression == "ceil":
        return ceil_handler
    if node_expression == "floor":
        return floor_handler
    if node_expression == "round":
        return round_handler
    if node_expression == "exists":
        return exists_handler
    if node_expression == "concat":
        return concat_handler
    if node_expression == "lookup":
        return lookup_handler

    raise Exception(f'handler {node_expression} not implemented or unknown')


def eq_handler(node: TreeNode):
    ensure_leafs(node, 2)
    args = get_handlers(node)
    return lambda data: eq(data, *args)


def rule_node_handler(node: TreeNode):
    assert len(node._leafs) == 1
    return get_handler_for(node._leafs[0])


def eq_delta_handler(node: TreeNode):
    ensure_leafs(node, 3)
    args = get_handlers(node)
    return lambda data: eq_delta(data, *args)


def neq_handler(node: TreeNode):
    ensure_leafs(node, 2)
    args = get_handlers(node)
    return lambda data: neq(data, *args)


def in_range_handler(node: TreeNode):
    ensure_leafs(node, 3)
    args = get_handlers(node)
    return lambda data: in_range(data, *args)


def abs_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: _abs(data, *args)


def ceil_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: ceil(data, *args)


def floor_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: floor(data, *args)


def round_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: _round(data, *args)


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


def exists_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: exists(data, *args)


def concat_handler(node: TreeNode):
    if len(node._leafs) < 1:
        raise Exception("concat expects something to concatenate, no parts were provided")

    args = get_handlers(node)
    return lambda data: concat(data, *args)


def lookup_handler(node: TreeNode):
    ensure_leafs(node, 1)
    args = get_handlers(node)
    return lambda data: lookup(data, *args)
