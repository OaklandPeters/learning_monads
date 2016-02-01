"""

My issue: there seems to be multiple concepts of Category and Element floating around
in these monad constructions.

To be most correct, to the Haskell organization of things, there are very few categories.
Mostly Hask and Klesi.

But, in my intuition, each Monad defines a Category itself.




"""


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
        