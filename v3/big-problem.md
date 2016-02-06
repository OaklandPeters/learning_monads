REALIZATION OF PROBLEM:
        There is a schism in meaning between the methods on Applicative and Monad.
        If Applicative.a_apply return the Codomain
        And you build a Monad on top of that Applicative
        The Monad.a_apply should return the Codomain, but it feels like it should return the monadic domain.

        So there is a big problem:
            Building up Functor -> Applicative -> Monad incrementally.

SOLUTION:

Monad having a .Category,
and making Applicative.a_lift and Monad.m_lift, which might be
different).

Two ways to construct monad:

Two-Category Version
----------------------
Monad.Category => Monad.Codomain. This is the version used most often in Haskell (maybe always... as far as I know).
Monad.return/lift/pure is the same as Applicative.lift/pure

Three-Category Version
------------------------
Monad.Category is different than the Monad.Codomain, and Monad.lift is different than Applicative.lift.

This version makes more sense in Python, and it corresponds to several monads I've tried to write. Such as the _ monad, and basically any monad which does the behavior of 'expand AST, then collapse to data'.

However, this requires writing three Categories (although the Domain and Codomain might be easy to write).

This suggests a reorganization is in order. Functor, Applicative, AND Monad should each define different versions of:

_map
_apply
_lift

f_lift : Domain.Morphism -> Codomain.Morphism
a_lift : Domain.Element -> Codomain.Element
m_lift : Domain.Morphism -> Monad.Category.Morphism
   AND   Domain.Element  -> Monad.Category.Element

Problems and Complications with the Three-Category Construction:
-------------------------------------------------------------------

(1) This leaves an important question: how to have Monad.Category track the distinction of Element and Morphism.
Maybe:
me_lift :
mm_lift :

Alternately, I can NOT explicitly define lifting functions, and just rely on the __new__ functions of those respective objects. .... actually no. This is a bad idea for two reasons:
* Some categories might not correspond to instanciatible classes
* I'd like to do dispatching in some __new__ / have polymorphic __new__ functions. _lift should be simple: taking exactly one argument of the type from the Codomain.

(2) Getting data OUT of the Monad. How? m_map and m_apply (and likely composition and monoid operators in the Monad category) continue to return objects in the monad, so there is the concern of how to map from the Monad.Category to the Codomain. Solution: f_apply and a_apply both STILL map into the codomain.

WAIT... NO. f_apply and a_apply map *from* the Domain, so it's not at all clear that they should be usable on the Monad.Category. What we need are one or more of:

* collapse behavior
* f_map for Monad.Category : something that allows you to apply a transform on each element in the monad
* foldable : implied by __iter__ I think. Related to reducable
* traversable : this thing is the ability to apply an arbitary Applicative over it.

See 'three-category-problem.md' for discussion on avenues of this.
        


(3) Non-chainability of .a_apply and .f_apply. These both map Domain -> Codomain, so they cannot placed end to end.

! Happy insight: because of problem (3) (non-chainability of f_apply and a_apply), it takes the Monad class to give chaining behavior. *Which is what we know should be required mathematically.*
