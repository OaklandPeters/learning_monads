REALIZATION OF PROBLEM:
        There is a schism in meaning between the methods on Applicative and Monad.
        If Applicative.a_apply return the Codomain
        And you build a Monad on top of that Applicative
        The Monad.a_apply should return the Codomain, but it feels like it should return the monadic domain.

        So there is a big problem:
            Building up Functor -> Applicative -> Monad incrementally.
