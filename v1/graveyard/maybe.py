#!/usr/bin/env python3
"""
I don't know how to get this to work...
    the chaining
    then collapse

First(user).bind(get_middle).bind(get_first).bind(get_last)  # == 'david'
Last(user).bind(get_first).bind(get_last).bind(get_middle)  # == 'bowie'
"""

from typing import Callable, TypeVar, Iterator, Any

from monad import Monad, classproperty


class Maybe(Monad):
    @classmethod
    def lift(cls, value):
        return Just(value)
    @classproperty
    def zero(cls):
        return Nothing()
    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            self.data
        )


class Just(Maybe):
    def __init__(self, value):
        self.data = value
    def bind(self, function: Callable[Element, [Maybe[Element]]]):
        return function(self.data)

class Nothing(Maybe):
    def bind(self, function: Callable[Element, [Maybe[Element]]]):
        return self
    def __repr__(self):
        return "{0}()".format(self.__class__.__name__)

class First(Maybe):
    def __init__(self, element):
        if not isinstance(element, Maybe):
            raise TypeError("Argument to '{0}' must be a Maybe.".format(type(self).__name__))
        else:
            self.data = element

    def bind(self, function: Callable[Element, [Maybe[Element]]]):



class Last(Maybe):
    def __init__(self, element):
        if not isinstance(element, Maybe):
            raise TypeError("Argument to '{0}' must be a Maybe.".format(type(self).__name__))
        else:
            self.data = element



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

maybe_get = maybe_error(IndexError)



import unittest


user = {
    'first': 'David',
    'last': 'Bowie',
    'uid': 1234
}
get = lambda key: lambda obj: obj[key]
# get_first = maybe_indexerror(lambda obj: obj['first'])
# get_last = maybe_indexerror(lambda obj: obj['last'])
# get_middle = maybe_indexerror(lambda obj: obj['middle'])


class TestMaybe(unittest.TestCase):
    def test_syntax_dev(self):
        """This is an exploration of what I'd like to
        see be true, syntactically.
        It is NOT a check on what IS true.
        """
        name = Maybe(user).bind(
            Maybe(get('first'))
            >> get('middle')
            >> get('last')
        )
        MaybeX >> value = MaybeX.append()

        # this is actually fmap, chained
    def test_nothing(self):
        pass
    def test_empty(self):
        pass
    def test_success(self):
        Maybe(user).bind(get_first)
    def test_failure(self):
        pass
    def test_chaining_success(self):
        pass
    def test_chaining_failure(self):
        pass
    def test_first(self):
        pass
    def test_last(self):
        pass
