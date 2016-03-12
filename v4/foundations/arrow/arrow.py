"""
This is more notes, than an actual workable idea at this point.

NOTICE: Most of these implementations based on Haskell
will not work, because Haskell's depend on currying.

In particular:
    An arrow is: (a, b, c)
    For OrdinaryArrow:
        arr f = f
    Because f::b->c
    So, I'll have to do something to enable functions to manipulate the output (c)

    For somewhat related reasons, I expect that _arrow_swap isn't easily definable, and identity may not be derivable (ie it needs to be defined independently for arrows)
"""
import typing

from ...support.methods import (
    abstractclassmethod, abstractclassproperty,
    abstractpedanticmethod, pedanticmethod,
)

from ..category.category import Category
from ..category.morphism import Morphism


# Argument
A = typing.TypeVar('A')
# InputType
B = typing.TypeVar('B')
# OutputType
C = typing.TypeVar('C')


class Arrow(Morphism, typing.Generic[A, B, C]):
    """

    Arrows basically just wrap morphisms, and do some extra shit.


    NEED FOR CLARITY: Haskell seems to be using 'arrow' to refer to basically a morphism inside a particular arrow category. I'll need some terminology to distinguish ~ Category-vs-Morphism, but for Arrows.
    NEED FOR CLARITY: where Arrow class should fit into the hierarchy.
        BECAUSE: Category and Monad are not related in Haskell's version of things, and Element/Morphism is not explicitly represented at all.
    """
    @abstractclassmethod
    def arr(cls, function) -> 'cls':
        """
        'lift a function to an arrow'
        Basically the constructor for the arrow

        UNSURE: if morphism needs to be a pure function, or is basically a
            morphism from a domain-category.

        :: (b -> c) -> (a, b, c)
        """

    @abstractpedanticmethod
    def first(cls, arrow):
        """
        Builds a new arrow out of an existing arrow, by 
        Send the first component of the input through the argument arrow, and copy the rest unchanged to the output.

        :: (a, b, c) -> a (b, d) (c, d)
        """

    # ============================
    #  Mixin methods
    # ============================
    # NOTE: I don't know how to implement or derive any of these yet
    @pedanticmethod
    def second(cls, arrow):
        """
        This most likely will not execute in its current form, but does communicate the idea.
        
        swap: trades places of pre and post
        """
        return cls.compose(
            cls.compose(
                cls.arr(_swap),
                cls.first(arrow)
            ),
            cls.arr(_swap)
        )

    @pedanticmethod
    def split(cls, left, right):
        """
        (***) :: a b c -> a b' c' -> a (b, b') (c, c')

        Split the input between the two argument arrows and combine their output. Note that this is in general not a functor.
        """
        return cls.compose(cls.first(left), cls.second(right))

    @pedanticmethod
    def fanout(cls, left, right):
        """
        (&&&) :: a b c -> a b c' -> a b (c, c')

        Fanout: send the input to both argument arrows and combine their output.
        """
        return cls.compose(
            cls.arr(lambda x: tuple(x, x)),
            cls.split(left, right)
        )

    @classmethod
    def identity(cls):
        """
        returnA :: Arrow a => a b b Source

        The identity arrow, which plays the role of return in arrow notation.

        PERSONAL NOTE: I'm not confident this is actually derivable
        """
        return cls.arr(_identity)

    @pedanticmethod
    def precomposition(cls, self, function):
        """
        Precomposition with a pure function.
        """

    @pedanticmethod
    def postcomposition(cls, self, function):
        """
        Post-composotion with a pure function
        """

    @pedanticmethod
    def composition(cls, left, right):
        """
        Right-to-left composition of morphisms within a category.

        NOTE TO SELF: this needs to be on a subclass
        """


class ArrowCategory(Category):
    """
    A category, defined in terms of Arrows rather than standard morphisms
    """
    @abstractclassproperty
    def Morphism(cls) -> 'Arrow':
        return NotImplemented


# ======================================
#   Concrete Implementations
# ======================================
class OrdinaryArrow(Arrow):
    """Haskell ordinary.  a -> b
    """
    def __init__(self, func):
        self.value = func

    @classmethod
    def arr(cls, func):
        return cls(func)

    @pedanticmethod
    def split(cls, left, right):
        def _split(x, y):
            return (left(x), right(y))
        return cls.arr(_split)

    @pedanticmethod
    def first(cls, arrow):
        return cls.split(arrow, cls.identity)

    @pedanticmethod
    def second(cls, arrow):
        return cls.split(cls.identity, arrow)


def kleisli(_Monad, function):
    """
    Note 
    """
    return _Monad(function)

class Kleisli:
    def __init__(self, value):
        self.value = value

    def __call__(cls)

@wrapper
def Kleisli(value):


class MonadicCategory(Monad):
    """Uses Monad and kleisli function to construct category.
    Personal note: this hints at a method of constructing a more lightweight
    monadic object, that doesn't bear so much weight. Basically, a monad
    without the categorical contex (and hence the need to construct
    category, functor, element, morphism objects).
    """
    def identity(cls, value):
        return kleisli(cls, )

class KleisliArrow(Arrow):
    """
    Arrows of a monad.
    """
    @classmethod
    def identity(cls):




# ==================================
#  Examples of arrows
#    which are generic to all
#    arrow categories.
# ==================================
def split(_Arrow: 'Type[Arrow]') -> 'Arrow[A, B, [B, B]]':
    """Constructs an arrow for ArrowCategory _Arrow, which Splits a single value into a pair of duplicate values."""
    return _Arrow.arr(lambda x: tuple(x, x))

def _uncurry(func1):
    def uncurryer1(b):
        def uncurryer2(c):
            return func1(b, c)
        return uncurryer2
    return uncurryer1

def unsplit(_Arrow: 'Type[Arrow]') -> 'Callable[[b, c], d] -> [a, [b, c], d]':
    """Combines a pair of values into a single value
    """
    return Pysk.compose(_Arrow.arr, _uncurry)

def parallel(F: 'Arrow', G: 'Arrow'):
    pass



# ==================================
#  My personal thoughts on
#     arrow-generic functions
# ==================================
# One concern: having branch and combine as seperate functions
#    makes the branch process change Categories, since branch
#    returns a tuple or list.
#    
#    Haskell gets around this by making the functions (***) and (&&&)
# combine *before* returning.
# 
# The arrow process might be thought of as a way to do something
# who's input and output are in the category, but internals are not.
# 

def _branch(*functions):
    def wrapper(arg):    
        return tuple(func(arg) for func in functions)
    return wrapper

def Branch(_Arrow):
    return _Arrow.arr(_branch)

def branch(arrow):
    """
    Would like to use this like:
        arrow = MyArrow(function)
        branch(arrow)(function1, function2, function3, ...)
    Alternately:
        arrow >> branch | (function1, function2)
        ... I don't know which symbol should be where I'm writing '|'
    """
    return arrow.compose(arrow.arr(Branch))


# ==================================
#    Utility functions
# ==================================
def _swap(x, y):
    return tuple(y, x)

def _arrow_swap(arrow):
    return arrow.arr(arrow.post, arrow.pre)

def _identity(x):
    return x
