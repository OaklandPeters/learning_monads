from abc import ABCMeta

class TypeCheckableMeta(ABCMeta):
    """Makes isinstance and issubclass overrideable."""

    def __instancecheck__(cls, instance):        
        if any('__instancecheck__' in klass.__dict__ for klass in cls.__mro__):
            return cls.__instancecheck__(instance)
        else:
            return type.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if any('__subclasscheck__' in klass.__dict__ for klass in cls.__mro__):
            return cls.__subclasscheck__(subclass)
        else:
            return type.__subclasscheck__(cls, subclass)


def type_check(value, *klasses, name='object'):
    if not any(isinstance(value, klass) for klass in klasses):
        return TypeError(str.format(
            "{0} should be type {1}, not '{2}'",
            name.capitalize(),
            ", ".join("'{0}'".format(klass) for klass in klasses),
            type(value).__name__,
        ))
    return value


def type_check_sequence(sequence, *klasses, name='object'):
    for i, value in enumerate(sequence):
        type_check(value, *klasses, name="{0}[{1}]".format(name, i))
    return sequence

def check_validation(cls, *args, **kwargs) -> None:
    """Checks all validation functions defined on
    classes in MRO of 'cls'.
    These functions should be classmethods which raise TypeError or return None.
    """
    for klass in cls.__mro__:
        # does 'klass' define it's own '_validation' method
        if '_validation' in klass.__dict__:
            klass._validation(*args, **kwargs)
