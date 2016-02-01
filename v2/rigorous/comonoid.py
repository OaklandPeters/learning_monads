"""
Notes on Comonoid/Comonad, and their symmetry with Monoid/Monad.
Found these at:
http://stackoverflow.com/questions/16551734/can-a-monad-be-a-comonad


class CoMonoid m where
  comempty :: (m,a) -> a
  comappend :: m -> (m,m)
--every haskell type is a CoMonoid
--that is because CCCs are boring!

instance Monoid a => Monad ((,) a) where
  return x = (mempty,x)
  join (a,(b,x)) = (a <> b, x)
instance CoMonoid a => CoMonad ((,) a) where
  coreturn = comempty
  cojoin = associate . first comappend

instance CoMonoid a => Monad ((->) a) where
  return = flip (curry comempty)
  join f = uncurry f . comappend
instance Monoid a => CoMonad ((->) a)  where
  coreturn f = f mempty
  cojoin f a b = f (a <> b)
"""


"""
[[STUDY THIS - I HAVENT READ THROUGH YET]]
The Cofree Comonad yields some data structures that are useful as Monads and Comonads both:

data Cofree f a = a :< f (Cofree f a)
Every Cofree Comonad over an Alternative functor yields a Monad -- see the instance here:

http://hackage.haskell.org/packages/archive/free/3.4.1/doc/html/Control-Comonad-Cofree.html

instance Alternative f => Monad (Cofree f) where
  return x = x :< empty
  (a :< m) >>= k = case k a of
                     b :< n -> b :< (n <|> fmap (>>= k) m)
This gives us, e.g. nonempty lists as Monads and Comonads both (along with nonempty f-branching trees, etc).

Identity is not an alternative, but Cofree Identity yields an infinite stream, and we can in fact give a different monad instance to that stream:

http://hackage.haskell.org/packages/archive/streams/3.1/doc/html/Data-Stream-Infinite.html

data Stream a = a :> Stream a
instance Comonad Stream where
  duplicate = tails
  extend f w = f w :> extend f (tail w)
  extract = head

instance Monad Stream where
  return = repeat
  m >>= f = unfold (\(bs :> bss) -> (head bs, tail <$> bss)) (fmap f m)
(note the functions above are not on lists but instead defined in the streams package).

Similarly the reader arrow is not an alternative, but Cofree ((->) r) yields a Moore machine, and Moore machines also are monads and comonads both:

http://hackage.haskell.org/packages/archive/machines/0.2.3.1/doc/html/Data-Machine-Moore.html

data Moore a b = Moore b (a -> Moore a b)
instance Monad (Moore a) where
  return a = r where r = Moore a (const r)
  Moore a k >>= f = case f a of
    Moore b _ -> Moore b (k >=> f)
  _ >> m = m
instance Comonad (Moore a) where
  extract (Moore b _) = b
  extend f w@(Moore _ g) = Moore (f w) (extend f . g)
So what's the intuition behind all these examples? Well we get the comonadic operations for free. The monadic operations we get are all forms of diagonalization. With alternative we can <|> things together to "smush" the structure, and magic up "empty" things when we run out of structure to smush. This lets us work on finite cases. Lacking alternative we need to have an indefinite amount of structure, so that no matter how many "join" operations (which we can think of as splicing or substitution) that we make, there's always more room to place the spliced elements (like at the Hilbert Hotel: http://www.encyclopediaofmath.org/index.php/Hilbert_infinite_hotel).

Relatedly, every Comonad gives rise to a related Monad (although I consider this more a curiousity):

http://hackage.haskell.org/packages/archive/kan-extensions/3.1.1/doc/html/Control-Monad-Co.html

http://comonad.com/reader/2011/monads-from-comonads/

>   "Every Cofree Comonad over an Alternative Functor yields a Monad" - This is worthy of the same level of fame as "monad is just a monoid of endofunctors"! :-D
"""

"""
There are many interesting structures that are both a Monad and a Comonad.

The Identity functor has been pointed out here by several other people, but there are non-trivial examples.

The Writer Monad plays a Reader-like role as a Comonad.

instance Monoid e => Monad ((,) e)
instance Comonad ((,) e)
The Reader Monad plays a Writer-like role as a Comonad.

instance Monad ((->) e)
instance Monoid e => Comonad ((->)e)
Non-empty lists also form both a monad and a comonad and are in fact a special case of a larger construction involving cofree comonads. The Identity case can also be seen as a special case of this.

There are also various Yoneda and Codensity-like constructions based on Kan extensions, that work to transform monads and comonads, although they favor one or the other in terms of operational efficiency.

I also have an adapter that converts an arbitrary comonad into a monad transformer. Sadly the opposite conversion isn't possible in Haskell.

In linear algebra there is a notion of a bialgebra. Ideally if we have something that forms both a Monad and a Comonad and we want to use those operations together without reasoning on a case-by-case basis, one would like to have that return and join are Comonad coalgebras and by extension that extract and duplicate are Monad algebras. If those conditions hold then you can actually reason about code that has both Monad f and Comonad f constraints and mixes the combinators from each without case-by-case reasoning.
"""
