from operator import eq
from typing import Any, Callable, Dict, Tuple, TypeVar, Union

T = TypeVar("T")
T1 = TypeVar("T1")


def gentle_eq(a: Any, b: Any) -> bool:
    if isinstance(a, BaseException):
        a = str(a)
    if isinstance(b, BaseException):
        b = str(b)

    return eq(a, b)


def example_test(func: Callable[..., T], examples: Dict[Tuple[T1, ...], T], *,
                 prep: Callable[[Union[T, T1]], Any] = None,
                 comp: Callable[[T, T1], bool] = gentle_eq):
    for input_params, expected_res in examples.items():
        try:
            res = func(*input_params)
        except BaseException as e:
            if isinstance(expected_res, BaseException):
                res = e
            else:
                raise

        if prep:
            res = prep(res)
            expected_res = prep(expected_res)

        try:
            assert comp(res, expected_res)
        except AssertionError:
            print("expected:", expected_res, "\nactual:", res)
            raise AssertionError(res, expected_res)
