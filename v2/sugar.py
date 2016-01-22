"""
Sugar operators.
"""

class MonadicSugar:
    def __rshift__(self, other: Union[Callable, Morphism]):
        """Pipe. Feeds 'self' into the function 'other'.
        Two types of dispatching involved here:
        (1) If 'other' is not in the same Monadic category, lift it to a Morphism.
        (2) If 'self' is a 
        """
        pass

class ElementSugar:
    def __rshift__(self, other: Union[Callable, Morphism]):
        """Pipe-ing. In this case, immediately invoked
        result = List(1, 2) >> add2 >> mul3
        self.assertEqual(result, List(9, 12))

        or

        result = List(1, 2) >> List(add2) >> mul3
        self.assertEqual(result, List(9, 12))
        """
        if not isinstance(other, self.Category):
            other = self.Category(other)
        return self.a_apply(other)


class MorphismSugar:
    def __rshift__(self, other: Union[Callable, Morphism]):
        """Pipe-ing. ~composition.
        list_f = List(add2) >> mul3
        self.assertEqual(lit_f(List(1, 2)), List(9, 12))

        or 
        list_f = List(add2) >> List(mul3)
        self.assertEqual(lit_f(List(1, 2)), List(9, 12))
        """
        if not isinstance(other, self.Category):
            other = self.Category(other)
        return self.compose(other)
