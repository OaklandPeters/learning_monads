
import typing

# class CategoryMeta(type):
#     """Placeholder"""

class Category(type):
    """
    Acts as both a metaclass, and as the authoritative location of all
    monadic methods for a monad-category.
    """


class Monoid:
    @classmethod
    def zero(cls):
        return cls.category.zero()

    def append(self, value):
        # return self.category.append(value)
        return self.category.append(self, value)

    def join(self):
        return self.category.join(self)



class Object:
    """
    This is used to seperate Objects from Morphisms in a given class,
    since the signatures of their methods should differ.

    And also, we want to be able to pattern match/distinguish functions
    from objects/elements.
    """
    def f_apply(self, function):
        return self.category.f_apply(self, function)

    def a_apply(self, morphism):
        """
        a_apply(element, morphism) --> destructures morphism (such as in List, destructures into multiple functions), and fmap's each destructured func over 'element'
        """
        return self.category.a_apply(self, morphism)

    def m_apply(self, constructor):
        """
        Basically Haskell's 'bind'
        In this context, a constructor means a function taking
        arguments from the domain category, into the monad's category.
        constructor::(a -> m b)
        """
        return self.category.m_apply(self, constructor)


class Morphism:
    """
    This is used to seperate Objects from Morphisms in a given class,
    since the signatures of their methods should differ.

    And also, we want to be able to pattern match/distinguish functions
    from objects/elements.

    f_map and a_map are not meaningfully defined for this, because f_map/m_map
    expect to take a bare (non-wrapped) *single* function.

    @todo: Move *everything* off of ListMorphism, and into this.
    """
    def a_map(self):
        return self.category.a_map(self)

    def __call__(self, *args, **kwargs):
        return self.a_map()(*args, **kwargs)


class Monad(Monoid):
    """
    This should be an abstract
    """
    def __new__(cls, *elements):
        """
        Dispatches to Morphism/Object classes where possible,
        as the Monad is not meant to be directly instantiatable.
        Requires instantiated Morphism and Object class properties.
        """
        if issubclass(cls, Object) or issubclass(cls, Morphism):
            self = object.__new__(cls)
        else:
            # Calls to constructor of List itself should dispatch
            if all(isinstance(elm, typing.Callable) for elm in elements):
                self = object.__new__(cls.Morphism)
            else:
                self = object.__new__(cls.Object)
        self.__init__(*elements)
        return self


    #@abstractmethod
    def __init__(self, *elements):
        return NotImplemented

    #@abstractproperty
    #def Category(self):
    #    return NotImplemented

    #@abstractproperty
    #def Morphism(cls):
    #   return NotImplemented

    #@abstractproperty
    #def Object(cls):
    #   return NotImplemented

    @classmethod
    def f_map(cls, function):
        return self.category.f_map(function)

    @classmethod
    def m_map(cls, constructor):
        return self.category.m_map(constructor)


def apply_recursively(function, guard=Object):
    """
    Helper function, to handle recursing down nested monadic structures,
    (such as list of lists).

    Intended to work with f_apply. Example:
    > list_nested.f_apply(recurse(add2))
    > list_nested = ListObject(1, 2, ListObject(3, 4))
    > add2 = lambda num: num+2
    ListObject(3, 4, ListObject(5, 6))
    """
    def wrapper(obj):
        if isinstance(obj, guard):
            return obj.f_apply(wrapper)
        else:
            return function(obj)
    return wrapper


class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
