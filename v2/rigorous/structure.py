"""

My issue: there seems to be multiple concepts of Category and Element floating around
in these monad constructions.

To be most correct, to the Haskell organization of things, there are very few categories.
Mostly Hask and Klesi.

But, in my intuition, each Monad defines a Category itself.




@todo: Add abstract methods to Functor-->Monad stack
"""


#
#   Functor --> Monad stack
#       Honestly, this stack seems much too complicated
#

class Functor:
    pass

class Alt(Functor):
    pass

class Plus(Alt):
    pass

class Apply(Functor):
    pass

class Applicative(Apply):
    pass

class Alternative(Applicative, Plus):
    pass

class Bind(Apply):
    pass

class Monad(Bind):
    pass

class MonadPlus(Monad, Alternative):
    pass


class SemiGroup:
    pass

class Monoid(SemiGroup):
    pass

#
#  Extra bullshit I'd like to see
#  
class Foldable:
    pass

class Traversable(Foldable, Functor):
    pass

class MonadFix(Monad):
    pass

class Comonoid:
    pass

class Comonad(Comonoid):
    pass


class GentleMonad(MonadPlus, MonadFix, Traversable, Comonad):
    pass








class Functor:
    @classproperty
    def Domain(cls) -> Category:
        """Input type(s).
        """
        pass

    @classproperty
    def Codomain(cls) -> Category:
        """Output"""
        pass

    @classmethod
    def f_apply(cls, element: Codomain.Element, function: Domain.Morphism) -> Domain.Element:
        """
        """

    @classmethod
    def f_map(cls, function: Domain.Morphism) -> Codomain.Morphism:
        """
        """

class Applicative(Functor):
    """
    """
    @classmethod
    def lift(cls, value):
        
