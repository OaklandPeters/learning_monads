"""
ForwardReference types


add_context_to_hkforwardrefs, must be called during class construction.
These forward-references might need to work with a custom TypeVar class

"""
import typing



class HKForwardRefBase(typing._ForwardRef):
    pass


class HKForwardRef(HKForwardRefBase):
    """Authoritative version of Higher-Kinded forward reference.
    For now, just a stub
    """



def add_context_to_hkforwardrefs(cls):
    """Adds a connection to 'cls', to the HigherKindedRef
    """


#=============================
#  Drafts
#=============================
class _HKForwardRefDumb(typing._ForwardRef):
    pass

