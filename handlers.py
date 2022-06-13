from ast import expr
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


def gt(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.gt)


def gte(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.ge)


def lt(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.lt)


def lte(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.le)


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
