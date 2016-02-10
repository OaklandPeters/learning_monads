"""
Annotations
"""
import typing

__all__ = (
    'AnnotationsDescriptor',
    'Annotations',
)


class AnnotationsDescriptor:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):

        print()
        print("owner_self:", type(owner_self), owner_self)
        print()
        import ipdb
        ipdb.set_trace()
        print()
        
        return self.fget(owner_cls)


class Annotations(dict):
    pass


def replace_annotations_in_namespace(namespace):
    for name, value in namespace.items():
        _replace_annotations(value)
    return namespace

def _replace_annotations(value):
    if hasattr(value, '__annotations__'):
        annotations = typing.get_type_hints(value)
        value.__annotations__ = AnnotationsDescriptor(Annotations(annotations))
        return value
    # wrapped functions, such as classmethods
    elif hasattr(value, '__func__'):
        return _replace_annotations(value.__func__)

