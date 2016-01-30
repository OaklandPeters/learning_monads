"""
These are notes on the Haskell typeclass hierarchy.
The reason is that I don't want to recreate 'Monad' *exactly*
I really want something more like MonadPlus and/or MonadFix
Frequently, I also want the behavior of Traversable.

BUT... these don't translate directly.
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

    @classmethod
    def mfix(cls, constructor) -> Element:
    """mfix :: (a -> m a) -> m a

    The fixed point of a monadic computation. mfix f executes the action f only once, with the eventual output fed back as the input. Hence f should not be strict, for then mfix f would diverge.
    """
