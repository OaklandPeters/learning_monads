"""
These are notes on the Haskell typeclass hierarchy.
The reason is that I don't want to recreate 'Monad' *exactly*
I really want something more like MonadPlus and/or MonadFix
Frequently, I also want the behavior of Traversable.

BUT... these don't translate directly.

INSIGHT: a *lot* of the 'Foldable' methods correspond well to Pythonic behavior.
    elem --> __contains__, length --> Sized, null --> __bool__

    But note: I'd really like to disambuate __Bool__ VS empty behavior.
"""


class Semigroupoid:
    """
    A Semigroupoid is a Category without the requirement of identity arrows for every object in the category.

    Basically, a close relative of Semigroup.

    PERSONAL NOTE: I'm using Identified/Semigroupoid/Category for functions, and Zeroable/SemiGroup/Monoid for data-structures.
    """
    @classmethod
    def composition(cls, morphism_a_b, morphism_b_c):
        """(.) :: cat b c -> cat a b -> cat a c

        morphism composition
        """


class Category(SemiGroupoid):
    """A class for categories. id and (.) must form a monoid.
    TL:DR; Basis for function composition, and determination of type correctness (since types are fundamentally about composition).
        Also... Categories are intimately related to type coersions and notions of equality. However, I do not understand how.

    https://en.wikibooks.org/wiki/Haskell/Category_theory


    There are three category laws, but I can't find the text for a summation fo them.

    Associative (of morphisms)
    
        f . (g . h) == (f . g) . h


    Closed (composition of morphisms)
        Any two morphisms within the category can be composed, and the result is also a morphism in the category.

        for any f::A -> B, g::B -> C
        there exists h::A -> C
            
            f . g = h

    Identity
        For every morphism, g: A -> B
         g . identity(B) == identity(A) . g == g


    PERSONAL THOUGHT: 'collapse' is a function of my own thought, which plays a similar role to 'join' from Monoid. (actually, Category could be thought of as a type of Monoid, but we are leaving hte distinction)

    PERSONAL THOUGHT: I think 'join' might be derivable for any Monoid with zero/append (and the ability to distinguish element of the type).

    """
    @classmethod
    def identity(cls, element):
        """id :: cat a a
        the identity morphism
        """

    @classmethod
    def composition(cls, morphism_a_b, morphism_b_c):
        """(.) :: cat b c -> cat a b -> cat a c

        morphism composition
        """

    @classmethod
    def this_fucking_thing():
        """(>>>) :: Category cat => cat a b -> cat b c -> cat a c
        Left-to-right composition
        https://hackage.haskell.org/package/base-4.8.2.0/docs/Control-Category.html

        NOTE: I have no idea in what way it is different than '.' composition
        """


class Arrow:
    """
    A generalization of Monads
    Unlike monads, arrows don't limit steps to having one and only one input. 

    https://en.wikibooks.org/wiki/Haskell/Understanding_arrows

    Like all type classes, arrows can be thought of as a set of qualities that can be applied to any data type. In the Haskell programming language, arrows allow functions (represented in Haskell by an arrow symbol) to combine in a reified form. However, the actual term "arrow" may also come from the fact that some (but not all) arrows correspond to the morphisms (also known as "arrows" in category theory) of different Kleisli categories. As a relatively new concept, there is not a single, standard definition, but all formulations are logically equivalent, feature some required methods, and strictly obey certain mathematical laws.[6]

    The description currently used by the Haskell standard libraries requires only two basic operations:

    A type constructor 'arr' that takes functions -> from any type s to another t, and lifts those functions into an arrow A between the two types.[7]
    
        arr (s -> t)        ->   A s t

    A piping method first that takes an arrow between two types and converts it into an arrow between tuples. The first elements in the tuples represent the portion of the input and output that is altered, while the second elements are a third type u describing an unaltered portion that bypasses the computation.[7]
    
        first (A s t)       ->   A (s,u) (t,u)
    
    Although only these two procedures are strictly necessary to define an arrow, other methods can be derived to make arrows easier to work with in practice and theory. As all arrows are categories, they can inherit a third operation from the class of categories:

    A composition operator >>> that can attach a second arrow to a first as long as the first function's output and the second's input have matching types.[7]
    
        A s t  >>>  A t u   ->   A s u
    
    One more helpful method can be derived from a combination of the previous three:

    A merging operator *** that can take two arrows, possibly with different input and output types, and fuse them into one arrow between two compound types. Note that the merge operator is not necessarily commutative.[7]
    
        A s t  ***  A u v   ->   A (s,u) (t,v)
        Arrow laws[edit]
        In addition to having some well-defined procedures, arrows must obey certain rules for any types they may be applied to:

    
    Arrow Laws:

    Arrows must always preserve all types' identities id (essentially the definitions of all values for all types within a category).[7]

        arr id              ==   id

    When connecting two functions f & g, the required arrow operations must distribute over compositions from the left.[7]

        arr (f >>> g)       ==   arr f  >>>  arr g
        first (f >>> g)     ==   first f  >>>  first g

    In the previous laws, piping can be applied directly to functions because order must be irrelevant when piping & lifting occur together.[7]

        arr (first f)       ==   first (arr f)

    The remaining laws restrict how the piping method behaves when the order of a composition is reversed, also allowing for simplifying expressions:

    If an identity is merged with a second function to form an arrow, attaching it to a piped function must be commutative.[7]
    
        arr (id *** g)  >>>  first f       ==   first f  >>>  arr (id *** g)
    
    Piping a function before type simplification must be equivalent to simplifying type before connecting to the unpiped function.[7]
    
        first f  >>>  arr ((s,t) -> s)     ==   arr ((s,t) -> s)  >>>  f
    
    Finally, piping a function twice before reassociating the resulting tuple, which is nested, should be the same as reassociating the nested tuple before attaching a single bypass of the function. In other words, stacked bypasses can be flattened by first bundling together those elements unchanged by the function.[7]
    
        first (first f)  >>>  arr ( ((s,t),u) -> (s,(t,u)) )   ==
          arr ( ((s,t),u) -> (s,(t,u)) )  >>>  first f




    
    
    
    """
    @abstractmethod
    @classmethod
    def arr(cls, function):
        """Turns a function into an arrow."""

    @abstractmethod
    @classmethod
    def arrow_compose(cls, ):
        """(>>>) :: (Arrow a) => a b c -> a c d -> a b d
        Arrow composition is achieved with (>>>). This takes two arrows and chains them together, one after another. It is also arrow- specific. Its signature is:
        """

    @classmethod
    def first(cls, arrow, left, right):
        """first  :: y a b -> y (a, c) (b, c)          -- maps over first component"""

    @classmethod
    def second(cls, arrow, left, right):
        """second :: y a b -> y (c, a) (c, b)          -- maps over second component"""

    @classmethod
    def combine(cls, arrow):
        """(***) :: a b c -> a b' c' -> a (b, b') (c, c')

        Split the input between the two argument arrows and combine their output. Note that this is in general not a functor.

        Can be written as this, which is in some sense, the first and second combined.
        (***)  :: y a c -> y b d -> y (a, b) (c, d) -- first and second combined
        """

    @classmethod
    def branch(cls, arrow, left, right):
        """(&&&) :: a b c -> a b c' -> a b (c, c')

        Fanout: send the input to both argument arrows and combine their output.

        (&&&)  :: y a b -> y a c -> y a (b, c)      -- (***) on a duplicated value
        """

    #
    #   Monoid related methods
    #       Gives rise to 'ArrowPlus' which is similar to MonadPlus
    #
    @classmethod
    def zero(cls):
        """zeroArrow :: a b c"""

    @classmethod
    def append(cls, ):
        """(<+>) :: a b c -> a b c -> a b c infixr 5 Source

        An associative operation with identity zeroArrow.
        """





class Semigroup:
    """
    Assoicative binary operation (~append or 'plus'), but not necessarily a zero.
    """
    @classmethod
    def append(cls, left, right):
        pass


class Zeroable:
    """
    This doens't exist explicitly in Haskell.
    Means it has a zero/identity element.
    """
    @classmethod
    def zero(cls):
        pass


class Monoid(Semigroup, Zeroable):
    """
    The reason? You can iteratively build up any Monoid.

    Haskell's Monoid doesn't seem to include 'join'. I don't know why, nor where I got the idea to include 'join' in monoid.
    INSIGHT: You can derive join for anything with zero + append + ability to typecheck or dispatch on the type.
        ... actually, it has to be Foldable
    """



class Foldable(Monoid):
    """
    A foldable container is a container with the added property that its items can be 'folded' to a summary value.

    In other words, it is a type which supports "foldr". Once you support foldr, of course, it can be turned into a list, by using toList = foldr (:) []. This means that all Foldables have a representation as a list, but the order of the items may or may not have any particular significance. 

    However, if a Foldable is also a Functor, parametricity and the Functor law guarantee that toList and fmap commute. Further, in the case of Data.Sequence, there is a well defined order and it is exposed as expected by toList. A particular kind of fold well-used by Haskell programmers is mapM_, which is a kind of fold over (>>), and Foldable provides this along with the related sequence_.

    For example, given a data type

        data Tree a = Empty | Leaf a | Node (Tree a) a (Tree a)
    
    a suitable instance would be

        instance Foldable Tree where
           foldMap f Empty = mempty
           foldMap f (Leaf x) = f x
           foldMap f (Node l k r) = foldMap f l `mappend` f k `mappend` foldMap f r

    This is suitable even for abstract types, as the monoid is assumed to satisfy the monoid laws. Alternatively, one could define foldr:

        instance Foldable Tree where
           foldr f z Empty = z
           foldr f z (Leaf x) = f x z
           foldr f z (Node l k r) = foldr f (f k (foldr f z r)) l

    Foldable instances are expected to satisfy the following laws:

        foldr f z t = appEndo (foldMap (Endo . f) t ) z
        foldl f z t = appEndo (getDual (foldMap (Dual . Endo . flip f) t)) z
        fold = foldMap id

    sum, product, maximum, and minimum should all be essentially equivalent to foldMap forms, such as

        sum = getSum . foldMap Sum

    but may be less defined.

    If the type is also a Functor instance, it should satisfy

        foldMap f = fold . fmap f
    
    which implies that

        foldMap f . fmap g = foldMap (f . g)


    REQUIRES: defining either 'fold' or 'foldMap'
    """
    @classmethod
    @abstractmethod
    def fold():
        """fold :: Monoid m => t m -> m Source

        Combine the elements of a structure using a monoid.
        """

    @classmethod
    @abstractmethod
    def foldMap():
        """foldMap :: Monoid m => (a -> m) -> t a -> m Source

        Map each element of the structure to a monoid, and combine the results.
        """

    #
    #  Derivable
    @classmethod
    def foldl():
        """foldl :: (b -> a -> b) -> b -> t a -> b Source

        Left-associative fold of a structure.
            foldl f z = foldl f z . toList
        """

    @classmethod
    def foldr1(cls):
        """foldr1 :: (a -> a -> a) -> t a -> a Source

        A variant of foldr that has no base case, and thus may only be applied to non-empty structures.
            foldr1 f = foldr1 f . toList

        NOTE TO SELF: Any Monoid or Zeroable doesn't need this, since 'fold' can be applied on empty structures.
        """

    @classmethod
    def toList(cls):
        """toList :: t a -> [a]
        List of elements of a structure, from left to right.
        """

    @classmethod
    def null(cls):
        """null :: t a -> Bool Source

        Test whether the structure is empty. The default implementation is optimized for structures that are similar to cons-lists, because there is no general way to do better.
        """

    @classmethod
    def length(cls):
        """length :: t a -> Int Source

        Returns the size/length of a finite structure as an Int. The default implementation is optimized for structures that are similar to cons-lists, because there is no general way to do better.
        """

    @classmethod
    def elem(cls):
        """elem :: Eq a => a -> t a -> Bool infix 4 Source

        Does the element occur in the structure?
        """


class Joinable(Foldable):
    """
    This is a class I'm writing as a placeholder. I don't know exactly what it's equivalent in Haskell is. I want it to be a Monoid that is garunteed to support 'join'.

    This requires:
        zero, append, for, lift

    This looks to me like a combination of Applicative, Monoid, and Foldable
    """
    @classmethod
    def join(cls, element):
        accumulator = cls.zero():
        for value in cls.for(element):
            if isinstance(value, cls):
                accumulator = accumulator.append(value)
            else:
                accumulator = accumulator.append(cls.lift(value))
        return accumulator



class Traversable(Functor, Foldable):
    """
    https://en.wikibooks.org/wiki/Haskell/Traversable
    A Traversable type is a kind of upgraded Foldable. Where Foldable gives you the ability to go through the structure processing the elements (foldr) but throwing away the shape, Traversable allows you to do that whilst preserving the shape and, e.g., putting new values in. Traversable is what we need for mapM and sequence : note the apparently surprising fact that the "_" versions are in a different typeclass.

    Functors representing data structures that can be traversed from left to right.

    A definition of traverse must satisfy the following laws:

    naturality
        t . traverse f = traverse (t . f) for every applicative transformation t
    
    identity
        traverse Identity = Identity
    
    composition
        traverse (Compose . fmap g . f) = Compose . fmap (traverse g) . traverse f
    

    A definition of sequenceA must satisfy the following laws:

    naturality
        t . sequenceA = sequenceA . fmap t for every applicative transformation t
    
    identity
        sequenceA . fmap Identity = Identity
    
    composition
        sequenceA . fmap Compose = Compose . fmap sequenceA . sequenceA
    
    where an applicative transformation is a function

        t :: (Applicative f, Applicative g) => f a -> g a

    preserving the Applicative operations, i.e.

        t (pure x) = pure x
        t (x <*> y) = t x <*> t y

    and the identity functor Identity and composition of functors Compose are defined as:

      newtype Identity a = Identity a

      instance Functor Identity where
        fmap f (Identity x) = Identity (f x)

      instance Applicative Indentity where
        pure x = Identity x
        Identity f <*> Identity x = Identity (f x)

      newtype Compose f g a = Compose (f (g a))

      instance (Functor f, Functor g) => Functor (Compose f g) where
        fmap f (Compose x) = Compose (fmap (fmap f) x)

      instance (Applicative f, Applicative g) => Applicative (Compose f g) where
        pure x = Compose (pure (pure x))
        Compose f <*> Compose x = Compose ((<*>) <$> f <*> x)

      (The naturality law is implied by parametricity.)

    
    Instances are similar to Functor, e.g. given a data type:

        data Tree a = Empty | Leaf a | Node (Tree a) a (Tree a)
    
    a suitable instance would be:

        instance Traversable Tree where
           traverse f Empty = pure Empty
           traverse f (Leaf x) = Leaf <$> f x
           traverse f (Node l k r) = Node <$> traverse f l <*> f k <*> traverse f r

    This is suitable even for abstract types, as the laws for <*> imply a form of associativity.

    The superclass instances should satisfy the following:

        In the Functor instance, fmap should be equivalent to traversal with the identity applicative functor (fmapDefault).

        In the Foldable instance, foldMap should be equivalent to traversal with a constant applicative functor (foldMapDefault).


    NOTE: Traversable can be defined from 'traverse' OR from 'SequenceA'

    """

    @classmethod
    @abstractmethod
    def traverse(cls, functor: Applicative, data: Traversable) -> ???:
        """
        traverse :: (Applicative f, Traversable t) => (a -> f b) -> t a -> f (t b)

        ... resembles that of mapping functions we have seen in other classes. Rather than using its function argument to insert functorial contexts under the original structure (as might be done with fmap) or to modify the structure itself (as (>>=) does), traverse adds an extra layer of context on the top of the structure. Said in another way, traverse allows for effectful traversals − traversals which produce an overall effect (i.e. the new outer layer of context).

        If the structure below the new layer is recoverable at all, it will match the original structure (the values might have changed, of course). Here is an example involving nested lists:

        GHCi> traverse (\x -> [0..x]) [0..3]
        [[0,0,0,0],[0,0,0,1],[0,0,0,2],[0,0,0,3],[0,0,1,0],[0,0,1,1]
        ,[0,0,1,2],[0,0,1,3],[0,0,2,0],[0,0,2,1],[0,0,2,2],[0,0,2,3]
        ,[0,1,0,0],[0,1,0,1],[0,1,0,2],[0,1,0,3],[0,1,1,0],[0,1,1,1]
        ,[0,1,1,2],[0,1,1,3],[0,1,2,0],[0,1,2,1],[0,1,2,2],[0,1,2,3]
        ]
        The inner lists retain the structure the original list − all of them have four elements. The outer list is the new layer, corresponding to the introduction of nondeterminism through allowing each element to vary from zero to its (original) value.
        """

    @classmethod
    @abstractmethod
    def sequenceA(cls, structure: Traversable[Applicative]) -> Traversable[Applicative]:
        """sequenceA :: Applicative f => t (f a) -> f (t a)

        Evaluate each action in the structure from left to right, and and collect the results. For a version that ignores the results see sequenceA_.

        GHCi> sequenceA [[1,2,3,4],[5,6,7]]
        [[1,5],[1,6],[1,7],[2,5],[2,6],[2,7]
        ,[3,5],[3,6],[3,7],[4,5],[4,6],[4,7]
        ]
        In this example, sequenceA can be seen distributing the old outer structure into the new outer structure, and so the new inner lists have two elements, just like the old outer list. The new outer structure is a list of twelve elements, which is exactly what you would expect from combining with (<*>) one list of four elements with another of three elements. One interesting aspect of the distribution perspective is how it helps making sense of why certain functors cannot possibly have instances of Traversable (how would one distribute an IO action? Or a function?).
        """

    # 
    # Derivable
    # 
    @classmethod
    def mapM(cls, ):
        """mapM :: Monad m => (a -> m b) -> t a -> m (t b) Source

        Map each element of a structure to a monadic action, evaluate these actions from left to right, and collect the results. For a version that ignores the results see mapM_.
        """

    @classmethod
    def sequence(cls, ):
        """sequence :: Monad m => t (m a) -> m (t a) Source

        Evaluate each monadic action in the structure from left to right, and collect the results. For a version that ignores the results see sequence_.
        """

    # Utility functions
    @classmethod
    def for(cls, t: Traversable[T], f: Applicative) -> Applicative[Traversable]:
        """for :: (Traversable t, Applicative f) => t a -> (a -> f b) -> f (t b) Source
        
        for is traverse with its arguments flipped. For a version that ignores the results see for_.

        NOTE: a version of this exists for monads. I have no idea why it needs to be distinct.
            forM is mapM with it's arguments flipped.
        forM :: (Traversable t, Monad m) => t a -> (a -> m b) -> m (t b)        
        """

    @classmethod
    def mapAccumL():
        """mapAccumL :: Traversable t => (a -> b -> (a, c)) -> a -> t b -> (a, t c) Source

        The mapAccumL function behaves like a combination of fmap and foldl; it applies a function to each element of a structure, passing an accumulating parameter from left to right, and returning a final value of this accumulator together with the new structure.
        """


class HardCases:
    """TLDR: 'filter' and 'concatMap' (insertion) are not implied by Traversable or Foldable
    But they are related to Applicative/Monad (but not exactly).

    2 Some trickier functions: concatMap and filter
    Neither Traversable nor Foldable contain elements for concatMap and filter. That is because Foldable is about tearing down the structure completely, while Traversable is about preserving the structure exactly as-is. On the other hand concatMap tries to 'squeeze more elements in' at a place and filter tries to cut them out. You can write concatMap for Sequence as follows:
        concatMap :: (a -> Seq b) -> Seq a -> Seq b
        concatMap = foldMap

    But why does it work? It works because sequence is an instance of Monoid, where the monoidal operation is "appending". The same definition works for lists, and we can write it more generally as:
        concatMap :: (Foldable f, Monoid (f b)) => (a -> f b) -> f a -> f b
        concatMap = foldMap

    And that works with lists and sequences both. Does it work with any Monoid which is Foldable? Only if the Monoid 'means the right thing'. If you have toList (f `mappend` g) = toList f ++ toList g then it definitely makes sense. In fact this easy to write condition is stronger than needed; it would be good enough if they were permutations of each other. filter turns out to be slightly harder still. You need something like 'singleton' (from Sequence), or \a -> [a] for lists. We can use pure from Applicative, although it's not really right to bring Applicative in for this, and get:
        filter :: (Applicative f, Foldable f, Monoid (f a)) => 
                  (a -> Bool) -> f a -> f a
        filter p = foldMap (\a -> if p a then pure a else mempty)

    It's interesting to note that, under these conditions, we have a candidate to help us turn the Foldable into a Monad, since concatMap is a good definition for >>=, and we can use pure for return.
    """


class Functor:
    """
    Unlike some other type classes we will encounter, a given type has at most one valid instance of Functor. This can be proven via the free theorem for the type of fmap. In fact, GHC can automatically derive Functor instances for many data types.

    Functor laws:
        Any sensible Functor instance, however, will also satisfy the functor laws, which are part of the definition of a mathematical functor. There are two:

    fmap id = id
    fmap (g . h) = (fmap g) . (fmap h)


    PERSONAL: I'm not sure if this is true in a strict and imperative language like Python. For example, on a tree, depth-first and breadth-first could be different Functors.
        INSIGHT: It (kinda) is true, but only between any two given categories. In Haskell, one of those categories is fixed. But for me... I don't necessarily want to assume the categories are always the same. So Functor could be between any two categories (types), and every pair of categories has their own functor.
    


    LESSON: fmap has to apply the funciton uniformly to all elements in the data structure. non-uniform data-structure *probably* don't have a meaningful Functor defined on them.
    
    INSIGHT: The above is concerned with homogenous mapping. A different view, is the more category-theoretic one, which sees a Functor as being responsible for mapping Element and Morphism into a new category. (the 'context' that people talk about for Functors in Haskell, is really the other category the Functor maps into)

    CHALLENGE: Proving or checking that a Functor maps Identity functions to Identity functions in a different category can be... hard. One aid would be to have a distinguished Identity morphism object in each category. Another approach, is to use a container to hold morphisms, and when it is empty, then execute the identity.
    """
    @classmethod
    def f_apply(cls, element, function):
        """
        For emphasis, we can write fmap’s type with extra parentheses: fmap :: (a -> b) -> (f a -> f b). Written in this form, it is apparent that fmap transforms a “normal” function (g :: a -> b) into one which operates over containers/contexts (fmap g :: f a -> f b). This transformation is often referred to as a lift; fmap “lifts” a function from the “normal world” into the “f world”.

        PERSONAL: This implies that 'lift' is aleady latent in Functor. 'lift' raises a morphism in the domain into a morphism in the codomain. In this context, we could just rename f_map --> lift.

        QUESTION: Does 'lift' need to be able to handle elements? No... that's the domain of Applicative's lift
        """

    @classmethod
    def f_map(cls, function):
        """
        Basic maps or decorates the function.
        Turns morphism in the domain into a morphism in the codomain.
        """

class Applicative:
    """


    PERSONAL: A key insight - the signature of a_apply looks very much like that of the 'apply' function in a category, just with everything wrapped in a context.
        apply   :: ((a -> b), a)     -> b
        a_apply :: (f (a -> b), f a) -> f b

    """
    @classmethod
    def lift(cls, value):
        """pure  :: a -> f a
        """
    @classmethod
    def a_apply(cls, element, morphism) -> Element:
        """
        (<*>) :: f (a -> b) -> f a -> f b
        """




class MonadFix(Monad):
    """
    The MonadFix typeclass provides the mfix method for value recursion. It can be used directly, or indirectly through the “recursive do” syntax extension (language extension RecursiveDo). It is useful for building cyclic data in monadic code.

    Here are the laws of MonadFix and some implications.

    (1) purity:
        mfix (return . h) = return (fix h)
        
        mfix over pure things is the same as pure recursion. mfix does not add any monadic action of its own.

    (2) left shrinking: (or tightening)
        mfix (\x -> a >>= \y -> f x y) = a >>= \y -> mfix (\x -> f x y)
        
        A monadic action on the left (at the beginning) that does not involve the recursed value (here x) can be factored out of mfix. So mfix does not change the number of times the action is performed, since putting it inside or outside makes no difference.

    (3) sliding:
        if h is strict, mfix (liftM h . f) = liftM h (mfix (f . h))

    (4) nesting:
        mfix (\x -> mfix (\y -> f x y)) = mfix (\x -> f x x)
        these two laws are analogous to those of pure recursion, i.e., laws of fix.
    """
    @abstractmethod
    @classmethod
    def mfix(cls, constructor) -> Element:
        """mfix :: (a -> m a) -> m a

        The fixed point of a monadic computation. mfix f executes the action f only once, with the eventual output fed back as the input. Hence f should not be strict, for then mfix f would diverge.
        """


class MondPlus(Monad):
    """
    The MonadPlus class is defined like this:

    class (Monad m) => MonadPlus m where
       mzero :: m a
       mplus :: m a -> m a -> m a
    The precise set of rules that MonadPlus should obey is not agreed upon.

    Monoid — mplus and mzero form a monoid:
        mplus mzero a = a
        mplus a mzero = a
        mplus (mplus a b) c = mplus a (mplus b c)

    Left Zero — mzero is a left zero for >>=:
        mzero >>= k = mzero

    Left Distribution:
        mplus a b >>= k = mplus (a >>= k) (b >>= k)

    Left Catch — this is rarely advocated, but Maybe and IO satisfy this as an alternative to Left Distribution.
        mplus (return a) b = return a
    
    1 Which satisfies what?
        [] satisfies Monoid, Left Zero, and Left Distribution. Maybe, IO and STM satisfy Monoid, Left Zero, and Left Catch.
    
    2 Which rules?
        Martin & Gibbons choose Monoid, Left Zero, and Left Distribution. This makes [] a MonadPlus, but not Maybe or IO.

    3 What should be done?
    It is proposed that the class be separated into MonadZero, MonadPlus, MonadOr.


    PERSONAL NOTE: I prefer just defining this as: MonadPlus(Monad, Monoid)
    """



