#!/User/bin/env python3
"""
Used for randomly generating data instances for unit-tests.
Little ad-hoc replacement for QuickCheck

Existing quick-check like libraries which could be used for this purpose, or
used as inspiration for better class structure:
    https://github.com/DRMacIver/hypothesis




@todo: Write way to take union at the class level

TODO:
Look for examples of pathelogical strings, drawn from various languages
    SQL
    Python
    Javascript



TODO: ADVANCED: Edge cases which should fail. For example: for float - passing in integers


Future-ideas
----------------
* Strings in various encodings.
* Common structured data: XML, JSON, HTML, CSV
* Serialized data,as string - of the structured data types.
* File serialization: txt, json, html, xml, csv
** Especially, see the way this would interact with mal-formed
* 'MalformedX' - data which is not technically correct version of X, but you
tend to encounter anyway. Slightly misformed. Especially for structured data.
** Subclass: where possible, construct a subclass, and feed it through.
** Duck-typing: for dict/list/tuple - Mapping, MutableMapping, Sequence, MutableSequence
** For strings: Strings in incorrect encodings. bytes. Py2 - str/unicode.
** For numbers: different data-types (float, complex)
** For structured data types: slightly incorrect encodings.
*** For HTML: incorrectly structured data, which most browsers accept anyway
** For everything: None
** For everything: the class-variable, rather than an instance
* Web communication: various calls: request, ajax. Honestly not sure what this would look like.
"""
import typing
import random
from abc import abstractmethod, ABCMeta, abstractproperty
import collections
import sys
import math

import string
import unicodedata
import unittest

from .typecheckable import type_check_sequence

maxint = sys.maxsize

# Typedefs
Inner = typing.TypeVar('Inner')
Index = typing.TypeVar('Index')
Pair = typing.Tuple[Index, Inner]


class RandGenInterface(collections.abc.Sequence, typing.Generic[Index, Inner], metaclass=ABCMeta):
    """
    Built assuming possible data values stored in an internal sequence.
    This is not a Sequence. Although it wraps linear (Sequence) data,
    it behaves more like a Mapping
    """

    #
    # Abstractmethods
    #
    @abstractmethod
    def __init__(self, *args, seed=None, **kwargs):
        """Abstract, but provides a default implemention
        to be used in super().__init__ calls
        """
        self.seed = seed
        self.Random = random.Random(self.seed)

    @abstractmethod
    def indices(self) -> typing.Sequence[Index]:
        """
        Augmented method - makes this compatible with RandUnion
        """
        return NotImplemented

    @abstractmethod
    def __getitem__(self, index: Index) -> Inner:
        return NotImplemented

    #
    # Semi-derived methods:
    #   These are implied by the __init__ method
    #@abstractproperty
    #def seed(self) -> int:
    #    return NotImplemented

    #@abstractproperty
    #def Random(self) -> random.Random:
    #    return NotImplemented

    #
    # Derived methods
    #
    def values(self) -> typing.Iterable[Inner]:
        for index in self.indices():
            yield self[index]

    #def deterministic(self) -> typing.Iterator[Pairs]:
    #    for index in self.indices():
    #        yield (index, self[index])

    #def pairs(self) -> typing.Sequence[Pairs]:
    #    if not hasattr(self, '_pairs'):
    #        self._pairs = tuple(self.deterministic())
    #    return self._pairs

    def __len__(self):
        return len(self.indices())

    def __iter__(self):
        return iter(self.values())

    def rand(self):
        return self.Random.choice(self.values())
    #
    # Randomization
    #
    def sample(self):
        """Random permutation of the indices.
        Resets to initial state every time this is called.
        """
        self.Random.seed(self.seed)
        length = len(self)
        for index_into_indices in self.Random.sample(length, length):
            yield self.indices()[index_into_indices]

    def walk(self) -> typing.Iterator[Pair]:
        """Random walk through the data.
        """
        for index in self.sample():
            yield (index, self[index])


class RandAtomics(RandGenInterface[int, Inner]):
    """Refined convenience abstract class.
    Requires only a single abstract *property*: _values
    Which is usually implemented at the class level
    """   
    @abstractproperty
    def _values(self) -> typing.Sequence:
        return NotImplemented

    # Mixin methods
    def __init__(self, seed=None):
        self.seed = seed
        self.Random = random.Random(self.seed)
        #super().__init__(self, seed=seed)

    def values(self):
        return self._values

    def indices(self):
        return tuple(range(len(self.values())))

    def __getitem__(self, index):
        return self._values[index]

    def __repr__(self):
        return "<{0}>".format(self.__class__.__name__)


Index2D = typing.Tuple[int, int]


class RandUnion(RandGenInterface[Index2D, Inner]):
    """
    Two possible forms of randomization
        Uniform in groups
        Uniform in every possible value
    Currently only (2) provided
    """
    #
    # Magic methods
    #
    def __init__(self, *groups, seed=None):
        super().__init__(self, seed=seed)
        type_check_sequence(groups, RandGenInterface)
        self.groups = groups

    def __repr__(self):
        return str.format(
            "{0}:(of {1})",
            self.__class__.__name__,
            " and ".join([gr.name for gr in self.groups])
        )

    def indices(self):
        for group_index, group in enumerate(self.groups):
            for value_index in range(len(group)):
                yield (group_index, value_index)

    def __getitem__(self, pair):
        return self.groups[pair[0]][pair[1]]


# ==========================================
#   Implementations
#
# ==========================================

class RandIntegers(RandAtomics[int, int]):
    """
    2147483647: largest 32-bit prime number, the 8th Merseine prime number
    """
    _values = (
        -sys.maxsize,
        -2147483647,
        -2,
        -1,
        0,
        1,
        2,
        2147483647,
        sys.maxsize,
    )

class RandFloats(RandAtomics[int, float]):
    _values = (
        -1e309,  # inf
        -1e308,
        -float(sys.maxsize),  # float equivalent of maximum int
        -2147483647.0,
        -math.pi,
        -math.exp(1),
        -2.0,
        -1.0,
        -1.0/1e308,  # greatest number less than zero
        -1.0/1e309,  # ~ 0
        0.0,
        1.0/1e309,  # rounded to zero
        1.0/1e308,  # smallest number less than zero
        1.0,
        2.0,
        math.exp(1),
        math.pi,
        2147483647.0,
        float(sys.maxsize),
        1e308,
        1e309,  # should be inf
    )

class RandBools(RandAtomics[int, bool]):
    _values = (True, False)

class RandTruthy(RandAtomics[int, typing.Any]):
    _values = (
        True, "x", (12, ), [False], {None: None}, 
    )

class RandFalsy(RandAtomics[int, typing.Any]):
    _values = (
        False, str(), tuple(), list(), dict(), None
    )



class RandStrings(RandAtomics[int, str]):
    """
    Random string, drawn from all valid unicode letters.
    """
    alphabet = [
        chr(i)
        for i in range(sys.maxunicode)
        if unicodedata.category(chr(i)).startswith('L')
    ]

    @classmethod
    def rand(cls, maxlength=80):
        randlength = random.randrange(0, maxlength)
        return u''.join([random.choice(cls.alphabet) for _ in range(randlength)])

    @property
    def _values(self):
        return (
            "",
            # Quotes in quotes in quotes
            "'", "''",
            '\"', '\\"', '""', '\"\"', '\\"\\"',
            "\\", "\\\\",
            "\'", "\'\'", "\\'", "\\'\\'", "\\\'",
            "\"", "\"\"", "\\\"","\\\"\\\"", "\\\\",
            "\a", "\\\a",  # ASCII Bell
            "\b", "\\\b",  # ASCII Backslash
            "\f", "\\\f",  # ASCII Formfeed
            "\n", "\\\n",  # ASCII Linefeed
            "\r", "\\\r",  # ASCII Carriage Return
            "\v", "\\\v",  # ASCII Vertical Tab
            "\t", "\\\t",  # Tab
            # Little Bobby Tables: https://xkcd.com/327/
            "Robert'); DROP TABLE Students;--",
            "eval(\"print(\'Hello\')\")",
            "eval(\"raise Exception()\")",
            'eval("eval(\"eval(\\\"3\\\")\")")',
            self.rand(), self.rand(), self.rand(), self.rand(), self.rand(),
            self.rand(), self.rand(), self.rand(), self.rand(), self.rand(),
            self.rand(), self.rand(), self.rand(), self.rand(), self.rand(),
        )


class RandPoliteStrings(RandStrings):
    """
    Random string from characters considered to be printable
    (by the string module). This includes digits, upper and lowercase
    letters, punctuation, and whitespace.
    """
    alphabet = string.printable



class RandLists(RandAtomics[int, list]):
    _values = (
        [],
        ['x'],
        [[]],
        [1],
        [[[]]],
        ['x', []],
        [[]]*10000  # obnoxiously huge list
    )






rs = RandString()


print()
print("rs:", type(rs), rs)
print()
import ipdb
ipdb.set_trace()
print()
