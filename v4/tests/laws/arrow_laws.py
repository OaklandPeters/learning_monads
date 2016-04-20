from abc import abstractproperty
import unittest


class ArrowTestSupportMixin:
    """
    Supporing functions for ArrowLawTests moved here, for clarity.
    """

    arrow = abstractproperty(lambda self: NotImplemented)
    values = abstractproperty(lambda self: NotImplemented)
    category = abstractproperty(lambda self: NotImplemented)
    morphisms = abstractproperty(lambda self: NotImplemented)
    
    @abstractproperty
    def morphisms(self):
        """
        Morphisms should already be in the basic arrow category - Psyk.
        """
        return NotImplemented
    @abstractproperty
    def composable_morphisms(self):
        """Returns two morphisms: left, right, which we know can compose
        correctly.
        """
        return NotImplemented


    def assert_function_equality(self, left, right):
        """
        To the best of our ability, confirms that functions are the same; by
        testing whether they produce the same output.
        """
        for value in self.values:
            self.assertEqual(left(value), right(value))


def assoc(pair, c):
    a, b = *pair
    return a, tuple(b, c)


class ArrowLawTests(ArrowTestSupportMixin):
    """
    To make use of this, inherit from unittest.TestCase, and this,
    while overriding the abstracts from ArrowTestSupportMixin
    """

    def test_conservation_of_identity(self):
        """
        First Law: arr id = id
        """
        self.assert_function_equality(
            self.arrow.arr(identity), identity
        )

    def test_distributivity_of_composition(self):
        """
        Second Law: arr (f >>> g) = arr f >>> arr g
        Note: this requires f, g to already be in some arrow (Pysk ?).
        """
        self.assert_function_equality(
            self.arrow.arr(f >>> g),
            self.arrow.arr(f) >>> self.arrow.arr(g)
        )

    def test_commutativity_of_first_and_arr(self):
        """
        Third Law: first (arr f) = arr (first f)
        """
        # Suspect this assumes f is already in a different arrow
        self.assert_function_equality(
            self.arrow.first(self.arrow.arr(f)),
            self.arrow.arr(self.arrow.first(f))
        )

    def test_distributivity_of_composition_over_first(self):
        """
        Fourth law: first (f >>> g) = first f >>> first g
        """
        self.assert_function_equality(
            self.arrow.first(self.arrow.compose(f, g)),
            self.arrow.compose(
                self.arrow.first(f),
                self.arrow.first(g)
            )
        )

    def test_(self):
        """
        Fifth law: first f >>> arr fst = arr fst >>> f
        
        ... no idea what fst is 
        """
        self.assert_function_equality(
            self.arrow.compose(
                self.arrow.first(f),
                self.arrow.arr(fst)
            ),
            self.arrow.compose(
                self.arrow.arr(fst),
                f
            )
        )

    def test_(self):
        """
        Sixth Law: first f >>> arr (id *** g) = arr (id *** g) >>> first f
        """
        self.assert_function_equality(
            self.arrow.compose(
                self.arrow.first(f),
                self.arrow.arr(
                    self.arrow.split(
                        self.arrow.identity,
                        g
                    )
                )
            ),
            self.arrow.compose(
                self.arrow.arr(
                    self.arrow.split(
                        self.arrow.identity,
                        g
                    )
                ),
                self.arrow.first(f)
            )
        )

    def test_(self):
        """
        Seventh Law: first (first f) >>> arr assoc = arr assoc >>> first f
        """
        self.assert_function_equality(
            self.arrow.compose(
                self.arrow.first(self.arrow.first(f)),
                self.arrow.arr(assoc)
            ),
            self.arrow.compose(
                self.arrow.arr(assoc),
                self.arrow.first(f)
            )
            ,
        )
