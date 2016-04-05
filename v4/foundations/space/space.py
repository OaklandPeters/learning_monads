from collections import Callable

from ...support.typecheckable import TypeCheckableMeta
from ...support.methods import pedanticmethod, abstractpedanticmethod, abstractclassproperty


class Morphism(Callable, metaclass=TypeCheckableMeta):
    @abstractpedanticmethod
    def call(cls, self: 'Morphism', element: 'Element') -> 'Element':
        return NotImplemented


class MorphismSugar(Morphism):
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)


class Element(metaclass=TypeCheckableMeta):
    @abstractpedanticmethod
    def apply(cls, self: 'Element', morphism: 'Morphism') -> 'Morphism':
        return NotImplemented


class Space(metaclass=TypeCheckableMeta):
    @abstractclassproperty
    def Element(cls):
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls):
        return NotImplemented

    @abstractclassmethod
    def call(cls, morphism: 'Morphism', element: 'Element') -> 'Element':
        return NotImplemented

    @abstractclassmethod
    def apply(cls, element: 'Element', morphism: 'Morphism') -> 'Morphism':
        return NotImplemented