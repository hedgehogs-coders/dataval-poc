import math
import numbers
from jsonpath_ng import parse
from typing import Callable, List
from functools import lru_cache
import operator

# utility functions


def dual_expr(data, left_expr, right_expr, operator=None):
    left = left_expr(data)
    right = right_expr(data)
    return operator(left, right) if operator is not None else (left, right)


def unary_number_expr(data, expr, func):
    val = expr(data)
    if not isinstance(val, numbers.Number):
        raise Exception(f'{val} must be a number')
    return func(val)


# arithmetical operations


def _abs(data, expr):
    val = expr(data)
    if not isinstance(val, numbers.Number):
        raise Exception(f'{val} must be a number')
    return abs(val)


# comparison functions


def eq(data, left_expr, right_expr) -> bool:
    return dual_expr(data, left_expr, right_expr, operator.eq)


def eq_delta(data, left_expr, right_expr, delta_expr):
    left, right = dual_expr(data, left_expr, right_expr)
    delta = delta_expr(data)
    return math.isclose(left, right, rel_tol=delta)


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


def in_range(data, expr, low, high):
    return low(data) <= expr(data) <= high(data)


# float numbers operations


def ceil(data, expr) -> int:
    return unary_number_expr(data, expr, math.ceil)


def floor(data, expr):
    return unary_number_expr(data, expr, math.floor)


def _round(data, expr):
    return unary_number_expr(data, expr, round)


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

# string manipulation functions


def to_upper(data, expr):
    string_val = expr(data)
    return string_val.upper()


def to_lower(data, expr):
    string_val = expr(data)
    return string_val.lower()

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


def substring(data, left_expr, from_expr, to_expr):
    string = left_expr(data)
    start_index = from_expr(data)
    end_index = to_expr(data)
    return string[start_index:end_index]


def index(data, left_expr, right_expr):
    string, substring = dual_expr(data, left_expr, right_expr)
    return string.index(substring)


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


# aggregating functions

def _all(data, *expressions):
    return all([expression(data) for expression in expressions])


def some(data, *expressions):
    return any([expression(data) for expression in expressions])


def none(data, *expressions):
    return not _all(data, *expressions)


# logic functions

def _not(data, expr) -> bool:
    return not expr(data)


def _if(data, condition_expr, true_expr, false_expr=None):
    if condition_expr(data):
        return true_expr(data)

    if false_expr is not None:
        return false_expr(data)


# is functions

def is_number(data, expr):
    return is_integer(data, expr) or is_float(data, expr)


def is_integer(data, expr):
    int_value = expr(data)
    return isinstance(int_value, int)


def is_float(data, expr):
    float_val = expr(data)
    return isinstance(float_val, float)


def is_alphanumeric(data, expr):
    str_val = expr(data)
    return str_val.isalnum()


def is_string(data, expr):
    str_value = expr(data)
    return isinstance(str_value, str)


def is_boolean(data, expr):
    bool_val = expr(data)
    return isinstance(bool_val, bool)


def is_object(data, expr):
    obj_val = expr(data)
    return isinstance(obj_val, dict)


def is_list(data, expr):
    list_val = expr(data)
    return isinstance(list_val, list)


def is_null(data, expr):
    null_val = expr(data)
    return null_val == None


def is_empty(data, expr):
    """
        works on strings or lists
        string - returns false if length of string at least 1 or greater
    """
    value = expr(data)
    if isinstance(value, (str, list)):
        return len(value) == 0

    raise Exception(
        f"is_empty could be applied to lists and strings {type(value).__name__} found")

# date and time

# cast functions
