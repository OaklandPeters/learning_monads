"""
Support functions which use or reference classes defined in category.py,
so this is defined afterward, and should not be imported there.
"""
import category


def apply_recursively(function, guard=category.Element):
    """
    Helper function, to handle recursing down nested monadic structures,
    (such as list of lists).

    Intended to work with f_apply. Example:
    > list_nested.f_apply(recurse(add2))
    > list_nested = ListElement(1, 2, ListElement(3, 4))
    > add2 = lambda num: num+2
    ListElement(3, 4, ListElement(5, 6))
    """
    def wrapper(obj):
        if isinstance(obj, guard):
            return obj.f_apply(wrapper)
        else:
            return function(obj)
    return wrapper
