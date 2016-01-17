

# class CategoryMeta(type):
#     """Placeholder"""

class Category(type):
    """Placeholder.
    Basically CategoryBase.
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

    def __eq__(self, other):
        if hasattr(other, 'category'):
            if self.category == other.category:
                return self.data == other.data
        else:
            return False

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(repr(elm) for elm in self.data)
        )

class Object(Monoid):
    """
    @todo: Move *everything* off of ListObject, and into this.
    This is used to seperate Objects from Morphisms in a given class,
    since the signatures of their methods should differ.
    And also, we want to be able to pattern match/distinguish functions
    from objects/elements.
    """
    def f_apply(self, function):
        return self.category.f_apply(self, function)

    def a_apply(self, morphism):
        return self.category.a_apply(self, morphism)


class Morphism(Monoid):
    """
    f_map is not meaningfully defined for this, because f_map expects
    to take a bare *single* function.

    @todo: Move *everything* off of ListMorphism, and into this.
    """
    def a_map(self):
        return self.category.a_map(self)

    def __call__(self, *args, **kwargs):
        return self.a_map()(*args, **kwargs)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join(repr(elm) for elm in self.data)
        )

class Base:
    """
    This should be an abstract
    """
    #@abstractmethod
    def __init__(self, *elements):
        return NotImplemented

    #@abstractproperty
    def category(self):
        return NotImplemented


def apply_recursively(function, guard=Object):
    """
    Helper function, makes it recurse down nested monadic structure
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
