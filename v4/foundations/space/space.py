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
    pass


class Space(metaclass=TypeCheckableMeta):
    @abstractclassproperty
    def Element(cls):
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls):
        return NotImplemented
