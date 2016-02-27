from ...support.typecheckable import TypeCheckableMeta
from ...support.methods import abstractclassproperty

from .element import Element
from .morphism import Morphism


class Category(metaclass=TypeCheckableMeta):
    """
    
    """
    @abstractclassproperty
    def Element(cls) -> Element:
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls) -> Morphism:
        return NotImplemented
