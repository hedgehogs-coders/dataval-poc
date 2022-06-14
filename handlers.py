from jsonpath_ng import parse
from typing import Callable, List
from functools import lru_cache
import operator


def dual_expr(data, left_expr, right_expr, operator=None):
    left = left_expr(data)
    right = right_expr(data)
    return operator(left, right) if operator is not None else (left, right)


# comparison functions
def eq(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.eq)


def neq(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.ne)


def gt(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.gt)


def gte(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.ge)


def lt(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.lt)


def lte(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.le)


# string matching functions

def starts_with(data, left_expr, right_expr) -> bool:
    string, pattern = dual_expr(data, left_expr, right_expr)

    if not isinstance(string, str) or not isinstance(pattern, str):
        raise Exception(
            "both arguments of starts-with must evaluate to strings")

    return string.startswith(pattern)


def ends_with(data, left_expr, right_expr) -> bool:
    string, pattern = dual_expr(data, left_expr, right_expr)

    if not isinstance(string, str) or not isinstance(pattern, str):
        raise Exception(
            "both arguments of ends-with must evaluate to strings")

    return string.endswith(pattern)


def contains(data, left_expr, right_expr) -> bool:
    string, pattern = dual_expr(data, left_expr, right_expr)

    if not isinstance(string, str) or not isinstance(pattern, str):
        raise Exception(
            "both arguments of ends-with must evaluate to strings")

    return string != None and pattern in string


def _not(data, expr) -> bool:
    return not expr(data)


# data manipulation functions

def length(data, expr) -> int:
    return len(expr(data))


@lru_cache(maxsize=512)
def path(path: str) -> Callable:
    jsonpath_expression = parse(path)
    return jsonpath_expression.find


def split(data, left_expr, right_expr) -> List[str]:
    string, divider = dual_expr(data, left_expr, right_expr)
    if not isinstance(string, str) or not isinstance(divider, str):
        raise Exception(
            f"split couldn't be performed on  types {type(string)} and {type(divider)}")
    return string.split(divider)


# list functions

def first(data, expr):
    list = expr(data)

    return list[0] if len(list) > 0 else None


def last(data, expr):
    list = expr(data)

    return list[-1] if len(list) > 0 else None


def in_list(data, left_expr, right_expr) -> bool:
    list, needle = dual_expr(data, left_expr, right_expr)

    return needle in list


def find(data, left_expr, right_expr):
    list, needle = dual_expr(data, left_expr, right_expr)
    return next(iter([item for item in list if item == needle]), None)


def find_all(data, left_expr, right_expr):
    list, needle = dual_expr(data, left_expr, right_expr)
    return [item for item in list if item == needle]
