"""
1st attempt at a Pythonic version of the Arrow typeclass.
I've made notes
"""
from . import functor
from ...groups import category


class Arrow(category.Category):
    # first
    # second
    # 



class FunctorArrow(functor_category.FunctorCategory, Arrow):
    pass


class CofunctorArrow(functor_category.CofunctorCategory, Arrow):
    pass



class ArrowPromotionError(TypeError, CategoryError):
    pass

class ArrowSugar(FunctorArrow):
    """
    @todo: the first clause is actually part of a Functor. Basically, lets you lift things from Pysk into this Category


    Arrow(f)       -->  (-, f,  - )
    Arrow(x)       -->  (x, -,  - )


    Arrow(f) >> g  -->  (-,  compose(f, g),  - )
    Arrow(f) >> x  -->  (x,       f       ,  - )
    Arrow(x) >> f  -->  (x,       f       ,  - )
    Arrow(x) >> y  -->        TypeError


    Difficult issues:
        What to use as initial values?
        Should function start as 'identity' or NotPassed? 
    """
    @pedanticmethod
    def __rshift__(cls, self, right):
        """
        """
        # ------
        #   This step belongs to FunctorCategory sugar
        # -----
        # If it's already in the Codomain, leave it alone
        if isinstance(right, cls.Codomain):
            pass
        # If it's in the Domain, promote it into the Codomain
        elif isinstance(right, cls.Domain):
            right = functor_category.promote(cls, right)
        else:
            raise ArrowPromotionCategory(str.format(
                "Cannot promote object of type '{0}' into '{1}' because it is not in the Domain {2} or Codomain {3} of {4}",
                right.__class__.__name__, cls.__name__, cls.Domain.__name__,
                cls.Codomain.__name__, cls.__name__
            ))
            

        if cls.is_element(right):
            return cls(

            )
        elif cls.is_morphism(right):
            pass
        else:
            raise TypeError(str.format(
                "I have no idea what to do with '{0}', since it is neither element nor morphism",
                right.__class__.__name__
            ))


    @pedanticmethod
    def __lshift__(cls, self, right):
        """
        """
        # Clearer, but slightly less general:
        # return (self >> right).resolve().extract()
        
        # More general, but opaque
        result = cls.__rshift__(self, right)
        return cls.extract(cls.compute(result))




from ..functor.functor_category import FunctorCategory
from ..category.category import Category


class Pysk:
    """The default Python category.
    Filler. This already exists in related project, I just need to copy it.
    """
    pass


class NotPassed:
    pass



# Not sure if... this inherits from FunctorCategory or MonadCategory
class ArrowCategory(MonadCategory):
    """
    Arrows are a category for which morphisms and elements share a representation.
    Additionally, there are some states which correspond to both/neither of Element/Morphism.

    Translating from Haskell equations:
        arr --> decorate

    """
    def __init__(self, arguments=NotPassed, function=NotPassed, result=NotPassed):
        self.arguments = arguments
        self.function = function
        self.result = result

    def __repr__(self):
        return str.format(
            "{0}({1}, {2}, {3})",
            self.__class__.__name__,
            repr(self.arguments),
            repr(self.function),
            repr(self.result)
        )

    def __str__(self):
        return str.format(
            "{0}({1}, {2}, {3})",
            _clever_str(self.__class__),
            _clever_str(self.arguments),
            _clever_str(self.function),
            _clever_str(self.result)
        )

    @pedanticmethod
    def compute(cls, self):
        return cls(
            self.arguments,
            self.function,
            cls.call(self.function, self.arguments)
        )

    @pedanticmethod
    def extract(cls, self):
        return self.result


class ArrowSugar(ArrowCategory):
    """
    Arrow(f)       -->  (-, f,  - )
    Arrow(x)       -->  (x, -,  - )


    Arrow(f) >> g  -->  (-,  compose(f, g),  - )
    Arrow(f) >> x  -->  (x,       f       ,  - )
    Arrow(x) >> f  -->  (x,       f       ,  - )
    Arrow(x) >> y  -->        TypeError


    Difficult issues:
        What to use as initial values?
        Should function start as 'identity' or NotPassed? 
    """
    @pedanticmethod
    def __rshift__(cls, self, right):
        """
        """
        if not isinstance(right, cls):
            right = cls(right)

        if cls.is_element(right):
            return cls(

            )
        elif cls.is_morphism(right):
            pass
        else:
            raise TypeError(str.format(
                "I have no idea what to do with '{0}', since it is neither element nor morphism",
                right.__class__.__name__
            ))


    @pedanticmethod
    def __lshift__(cls, self, right):
        """
        """
        # Clearer, but slightly less general:
        # return (self >> right).resolve().extract()
        
        # More general, but opaque
        result = cls.__rshift__(self, right)
        return cls.extract(cls.compute(result))


#
#  Utility functions
#
def _clever_str(obj):
    if obj is NotPassed:
        return " - "
    elif hasattr(obj, '__name__'):
        return obj.__name__
    else:
        return repr(obj)


