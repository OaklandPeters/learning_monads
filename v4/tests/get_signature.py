"""Splat of notes, because I would like to be able
to type-check with Callable[[], ]
"""
import inspect


def sig_info(func):
    """
    Task: get positional signature
    """
    sig = inspect.signature(func)
    ordered_dict = sig.parameters

    args, varargs, keywords, defaults = inspect.getargspec(func)

