"""
Trying to build up to MaybeArrow, incrementally using every step from the hierarchy 
developed in space/, groups/, and foundations/


@HARD-TASK: To get typechecking of Element/Morphism for all of
MaybeSpace/MaybeCategory/MaybeFunctorCategory/MaybeMonad/MaybeSpace
"""
from ..space.space import Space, Morphism, Element, MorphismSugar

#
# Placeholders for hierarchy
# 
class _MaybeMorphism(Morphism, MorphismSugar):
    call
    __call__
    __instancecheck__  # needs to do run-time typechecking

class _MaybeElement(Element):
    apply
    __instancecheck__  # needs to do run-time typechecking.

class _MaybeSpace(Space):
    call
    apply
    Morphism
    Element

class _MaybeCategory(_MaybeSpace, Category, CategorySugar):
    identity
    compose

# COMPLICATION: Relationship between _MaybeFunctor and _MaybeFunctorCategory
#  Looks like it needs mutual definition.
#  Alternately - _MaybeFunctorCategory needs to be it's own functor instance
#     so it's decorate/construct return type _MaybeFunctorCategory rather than
#     simply _MaybeCategory
class _MaybeFunctor(Functor):
    Domain = MonoPysk
    Codomain = _MaybeCategory
    decorate   # MonoPysk.Morphism -> _MaybeCategory.Morphism
    construct  # MonoPysk -> _MaybeCategory

class _MaybeFunctorCategory(_MaybeCategory, FunctorCategory):
    """I haven't written out or fleshed out FunctorCategory ABC,
    or it's relationship to MaybeFunctor."""
    Domain = MonoPysk
    Codomain = classproperty(lambda cls: cls)
    Functor = _MaybeFunctor

class _MaybeMonad(_MaybeFunctorCategory, Monad):
    bind
    map

class _MaybeCofunctor(Cofunctor):
    Domain = MonoPysk
    Codomain = _MaybeCategory
    corate  # _MaybeCategory.Morphism -> MonoPysk.Morphism
    deconstruct  # _MaybeCategory.Element -> MonoPysk.element

class _MaybeCofunctorCategory(_MaybeCategory, CofunctorCategory):
    Domain = MonoPysk
    Codomain = classproperty(lambda cls: cls)
    Cofunctor = _MaybeCofunctor

class _MaybeComonad(_MaybeCofunctorCategory, Comonad):
    """I haven't decided what the function for this should be called.
    The equivalent of bind/map
    """

class _MaybeBimonad(_MaybeMonad, _MaybeComonad):
    pass

class _MaybeArrow(Arrow):
    """ Do not know the functions here either. Haskell provides first, second, ~branch, ~fanout
    """
    pass








#
#  Older implementations
#
class MaybeCategory(Category):
    def __init__(self, value, initial):
        self.value = value
        self.initial = initial

    @pedanticmethod
    def compose(cls, self: 'cls.Morphism', morphism: 'cls.Morphism') -> 'cls.Morphism':
        @functools.wraps(self.value)
        def wrapped(initial):
            result = self.value(initial)
            if result is None:
                return morphism.value(initial)
            else:
                return result
        return cls(wrapped, None)

    @staticmethod
    def _identity(value):
        return None

    @classproperty
    def identity(cls):
        return cls(cls._identity, None)

    @pedanticmethod
    def call(cls, self: 'cls.Morphism', element: 'cls.Element'):
        """Use the first non-None between:
            element.value and result=self.value(element.initial)
        """
        if element.value is None:
            return cls(self.value(element.initial), element.initial)
        else:
            return cls(element.value, element.initial)

    @pedanticmethod
    def apply(cls, self: 'cls.Element', morphism: 'cls.Morphism') -> 'cls.Element':
        """
        NOTE: morph.__call__ isn't working, because it defers to .map, which isn't working.
        """
        return cls.call(morphism, self)

    def __repr__(self):
        return Pysk.__repr__(self)

    def __str__(self):
        return Pysk.__str__(self)

    def __call__(self, element):
        return self.call(element)

    @classproperty
    def Category(cls):
        """This will go awry during inheritance."""
        return cls

    def __eq__(self, other):
        if hasattr(self, 'Category') and hasattr(other, 'Category'):
            if issubclass(other.Category, self.Category):
                return (self.value == other.value) and (self.initial == other.initial)
        return False


class MaybeFunctor:
    @classmethod
    def dispatch(cls, obj):
        """Convenience function for constructing."""
        if obj == cls.Domain.identity:
            return cls.Codomain.identity
        elif cls.Domain.is_element(obj):
            return cls.construct(obj)
        elif cls.Domain.is_morphism(obj):
            return cls.decorate(obj)
        else:
            raise CategoryError(str.format(
                "Argument is not an object in Domain {0}", cls.Domain.__name__))


    @classproperty
    def Object(cls):
        return typing.Union[cls.Domain.Element, cls.Domain.Morphism]

    @classproperty
    def Domain(cls):
        return Pysk

    @classproperty
    def Codomain(cls):
        return MaybeCategory

    @classproperty
    def identity_morphism(cls):
        return cls(_constant(None), None)

    @classmethod
    def construct(cls, element: 'cls.Domain.Element') -> 'cls.Codomain.Element':
        return cls(None, element)

    @classmethod
    def decorate(cls, morphism: 'cls.Domain.Morphism') -> 'cls.Codomain.Morphism':
        return cls(morphism, None)

    @pedanticmethod
    def is_element(cls, obj):
        return isinstance(obj, Maybe)

    @pedanticmethod
    def is_morphism(cls, obj):
        if isinstance(obj, Maybe):
            if callable(obj):
                return True
        return False


class Maybe(MaybeCategory, MaybeFunctor, Monadic):
    """
    value - morphisms hold function here, and elements hold results
    initial - for elements only, holds initial argument

    """
    def __init__(self, *args):
        # Case 1 - no arguments --> identity morphism
        if len(args) == 0:
            #self.value = _constant(None)  # might have to set = _constant(None)
            self.value = self.Codomain._identity
            self.initial = None
        # Case 2 - only 1 thing passed in
        # I'd REALLY like to handle this in Functor
        # But I don't know how yet
        elif len(args) == 1:
            # Morphism
            if callable(args[0]):
                # Special case
                if args[0] == self.Domain.identity:
                    self.value = self.Codomain._identity
                    self.initial = None
                else:
                    self.value = args[0]
                    self.initial = None
            # Element
            else:
                self.value = None
                self.initial = args[0]
        # Case 3 - two things passed in
        elif len(args) == 2:
            self.value, self.initial = args[0], args[1]

    Category = MaybeCategory

    @pedanticmethod
    def flatten(cls, element):
        """@todo - write this"""
        pass

    @pedanticmethod
    def map(cls,
            elm: 'MaybeCategory.Element',
            constructor: 'Callable[Pysk.Element, [MaybeCategory.Element]]'
            ) -> 'MaybeCategory.Element':

        return cls.flatten(cls.apply(elm, constructor))

    @pedanticmethod
    def bind(cls,
             morphism: 'cls.Codomain.Morphism',
             constructor: 'Callable[cls.Domain.Element, [cls.Codomain.Element]]'
             ) -> 'cls.Codomain.Element':
        """
        In Haskell, this is called 'Klesli composition', using symbol: >=>
        'f_compose' ~ functor-specific composotion

        (C1 -> C2, D2 -> C3) -> C3
        """
        @functools.wraps(constructor)
        def wrapped_constructor(element):
            return cls.flatten(cls.apply(element, constructor))
        return cls.compose(morphism, wrapped_constructor)

    @pedanticmethod
    def bind(cls, self: 'cls.Morphism', func: 'Pysk.Morphism') -> 'cls.Morphism':
        """Basically compose. Should put func at the end of the chain."""
        return self.compose(Maybe(func))

    @pedanticmethod
    def __rshift__(cls, self, arg):
        """
        Chain(f) >> g == Chain(compose(f, g))
        Chain(f) >> x == Chain(f(x))
        Chain(x) >> f == Chain(f(x))
        Pipe(x) >> y -> TypeError

        This method means this works as well:
            value = Maybe()
            value >>= f
            value >>= x

        """
        if not isinstance(arg, cls):
            arg = cls(arg)

        if callable(self.value) and callable(arg.value):
            return self.compose(arg)
        elif callable(self.value) and not callable(arg.value):
            return self.call(arg)
        elif not callable(self.value) and callable(arg.value):
            return self.apply(arg)
        elif not callable(self.value) and not callable(arg.value):
            raise TypeError("Operator 'Pipe(...) >> X', X must be callable")
        else:
            raise TypeError("Case fall-through error. This should never occur")


    @pedanticmethod
    def __lshift__(cls, self, arg):
        if callable(self.value) and callable(arg):
            return Pysk.compose(arg, self.value)
        elif callable(self.value) and not callable(arg):
            return self.value(arg)
        elif not callable(self.value) and callable(arg):
            return arg(self.value)
        elif not callable(self.value) and not callable(arg):
            raise TypeError("'Pipe() >> argument << argument' is invalid")
        else:
            raise TypeError("Case fall-through error. This should never occur")