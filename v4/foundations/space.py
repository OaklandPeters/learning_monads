from ..support.typecheckable import TypeCheckableMeta
from ..support.methods import pedanticmethod, abstractpedanticmethod, abstractclassproperty
from ..basis import Caller, Applicative


class Morphism(Caller, metaclass=TypeCheckableMeta):
    pass


class MorphismSugar(Morphism):
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)


class Element(Applicative, metaclass=TypeCheckableMeta):
    pass


class Space(metaclass=TypeCheckableMeta):
    @abstractclassproperty
    def Element(cls):
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls):
        return NotImplemented
