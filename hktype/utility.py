import typing


def attributes_with_annotations(namespace: typing.Mapping):
    for name, value in namespace.items():
        yield from _if_annotation(name, value)

def _if_annotation(name, value):
    if hasattr(value, '__annotations__'):
        yield (name, value)
    # wrapped functions, such as classmethods, try recursive descent
    elif hasattr(value, '__func__'):
        yield from _if_annotation(value.__func__)

