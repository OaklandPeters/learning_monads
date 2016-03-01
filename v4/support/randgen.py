#!/User/bin/env python3
"""
Used for randomly generating data instances for unit-tests.
Little ad-hoc replacement for QuickCheck

Existing quick-check like libraries which could be used for this purpose, or
used as inspiration for better class structure:
    https://github.com/DRMacIver/hypothesis




@todo: Determine whether I want this to look like a Sequence or a Mapping, and they inherit/rebuild from that.
@todo: After practicing with this, determine if it needs .deterministic() and .pairs()
"""
import typing
import random
from abc import abstractmethod, ABCMeta, abstractproperty
import collections

import sys

import string
import unicodedata
import unittest

from .typecheckable import meets

maxint = sys.maxsize

# Typedefs
Inner = typing.TypeVar('Inner')
Index = typing.TypeVar('Index')
Pair = typing.Tuple[Index, Inner]


class RandGenInterface(collections.abc.Sequence, typing.Generics[Index, Inner], metaclass=ABCMeta):
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
    @abstractproperty
    def seed(self) -> int:
        return NotImplemented

    @abstractproperty
    def Random(self) -> random.Random:
        return NotImplemented

    #
    # Derived methods
    #
    def values(self) -> typing.Iterable[Inner]:
        for index in self.indices():
            yield self[index]

    def deterministic(self) -> typing.Iterator[Pairs]:
        for index in self.indices():
            yield (index, self[index])

    def pairs(self) -> typing.Sequence[Pairs]:
        if not hasattr(self, '_pairs'):
            self._pairs = tuple(self.deterministic())
        return self._pairs

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


class RandAtomic(RandGenInterface[int, Inner]):
    """Refined convenience abstract class.
    Requires only a single abstract *property*: _values
    Which is usually implemented at the class level
    """   
    @abstractproperty
    def _values(self) -> typing.Sequence:
        return NotImplemented

    # Mixin methods
    def __init__(self, seed=None):
        super().__init__(self, seed=seed)

    def values(self):
        return self._values

    def indices(self):
        return tuple(range(len(self.data)))

    def __getitem__(self, index):
        return self._values[index]

    def __repr__(self):
        return str.format(
            "{0}:({1})", self.__class__.__name__
        )


IndexPair = typing.Tuple[int, int]

class RandUnion(RandGenInterface[IndexPair, Inner]):
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

class RandInteger(RandAtomic):
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

class RandString(RandAtomic):
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



class RandList(RandAtomic):
    _values = (
        [],
        ['x'],
        [[]],
        [1],
        [[[]]],
        ['x', []],
        [[]]*10000  # obnoxiously huge list
    )






class PoliteString(String):
    """
    Random string from characters considered to be printable (by the string module). This includes digits, upper and lowercase letters, punctuation, and whitespace.
    """
    #String of characters which are considered printable. This is a combination of digits, letters, punctuation, and whitespace.
    alphabet = string.printable






    
class TestSupportBase(unittest.TestCase):
    klass = NotImplemented  # abstract
    def grab(self, N=10):
        for i in range(N):
            yield self.klass()


class IRandTestSupport:
    def test_irand(self):
        iterator = self.klass.irand()
        for i in range(10):
            instance = next(iterator)
            self.assertTrue(isinstance(instance, self.klass))
            

class StringTests(IRandTestSupport, TestSupportBase):
    klass = String
    def test_string_parent(self):
        for instance in self.grab():
            self.assertTrue(isinstance(instance, str))


class PoliteStringTests(StringTests):
    klass = PoliteString

class IntegerTests(IRandTestSupport, TestSupportBase):
    klass = Integer
    def test_int_parent(self):
        for instance in self.grab():
            self.assertTrue(isinstance(instance, int))

class PositiveIntegerTests(IntegerTests, TestSupportBase):
    klass = PositiveInteger
    def test_positive(self):
        for instance in self.grab():
            self.assertTrue(instance > 0)
