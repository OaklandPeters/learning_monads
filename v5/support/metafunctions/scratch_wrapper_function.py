"""
A simple(ish) decorator, intended to construct classes to act as wrappers.
I hope that this can take over some of the roels of Haskell's newtype.

When you basically just want to decorate a function, but give it
a readable name, and *maybe* type check on it, while making the
wrapped object still accessable
"""



# =======================================
#   SIMPLE: Pythony example: compose
# =======================================

def compose(left, right):
    """Functional method."""
    def wrapper(element):
        return right(left(element))
    return wrapper


class Composition:
    """OOP method"""
    def __init__(self, left, right):
        self.left = left
        self.righ = right

    def __call__(self, element):
        return self.right(self.left(element))

class Composition2:
    """OOP, to fit this style (one argument)."""
    def __init__(self, *args):
        self.value = args

    def __call__(self, element):
        left, right = self.value
        return right(left(element))

def stub_wrapper(x):
    return x

@stub_wrapper
def Composer(element):
    left, right = self.value
    return left(right(element))


def basic_wrapper(function):
    class BasicWrapper:
        @property
        def wrapped(self):
            """Puts function in the namespace of the class."""
            return function

        def __init__(self, *args):
            self.value = args

        def __call__(self, element):
            return self.wrapped(self, element)

        def __repr__(self):
            return str.format(
                "{0}(wrapped={1}, value={2})",
                self.__class__.__name__,
                self.wrapped.__name__,
                repr(self.value)
            )

    return BasicWrapper


import abc
from .

class WrapperType(metaclass=abc.ABCMeta):
    """
    REALIZATION: This may be best expressed as a metafunction on a Category,
        similar to how generic_function.py works on Category.
    This particular implementation corresponds to a metafunction on Pysk. (well, a version of pysk + *args)
    But.... I could rephrase it in terms of category methods, and make it specific to a category.
    So thsi would become:
    
    @Wrapper(Pysk)
    def Composed(self, element):
        ....

    class Wrapper()
    """
    @abc.abstractproperty
    def wrapped(self):
        return self._wrapped

    def __init__(self, *args):
        self.value = args

    def __call__(self, element):
        return self.wrapped(self, element)

    def __repr__(self):
        return str.format(
            "{0}(wrapped={1}, value={2})",
            self.__class__.__name__,
            self.wrapped.__name__,
            repr(self.value)
        )

class Wrapper(abc.ABCMeta):
    """
    A metaclass, intended to be used as a decorator function.
    """
    def __new__(mcls, name, bases, namespace):
        



@Wrapper
def Composed(self, element):
    left, right = self.value
    return right(left(element))


add3 = lambda x: x+3
mul4 = lambda x: x*4

comp1 = Composed(add3, mul4)
comp2 = Composed(mul4, add3)

print()
print("Composed:", type(Composed), Composed)
print()
import ipdb
ipdb.set_trace()
print()


# =======================================
# HARD: Haskelly example: Kleisli
# =======================================
# newtype Kleisli m a b = Kleisli { runKleisli :: a -> m b}

class Kleisli:
    """
    Class-based method
    """
    def __init__(self, value):
        pass
