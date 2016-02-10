"""
Edits __annotations__ inside a namespace, replacing TypeVar with their concrete
versions. Intended to be called during class construction.

This is a somewhat out-dated approach - a more modern approach
is the Annotations descriptor.


Next Steps:



Later Steps:
* Have this replace __annotations__ in the namespace BEFORE class construction,
  because we only want to affect the namespace of this class, not that of it's
  parents.
"""
import typing

import utility


def namespace_annotations_corrector(bases, namespace, parameters):
    """
    Replace type-variables inside namespace.
    This mutates, which is annoying, but copying everything would be slow.
    """
    # Replace type-variables
    for name, value in utility.attributes_with_annotations(namespace):
        corrected = _annotations_corrector(value, bases, parameters)
        value.__annotations__ = corrected
    return namespace


def _annotations_corrector(function, bases, parameters):
    """
    """
    annotations = typing.get_type_hints(function)    
    accumulator = dict()
    for key, value in annotations.items():
        # If it is an unfilled typevar
        if isinstance(value, typing.TypeVar):
            # Find parent with generic version of this parameter
            position = None
            for parent in bases:
                if value in getattr(parent, '__parameters__', []):
                    position = parent.__parameters__.index(value)
            if position is None:
                raise ValueError("Could not find position in __parameters__ of parent classes")
            # If this is a structured reference, resolve it
            if _is_structured_forward_ref(value):
                base = parameters[position]
                tinyns = {value._structured_forward_ref_name: parameters[position]}
                concrete = eval(value._structured_forward_ref_code, tinyns)
            else:
                concrete = parameters[position]
            accumulator[key] = concrete
        else:
            accumulator[key] = value
    return accumulator


#==========================
#
#   TO BE REPLACED BY
#    ACTUAL SUBCLASS
#        HKTypeVar
#
#==========================

def _resolver(forward_code, globalns, localns):
    if globalns is None and localns is None:
        globalns = localns = {}
    elif globalns is None:
        globalns = localns
    elif localns is None:
        localns = globalns
    return typing._type_check(
        eval(forward_code, globalns, localns),
        "Forward references must evaluate to types.")

class CleverForward(typing._ForwardRef):
    """When is the forward replaced?
    Ah, realization..., eval_type replaces the string, with a concrete type.
    That concrete type is later replaced
    """
    def _eval_type(self, globalns, localns):
        code_str = self.__forward_arg__
        parts = code_str.split('.')
        name = parts[0]
        rfront = _resolver(name, globalns, localns)
        structured = structured_forward_ref(rfront, name, code_str)
        return structured

def _is_structured_forward_ref(obj):
    return hasattr(obj, '_structured_forward_ref_name')

def structured_forward_ref(type_var: typing.TypeVar, name:str, code: str):
    """I might need to copy here, becuase I don't know if mutating
    klass (typing.TypeVar ~Domain) will potentially mutate other versions
    of it
    ... I would create a subclass here if they would let me subclass TypeVar ...
    """
    
    structured = copy.deepcopy(type_var)
    setattr(structured, '_structured_forward_ref_name', name)
    setattr(structured, '_structured_forward_ref_code', code)
    return structured
