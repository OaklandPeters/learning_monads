"""
REALIZATION: This *might* best be expressed as a metafunction on a Category,
    similar to how generic_function.py works on Category.
    (actually, I suspect this will require the Category have Functor and Arrow as well)

This particular implementation corresponds to a metafunction on Pysk. (well, a version of pysk + *args)
But.... I could rephrase it in terms of category methods, and make it specific to a category.
So thsi would become:

@Wrapper(Pysk)
def Composed(self, element):
    ....
"""

import abc
from ..pysk import Pysk


class WrapperType(metaclass=abc.ABCMeta):
    """
    
    class Wrapper()
    """
    @abc.abstractproperty
    def wrapped(self):
        return NotImplemented

    def __init__(self, *args):
        self.value = args

    def __call__(self, element):
        return self.wrapped(self, element)

    def __repr__(self):
        return str.format(
            "{0}({1})",
            self.__class__.__name__,
            repr(self.value)
        )


class WrapperF(abc.ABCMeta):
    """
    A metaclass, intended to be used as a decorator function.

    @WrapperF
    def Composed(self, element):

    """
    def __new__(mcls, function):
        cls = type(function.__name__, (WrapperType, ), {'wrapped': function})
        return cls



class WrapperCType(abc.ABCMeta):
    @abc.abstractproperty
    def wrapped(self):
        return NotImplemented

    @abc.abstractproperty
    def Category(self) -> 'FunctorCategory':
        return NotImplemented

    def __init__(self, *args):
        self.value = self.Category.construct(*args)

    def __call__(self, element):
        return self.Category.call(self.wrapped, element)

    def __repr__(self):
        return str.format(
            "{0}({1})",
            self.__class__.__name__,
            repr(self.value)
        )

class WrapperCMeta(abc.ABCMeta):        
    def __new__(mcls, category, function):
        return type(function.__name__, (WrapperType, ),
                    {'_wrapped': function, 'category': category})


class WrapperC:
    """
    Basically, wrapperF, but asks for a category first.
    @WrapperC(Pysk)
    def Composed(self, element):
        left, right = self.values
        return right(left(element))

    """
    def __init__(self, category):
        self.category = category

    def __call__(self, function):
        return WrapperCMeta(self.category, function)


@WrapperF
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
