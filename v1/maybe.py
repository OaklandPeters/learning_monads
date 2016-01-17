#!/usr/bin/env python3
"""

Ok, I'm just arbitarily defining this 'Maybe' as Maybe error.


Idea for treatment:
    Have 'lift' just be a wrap (even when used as a decorator).
    So, that lift(function) --> an object whose __call__ triggers f_apply
"""

from typing import Callable, TypeVar, Iterator, Any

from monad import Monad, classproperty

AccessorErrors = (AttributeError, IndexError, KeyError)

def maybe_error(*exceptions):
    """
    Turns a normal function into one returning Maybe.
    This is basically 'fmap' for Maybe.
    Although, you have to pass it an exception type first.
    """
    def wrapper(function):
        def wrapped(*args, **kwargs):
            try:
                return Just(function(*args, **kwargs))
            except *exceptions:
                return Nothing()
        return wrapped
    return wrapper

class Maybe:
    def __init__(self, *elements, exceptions=AccessorErrors):
        self.exceptions = exceptions
        self.data = elements

    def f_apply(self, function):
        try:
            return Just(function(*self.data))
        except self.exceptions:
            return Nothing()

    def f_map(self):
        def wrapped(*args, **kwargs):
            function = self.data[0]  # This is not a safe assumption, that there is exactly 1 elem
            try:
                return Just(function(*args, **kwargs))
            except self.exceptions:
                return Nothing()
        return wrapped
