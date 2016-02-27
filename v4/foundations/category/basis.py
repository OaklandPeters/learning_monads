from ...support.typecheckable import TypeCheckableMeta
from ...support.methods import abstractpedanticmethod


class Applicative(metaclass=TypeCheckableMeta):
    @abstractpedanticmethod
    def apply(cls, element: 'Element', morphism: 'Morphism') -> 'Element':
        return NotImplemented
