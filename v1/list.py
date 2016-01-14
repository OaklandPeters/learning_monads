#!/usr/bin/env python3

import itertools
from typing import Callable, TypeVar, Iterator, Any

from monad import Monad, classproperty

Element = TypeVar('Element')

class List(Monad):
    """
    Will probably need 1 or 2 more functions that Haskell, because of need to be able to lift both functions and variables (which must be treated seperately in Python)
    """
    def bind(self, list_function: 'Callable[Element, List[Element]]') -> 'List[Element]':
        accumulator = self.zero
        for elm in self.data:
            accumulator = accumulator.append(list_function(elm))
        return accumulator.join()

    @classmethod
    def lift(cls, element: Element) -> 'List[Element]':
        return cls(element)

    def append(self, element: Element) -> 'List[Element]':
        accumulator = self.zero
        accumulator.data = self.data
        accumulator.data = accumulator.data + (element, )
        return accumulator

    @classproperty
    def zero(cls) -> 'List':
        return cls()

    def join(self) -> 'List[Element]':
        """ ~ flatten """
        accumulator = self.zero
        for element in self.data:
            if isinstance(element, List):
                for inner_elm in element:
                    accumulator = accumulator.append(inner_elm)
            else:
                accumulator = accumulator.append(element)
        return accumulator


    # -------------
    def __init__(self, *elements):
        self.data = elements

    def __repr__(self) -> str:
        return "List({0})".format(", ".join(repr(elm) for elm in self))

    def __str__(self):
        return repr(self)

    def __iter__(self) -> Iterator[Element]:
        return iter(self.data)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, List):
            return self.data == other.data
        else:
            return False

    # def __contains__(self, obj):
    #     return obj in self.data




#=============
# Unit-tests
#==============
import unittest

class TestList(unittest.TestCase):
    def test_zero(self):
        nul = List.zero
        self.assertEqual(nul.data, tuple())
        self.assertEqual(list(iter(nul)), [])

    def test_bind_single(self):
        _addtwo = lambda elm: elm + 2
        L_addtwo = lambda elm: List(_addtwo(elm))
        _list = List(1, 2, 3)
        result = _list.bind(L_addtwo)
        expected_data = tuple([_addtwo(elm) for elm in _list.data])
        self.assertEqual(result.data, expected_data)

    def test_bind_double(self):
        _double = lambda elm: (elm, elm.upper())
        L_double = lambda elm: List(*_double(elm))
        _list = List('a', 'b', 'c')
        result = _list.bind(L_double)
        expected_data = tuple([sub for elm in _list for sub in _double(elm)])
        self.assertEqual(result.data, expected_data)


if __name__ == "__main__":
    unittest.main()
