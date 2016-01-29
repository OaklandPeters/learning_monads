"""
This provides tests of category-theoretic laws. In the form of 
unit-test related Mixin classes, for Functor, Applicative, Monad, and Monoid.

These are things that should be true for every implementation.
"""
import unittest
import abc





class FunctorLaws(metaclass=abc.ABCMeta):

    @abc.abstractproperty
    def Functor(self):
        return NotImplemented

    @ABC.abstractproperty
    def get_element(self):
        """Return random element in this category."""
        return NotImplemented

    @abc.abstractmethod
    def get_morphism(self):
        """Return random morphism that can operate on single elements in thsi category."""
        return NotImplemented

    def test_fmap_identity(self):
        """
        fmap id      = id
        """
        identity = lambda value: value
        mapped = self.Functor.f_map(identity)
        for value in (self.get_element() for _ in range(5)):
            self.assertEqual(mapped(value), identity(value))

    def test_fmap_composition(self):
        """
        fmap (p . q) = (fmap p) . (fmap q)
        """
        for _ in range(5):
            p, q = self.get_morphism(), self.get_morphism()

            p_q = lambda element: p(q(element))
            fp_q = self.Functor.f_map(p_q)

            fp, fq = self.Functor.f_map(p), self.Functor.f_map(q)
            fp_fq = self.Functor.compose()

            self.assertEqual(
            )
