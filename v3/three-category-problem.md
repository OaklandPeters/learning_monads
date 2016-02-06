Three-Category Construction Problem
=====================================
How to map from the Monad.Category into the Codomain?

CONCLUSION FROM THE BOTTOM OF THE PAGE: The three-category construction basically requires it also be a comonad. Together, you get this Bimonad behavior. And this is not obvious


What we need are one or more of:

* collapse behavior
* f_map for Monad.Category : something that allows you to apply a transform on each element in the monad
* foldable : implied by __iter__ I think. Related to reducable
* traversable : this thing is the ability to apply an arbitary Applicative over it.

To work these out I really need 1 or 2 good examples of simple and concrete Three-Category Constructions (they can't be implemented yet of course). Underscore/_ is one.

Is it true that the f_map and a_map should still be usable? Since the Monad inherited from them, and in some-sense just represents a 'Frozen' version of the Functor application? Perhaps in this view, each 'f_map(domain_morphism)' represents a morphism in the Monad, and naturally any two morphisms in it can be composed. This *should* mean that fmap(domain_morphism) should be very close to bind/m_map
    f_map(domain_morphism) :: (a -> b) -> (f a  -> f b)
                             (D a -> D b) -> (C a -> C b)
    m_map(constructor) :: (a -> m b)   ->   m a   ->   m b
                          (D a -> M b) ->  (M a    ->  M b)

    m_lift :: a -> m a
             (D a -> M a)
    domain_morphsim . m_lift :: (D a -> D b) . (D b -> M b)
                            ==> (D a -> M b)
    f_map(domain_morphsim . m_lift) :: 
        ==> ((D a -> D b) -> (C a -> C b)) . (D a -> M b)
        Which we cannot do, since (D a -> M b) isn't a morphism in the domain (D a -> D b)

        Recall functor composition law:  fmap (f . g) == fmap f . fmap g
        ==> fmap(domain_morphism) . fmap(m_lift)
        ==> ((D a -> D b) -> (C a -> C b))  .  ()


    a_lift(domain_element) :: (D a -> C a)
    a_apply(codomain_morphism, domain_element) :: ((C a -> C b), D a) -> C b
        * NOTE: in three-category construction, this follows trivially from f_map + a_lift
        * What this really says is: fmap lets us use domain functions on the codomain --> Codomain.Element
          but aapply lets us use codomain functions on the domain --> Codomain.Element


In the end, I'm going to need functions with the signatures for:
* domain_element -> monad_element           :: m_lift
* domain_morphism -> monad_morphism
* mlift(domain_morphism) -> codomain_morphism
  monad_morphism -> codomain_morphism
* mlift(domain_element) -> codomain_element
  monad_element -> codomain_element


Insight: I need the 'missing' piece, to prove that I can 
(1) apply fmap/fapply/a_apply to the monad
(2) 'complete the translation' (seeing the monad as being frozen mid-translation), from the monad into the codomain


One Piece:
(D a -> D b) . mlift  ==  (D a -> M b)
So monad mlift implies the ability to turn any domain morphism into a constructor in the monad

If we require

fmap(D a -> D b)(C a)  ==  fmap((Da -> D b) . mlift)(C a)
    So lifting into the monad doesn't interfere with the function application


f_lift = f_map
f_map(D a -> D b)    ==     C a -> C b
(D a -> D b) . m_LIFTER . m_DROPPER  ==  C a -> C b








Comonad
    extract :: w a -> a
        M a -> C a
        Law:  extract . fmap f =  f . extract
    duplciate :: M a -> M M a
        ... I suspect this is comonoidal, and might not be needed
        Law: duplicate = extend id
        Law: fmap (fmap f) . duplicate = duplicate . fmap f
    extend :: (w a -> b) -> w a -> w b
        (M a -> C b) ->  (M a -> M b)
        Law: extend f = fmap f . duplicate
