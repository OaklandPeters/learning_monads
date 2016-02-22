from abc import abstractclassmethod

from ...support.typecheckable import TypeCheckableMeta


class Element(metaclass=TypeCheckableMeta):
    pass
    def apply(self, morphism: 'Morphism') -> 'Element':
        return NotImplemented
