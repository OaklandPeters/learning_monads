"""
This is a listing of all types of methods I've discerned that are needed.
By this, I mean, after I take the Functor/Applicative/Monad + Monoid hierarchy,
and realize that I need to double the number of functions, to account for
the fact that I need seperate functions for Data (Objects) VS Functions (Morphisms)
-- which Haskell does not.


Function::(a -> b)
    A normal function, in the pre-category.
Constructor::(a -> m b)
    A function from pre-category, into the monad category.
Endofunction::(m a -> m b)
    Basically a morphism in the category.
Outrofunction::(m a -> b)
    Not particularly used. Corresponds to comonads (I think)

Domain Element::a
Element::m a
"""

class MyMonad:

    @classproperty
    def domain(cls: Monad):
        pass
    @classproperty
    def codomain(cls: Monad):
        pass
    @classproperty
    def objects(cls):
        pass
    @classproperty
    def morphisms(cls):
        pass

    def f_map(cls: Monad, function) --> Morphism:
        """
        Translates the function to working within the category.
        This is basically the decoration/wrapping process.
        The 'lazy-evaluated' version of function application.
        fmap::(a -> b) -> (m a -> m b)
        """
        pass

    def f_apply(cls: Category, function, object):
        """
        Applies the function, in the manner specified by the functor/monad.
        This is the simplest and best defined method in this whole constructor.
        FAPPLY SHOULD BE AUTHORITATIVE
        ... maybe I shoudl write it first
        fapply::(a -> b, a) -> m b
        """
        pass

    def a_map(cls: Category, morphism):

    def a_apply(cls: Category, morphism) -> Element:
        """
        ::(m (a -> b), m a) -> m b
        """

    def m_map(cls, constructor):
        """
        ::(a -> m b) -> (m a -> m b)
        """

    def m_apply(cls):
        """
        ::(a -> m b, m a) ->  m b
        """

    def zero(cls):
        """
        """

    def append(cls, element, element):
        """
        Could be composed two ways. Rigorously haskell:
        ::(m a, m a) -> m a
        Or intuitive:
        ::(m a, a) -> m a
        """
        pass

    def join(cls, element):
        """
        ::(m m a) -> (m a)
        """
        pass
