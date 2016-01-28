"""
Notes on the future deconstructor/extractor.
I suspect this is going to correspond to either/or:
(1) The core functions from Traversable
(2) The signature function(s) of Comonad
"""


def laws():
    """
    Trying to decide/determine which laws should be true
    about the deconstruction operator '<<'

    Note: because I suspect that '>>' should not be precisely 'bind'/'m_apply',
    neither do I want '<<' to be precisely 'unlift'.

    ... aside thought: am I just wanting to push the values into another category?
        Or am I wanting to revert the values into their original category?
        One issue: if there is more than one value, then they have to be wrapped in something (a Sequence or Iterable).

    def <<(cls: Comonad, element: Element, builder: Monoid):
        # split::M a -> (M a, M a)
        # Note: some version of split can take a function to use as a rule
        #     on how to split - just as some join() methods can
        
        accumulator = builder()  # or builder.zero()

        # this is trying to build the inverse of an iterator
        while (not isinstance(deccumulator, deccumulator.zero)):
            elm, deccumulator = decummulator.split()
            # somehow extract the 'value' from elm
            value = elm.SOME_METHOD()
            accumulator = accumulator.append(builder.lift(value))

        return accumulator
            

        element.split
    """

    def law_one(Monad, value):

        klass
        assert issubclass(klass, Iterable)
        value = klass.random()
        assert value == (Monad() >> value << klass)


