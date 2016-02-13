"""
ForwardReference types


add_context_to_hkforwardrefs, must be called during class construction.
These forward-references might need to work with a custom TypeVar class.

class HKTypeVar(typing.TypeVar, typing._ForwardRef)
TypeVar's are established inside a typing expression. They inherit
'ThisType'/'UnderscoreType' like functionality, that returns an object
which is *both* a TypeVar and a ForwardRef

"""
import typing

import utility



class HKForwardRefBase(typing._ForwardRef):
    # Context is the class/instance to pass into the HK resolution function
    context = None


class HKForwardRef(HKForwardRefBase):
    """Authoritative version of Higher-Kinded forward reference.
    For now, just a stub
    """


def add_context_to_hkforwardrefs(cls):
    """Adds a connection to 'cls', to the HigherKindedRef
    """
    namespace = vars(cls)
    for name, attr in utility.attributes_with_annotations(namespace):
        for arg_name, arg_value in attr.__annotations__.items():
            if isinstance(arg_value, HKForwardRefBase):
                arg_value.context = cls
    return namespace
        

#=============================
#  Drafts
#=============================
class _HKForwardRefDumb(HKForwardRefBase):
    def __new__(cls, arg):
    pass

