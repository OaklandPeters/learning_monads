from ...support.typecheckable import TypeCheckableMeta, meets
from ...support.methods import abstractclassproperty

from .element import Element
from .morphism import Morphism


class Category(metaclass=TypeCheckableMeta):
    """
    AbstractBaseClass for categories.
    """
    @abstractclassproperty
    def Element(cls) -> Element:
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls) -> Morphism:
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Category:
            return meets(C, cls.__abstractmethods__)
        return NotImplemented
