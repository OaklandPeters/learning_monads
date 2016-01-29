"""
Randomized Category/Type Based Unit-Testing Tools


This file also provides tools for generating and testing randomized data
and functions. I can't recall the name for this, but there is a school of
unit-test design based on it...
"""
import abc
import random
import itertools

from ..support_pre import classproperty


class CategoryTestingTool(metaclass=abc.ABCMeta):
    """
    @todo: Make BOTH elements and morphisms return along with a unique ID, so that TestingCategory.elements[_id] and TestingCategory.morphisms[_id] work
    """

    def __init__(self, seed=None):
        self.seed = seed
        random.seed(self.seed)

    @property
    def element(self):
        return random.choice(cls.elements)

    @property
    def morphism(self):
        return random.choice(cls.morphisms)
    
    @classproperty
    @abc.abstractmethod
    def elements(cls):
        """Should be a sequence of relevant elements of this category.
        Generally this sequence is *not* randomly generated, although
        '.element' does randomly pull from it."""
        return NotImplemented

    @classproperty
    @abc.abstractmethod
    def morphisms(cls):
        """Should be a sequence of unique names, and unary functions that
        are valid for any element of this category.
        I might need this for binary functions as well...
        """
        return NotImplemented

    @classproperty
    def walk(cls):
        """Generates all pairs"""
        yield from itertools.product(enumerate(cls.element), enumerate(cls.morphisms))


class RandomInteger(CategoryTestingTool):
    """
    @todo: Make this calculate and include the greatest/smallest possible integer on the system.
    """
    elements = (
        -100000000000,
        -2,
        -1,
        0,
        1,
        2,
        100000000000,
    )

    @classproperty
    def morphisms(cls):
        def add_to_itself(x):
            return x + x
        def subtract_from_itself(x):
            return x - x
        def double(x):
            return x*x
        def divide(x):
            return x/x
        def square(x):
            return x**x
        def invert(x):
            return -x
        def boolean_branch(x):
            if x:
                return 1
            else:
                return 0
        return (
            add_to_itself,
            subtract_from_itself,
            double,
            divide,
            square,
            invert,
            boolean_branch
        )

class RandomString(CategoryTestingTool):
    """
    @todo: Find a bunch of examples of strange/edge-case strings
    """
    @classproperty
    def elements(cls):
        return (
            "",
            "1",
            "a",
            "aaa",
            "-",

        )


class RandomAny(CategoryTestingTool):
    """
    Warning: these are not actually Sequences, but Iterators, because generating them
    might be too slow.
    """
    subcategories = (
        RandomInteger,
        RandomString
    )
    @classproperty
    def elements(cls):
        for cat in cls.subcategories:
            yield from cat.elements

    @classproperty
    def morphisms(cls):
        for cat in cls.subcategories:
            yield from cat.morphisms
