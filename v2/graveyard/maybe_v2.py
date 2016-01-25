"""
Write this one only as 'first'



This version of Maybe is more closely paralleling Haskell.

I'd like not to have to ditch the old one, but maybe I should.

PART of my confusion is likely that Maybe is a simplified version of 'Either'

CONFUSION about this version....
    How do chain these things together?
    I suspect that Haskell's lazy function behavior handles this.
    (I think people were doing the equivalent of:
    Maybe(elm) >>= (
        Maybe(get(0)) >>= (
            Maybe(get(1)) >>= (
                . . .
            )
        )
    )

    This reinforces the intuition that the way to handle the First/Last chaining
    behavior is inside the 'append'

    So... updated structure

    Just, Nothing --> Elements: do not have a 'default'
    First, Last --> Morphisms: *do* have a default

    Which *seems* simple, but means that Elements are not a Monoid

    Related: this page shows that there are 3 (or 4) ways of making Maybe into a Monoid.
    And some of them seem hacky (such as defining the identity/zero element and then just not using it anywhere).


Monoidal structure in Haskell's applicative:
<|> ~ mappend
Nothing <|> p = p
Just x <|> _ = Just x

... so it doesn't use the 'default' behavior


"""
import category

class MaybeCategory(category.Category):

    @classmethod
    def f_apply(cls, element, function):
        if isinstance(element, Nothing):
            return Nothing()
        else:
            return Just(function(element.data))


    @classmethod
    def a_apply(cls, element, morphism):


    @classmethod
    def m_apply(cls, element, constructor):
        if isinstance(element, Nothing):
            return Nothing()
        else:
            return constructor(function(element.data))
            # I suspect this is equivalent to:
            # return element.f_apply(constructor).join()


    @classmethod
    def join(cls, element, reducer=take_last):
        pass



class MaybeElement:
    """
    Should be constructed via 'Maybe(x)'
    """
    def __init__(self, context):
        self.context = context

class MaybeMorphism(category.Morphism, Maybe):
    def __init__(self, function, reducer=take_first):
        self.data = function
        self.reducer = reducer

class Just(MaybeElement):
    def __init__(self, data, context):
        self.data = data
        self.context = context

class Nothing(MaybeElement):
    def __init__(self, context):
        self.context = context

