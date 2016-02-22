"""
Stubs for group-theory classes.



Group-like structures
                Totality Associativity  Identity  Divisibility  Commutativity
            ---------------------------------------------------------------
Semicategory  | Unneeded    Required    Unneeded    Unneeded    Unneeded
Category      | Unneeded    Required    Required    Unneeded    Unneeded
Groupoid      | Unneeded    Required    Required    Required    Unneeded
Magma         | Required    Unneeded    Unneeded    Unneeded    Unneeded
Quasigroup    | Required    Unneeded    Unneeded    Required    Unneeded
Loop          | Required    Unneeded    Required    Required    Unneeded
Semigroup     | Required    Required    Unneeded    Unneeded    Unneeded
Monoid        | Required    Required    Required    Unneeded    Unneeded
Group         | Required    Required    Required    Required    Unneeded
Abelian Group | Required    Required    Required    Required    Required

* Defining trait: binary operation, closed under operation
* For clarity, I'll *probably* seperate around Totality --> Category VS Group on the Morphism VS Element divide.
* Closure <--> Totality, but I forget why this must be true

@todo: 
@todo: Each of these probably has associated-laws that I could write unit-tests for.
@todo: Each of these probably has utility functions associated
"""
from typing import TypeVar, Generic
from abc import abstractmethod, abstractclassmethod, ABCMeta
from collections import Callable

from support_pre import abstractclassproperty, abstractpedanticmethod, pedanticmethod


# Placeholder for brevity
_abstractpedanticmethod = lambda : abstractpedanticmethod(lambda cls, self: NotImplemented)
_abstractclassmethod = lambda : abstractclassmethod(lambda cls: NotImplemented)


# ==============================================
#   Category-related
#       Based on functions/morphisms
#       Not total/closed, becuase not all morphisms
#       can be composed
# ==============================================


class Composable:
    """ Associativity """
    compose = _abstractpedanticmethod()  # binary

class Identifiable:
    """ Identity """
    identity = _abstractclassmethod()

class Invertible:
    """ Divisibility """
    invert = _abstractclassmethod()

class Category(Composable, Identifiable):
    pass

class Groupoid(Identifiable, Composed, Invertible):
    """ Not often used, because very few real-world
    morphisms can be inverted."""
    

# ==============================================
#   Category-related
#       Based on functions/morphisms
#       Not total
# ==============================================

class Zeroable:
    """ Identity """
    zero = _abstractclassmethod()

class Associative:
    """ Associative """
    append = _abstractpedanticmethod()

class Divisible:
    """ Divisible """
    extract = _abstractpedanticmethod()

class Semigroup:
    pass

class Monoid:
    pass

# ==============================================
#   More speculative
#       Usually because it's my own terminology
# ==============================================
LeftType = TypeVar('LeftType')
RightType = TypeVar('RightType')
class Binary(Generic[Left], metaclass=ABCMeta):
    @abstractpedanticmethod
    def operation(cls, left: LeftType, right: Rig)

class BinaryClosed(Generic[Element], metaclass=ABCMeta):
    """Could probably call this BinaryClosed."""
    @abstractpedanticmethod
    def operation(cls, left: Element, right: Element) -> Element:
        return NotImplemented
