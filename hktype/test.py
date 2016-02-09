"""
Test
"""
import unittest
import typing

from support_pre import abstractclassproperty
import hktyping
import corrector


#======================================
# Define elements shared across tests
#======================================
class Category:
    """Placeholder"""
    @abstractclassproperty
    def Element(cls):
        return NotImplemented

    @abstractclassproperty
    def Morphism(cls):
        return NotImplemented

class AnyCategory(Category):
    Element = typing.Any
    Morphism = typing.Callable

class ListCategory(Category):
    Element = list
    Morphism = typing.Callable[[list], list]










class HKGenericTests(unittest.TestCase):
    """
    @TODO: copy 'fmap_like' method to test_generics_replacement

    More tests to write:
    * Standard typing.Generic behavior
    * Generics-replacement on instances
    * Generics-replacement on instance-methods
    """
    def test_standard_generics(self):
        Domain = typing.TypeVar('Domain')
        Codomain = typing.TypeVar('Codomain')

        class Functor(typing.Generic[Domain, Codomain]):
            def fmap_like(self, function: Domain) -> Codomain:
                pass
        class ListFunctor(Functor[AnyCategory, ListCategory]):
            pass
        listf = ListFunctor()

        self.assertEqual(Functor.__parameters__, (Domain, Codomain))
        self.assertEqual(ListFunctor.__parameters__, (AnyCategory, ListCategory))
        self.assertEqual(listf.__parameters__, (AnyCategory, ListCategory))


        self.assertEqual(
            typing.get_type_hints(Functor.fmap_like),
            {'function': Domain, 'return': Codomain})
        # This is bad behavior - the __annotations__ on methods on our child class & instances
        #   does not reflect the changes to __parameters__
        #   However, this is the default behavior of typing, so I'm testing for it
        self.assertEqual(
            typing.get_type_hints(ListFunctor.fmap_like),
            {'function': Domain, 'return': Codomain})
        self.assertEqual(
            typing.get_type_hints(listf.fmap_like),
            {'function': Domain, 'return': Codomain})

    def test_generics_replacement(self):
        """
        Most basic change. Confirm that generic parameters are actually swapped
        out on child classes.
        """
        Domain = hktyping.HKTypeVar('Domain')
        Codomain = hktyping.HKTypeVar('Codomain')

        class Functor(hktyping.HKGeneric[Domain, Codomain]):
            def fmap_like(self, function: Domain) -> Codomain:
                pass
        class ListFunctor(Functor[AnyCategory, ListCategory]):
            pass
        listf = ListFunctor()

        self.assertEqual(Functor.__parameters__, (Domain, Codomain))
        self.assertEqual(ListFunctor.__parameters__, (AnyCategory, ListCategory))
        self.assertEqual(listf.__parameters__, (AnyCategory, ListCategory))

        #
        #  THIS IS BAD - AND I SHOULD FEEL BAD
        #   It looks like the replacement is occuring to the parent, which is terrible
        #
        self.assertNotEqual(
            typing.get_type_hints(Functor.fmap_like),
            {'function': Domain, 'return': Codomain})
        # These are correct
        self.assertEqual(
            typing.get_type_hints(ListFunctor.fmap_like),
            {'function': AnyCategory, 'return': ListCategory})
        self.assertEqual(
            typing.get_type_hints(listf.fmap_like),
            {'function': AnyCategory, 'return': ListCategory})


    #def test_standard_forward_ref(self):
    #    Domain = typing.TypeVar('Domain')
    #    Codomain = typing.TypeVar('Codomain')
    #    CF = typing._ForwardRef
    #    class Functor(typing.Generic[Domain, Codomain]):
    #        def f_apply(cls, element: CF('Codomain'), function: CF('Domain')) -> CF('Codomain'):
    #            pass
    #    class ListFunctor(Functor[AnyCategory, ListCategory]):
    #        pass
    #    self.assertEqual(ListFunctor.__parameters__, (AnyCategory, ListCategory))

    #    print()
    #    print("f_apply.__annotations__:", type(f_apply.__annotations__), f_apply.__annotations__)
    #    print()
    #    import ipdb
    #    ipdb.set_trace()
    #    print()
        

    #def test_structure_ref(self):
    #    """Old-style structured ref.
    #    Drawn from corrected_generics.py

    #    This DOES work when placed at the top level, but does NOT when placed inside a class
    #    I suspect that forward_frame is failing.
    #    """
    #    Domain = hktyping.HKTypeVar('Domain')
    #    Codomain = hktyping.HKTypeVar('Codomain')
    #    CF = corrector.CleverForward
    #    class Functor(hktyping.HKGeneric[Domain, Codomain]):
    #        def f_apply(cls, element: CF('Codomain.Element'), function: CF('Domain.Morphism')) -> CF('Codomain.Element'):
    #            pass
    #    class ListFunctor(Functor[AnyCategory, ListCategory]):
    #        pass
    #    print()
    #    print("ListFunctor.__parameters__:", type(ListFunctor.__parameters__), ListFunctor.__parameters__)
    #    print()
    #    import ipdb
    #    ipdb.set_trace()
    #    print()
    #    self.assertEqual(ListFunctor.__parameters__, (AnyCategory, ListCategory))




    #def test_functor(self):
    #    Domain = hktyping.HKTypeVar('Domain')
    #    Codomain = hktyping.HKTypeVar('Codomain')

    #    class Functor(hktyping.HKGeneric[Codomain, Domain]):
    #        @classmethod
    #        def f_apply(cls, element: Codomain.Element, function: Domain.Morphism) -> Codomain.Morphism:
    #            return NotImplemented

    #    class ListFunctor(Functor[AnyCategory, ListCategory]):
    #        """
    #        Waht I really want is for the forward refs on f_map to resolve themselves
    #        in the context of ListFunctor (which has provided values for Codomain and Domain)
    #        """
    #        pass

    #    anno_apply = typing.get_type_hints(ListFunctor.f_apply)


    #    print()
    #    print("anno_map:", type(anno_map), anno_map)
    #    print("anno_apply", type(anno_apply), anno_apply)
    #    print()
    #    import ipdb
    #    ipdb.set_trace()
    #    print()

    #def test_higher_kinded(self):
    #    Domain = hktyping.HKTypeVar('Domain')
    #    Codomain = hktyping.HKTypeVar('Codomain')

    #    class Functor(CorrectedGeneric[Codomain, Domain]):
    #        @classproperty
    #        def Codomain(cls):
    #            return cls.__parameters__[0]

    #        @classproperty
    #        def Domain(cls):
    #            return cls.__parameters__[1]

    #        def getter(cls) -> This.Domain.Element:
    #            return cls.Domain.Element()

    #    class ListFunctor(Functor[AnyCategory, ListCategory]):
    #        """
    #        Waht I really want is for the forward refs on f_map to resolve themselves
    #        in the context of ListFunctor (which has provided values for Codomain and Domain)
    #        """
    #        pass

    #    anno_getter = typing.get_type_hints(ListFunctor.getter)


    #    print()
    #    print("anno_getter:", type(anno_getter), anno_getter)
    #    print()
    #    import ipdb
    #    ipdb.set_trace()
    #    print()



#
#   Add this unit-test
#
#class ThisTests(unittest.TestCase):
#    def test_basic(self):
#        self.assertEqual(This(ListFunctor), ListFunctor)
#        self.assertEqual(This.Domain(ListFunctor), ListFunctor.Domain)
#        self.assertEqual(This.Domain.Morphism(ListFunctor), ListFunctor.Domain.Morphism)


if __name__ == "__main__":
    unittest.main()
