"""

Key things here are the way that foldable interacts with Zeroable/SemiGroup/Monoid:


class Foldable(Generic[InType, OutType]):
    @abstractpedanticmethod
    def foldr(cls,
              self: 'Foldable[InType, OutType]',
              function: Callable[[InType], OutType],
              initial: OutType) -> OutType:
        """
        The initial is also used as the accumulator."""
        return NotImplemented


class Zeroable:
    """In most cases, this indicates a container that can be 'empty'."""
    @abstractclassmethod
    def zero(cls):
        return NotImplemented


class SemiGroup(Generic[Element]):
    @abstractpedanticmethod
    def append(self, other: 'SemiGroup[Element]') -> 'SemiGroup[Element]':
        return NotImplemented


class Monoid(Zeroable, SemiGroup):
    ""
    > In Haskell, the Monoid typeclass (not to be confused with Monad) is a class for types which have a single most natural operation for combining values, together with a value which doesn't do anything when you combine it with others (this is called the identity element). It is closely related to the Foldable class, and indeed you can think of a Monoid instance declaration for a type m as precisely what you need in order to fold up a list of values of m.
    ""
    @classmethod
    def flatten(cls, foldable: Foldable):
        ""Fold a structure, using the rules of this monoid.
        Haskell calls this 'mconcat'.
        sum = lambda foldable_list_of_ints: AdditionMonoid.flatten(foldable_list_of_ints)
        ""
        return foldable.foldr(cls.append, cls.zero())


class Reducable(Foldable, Zeroable):
    @pedanticmethod
    def reduce(cls, self, function):
        return cls.foldr(self, function, cls.zero())


class Joinable(Foldable, Zeroable, SemiGroup):
    @pedanticmethod
    def join(cls, self):
        ""Uses the natural append operation of a monoid in a foldr.
        Haskell calls this 'fold'.
        ""
        return cls.foldr(self, cls.append, cls.zero())
"""
