"""
Convenience functions for creating versions of Category/Element/Morphism
with 'standard' level behavior.

Right now, these are stubs - and will need to be replaced with metaclass-type
things later. Inspiration for those metaclasses should be drawn from typing.py.
"""
from typing import Any, Callable

from ...support.typecheckable import TypeCheckableMeta
from .category import Category, Element, Morphism

class StandardCategory:
    """Stub. Will need to be a metaclass thing later."""
    def __new__(cls, element, morphism):
        class _Category(Category):
            Element = element
            Morphism = morphism
        return _Category


# ===================================
#   Metaclass approach
#
# ===================================

#    UNFINISHED - so the names are intentionally weird

class StandardMeta(TypeCheckableMeta):
    """
    The approach to building the StandardCategory/StandardElement/StandardMorphism
    is to use their individual __new__ methods to define the interface, then
    defer to StandardMeta.__new__ to actually build the class.
    """
    def __new__(cls, name, bases, namespace):
        return super().__new__(cls, name, bases, namespace)

class StandardTypeChecker(TypeCheckableMeta):
    """
    @todo: Should this have (metaclass=ABCMeta), to enable abstract checks? Or will that create diamond-pattern errors for metaclasses when merging with Element (which uses TypeCheckableMeta)
    """
    @abstractclassproperty
    def _instancechecker_data(cls):
        return NotImplemented

    @abstractclassproperty
    def _subclasschecker_data(cls):
        return NotImplemented

    @classmethod
    def __instancecheck__(cls, instance):
        return isinstance(instance, cls._instancechecker_data)

    @classmethod
    def __subclasscheck__(cls, subclass):
        return issubclass(subclass, cls._subclasschecker_data)


class StandardElement_usingMeta(StandardMeta, metaclass=StandardMeta):
    def __new__(cls, name='Element', element_type=typing.Any):

        self = super().__new__(cls, name, (Element, StandardTypeChecker), {})
    


class StandardMorphism_usingMeta(StandardMeta, metaclass=StandardMeta):
    def __new__(cls, morphism_type):
        self = super().__new__(cls, 'Morphism', ())


class StandardCategory_usingMeta(StandardMeta, metaclass=StandardMeta):
    """
    @todo: Validate element_type, morphism_type as TypeCheckable
    """
    def __new__(cls, name, element_type, morphism_type):
        Element = 
        self = super().__new__(cls, name, (), {'Element': element_type, 'Morphism': morphism_type})

