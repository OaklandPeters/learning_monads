from abc import ABCMeta, abstractclassmethod


def _has_concrete_method(cls, name):
    if any(name in klass.__dict__ for klass in cls.__mro__):
        method = getattr(cls, name)
        if not getattr(method, '__isabstractmethod__', False):
            return True
    return False


class TypeCheckableMeta(ABCMeta):
    """Makes isinstance and issubclass overrideable."""

    def __instancecheck__(cls, instance):
        if _has_concrete_method(cls, '__instancecheck__'):
            return cls.__instancecheck__(instance)
        else:
            # If __instancheck__ NOT redefined
            #   OR if it is redefined, but as an abstractmethod
            return ABCMeta.__instancecheck__(cls, instance)

    def __subclasscheck__(cls, subclass):
        if _has_concrete_method(cls, '__subclasscheck__'):
            return cls.__subclasscheck__(subclass)
        else:
            return ABCMeta.__subclasscheck__(cls, subclass)


class TypeCheckable(metaclass=TypeCheckableMeta):
    @abstractclassmethod
    def __instancecheck__(cls, instance):
        return NotImplemented

    @abstractclassmethod
    def __subclasscheck__(cls, subclass):
        return NotImplemented


def meets(klass: 'type', abstracts: 'Union[Sequence[str]]'):
    return not missing_abstracts(klass, abstracts)


def _missing_abstracts(klass, abstracts):
    for method in abstracts:
        for base in klass.__mro__:
            if method in base.__dict__:
                break
        else:
            yield method


def missing_abstracts(klass, abstracts):
    if hasattr(abstracts, '__abstractmethods__'):
        abstracts = abstracts.__abstractmethods__
    return list(_missing_abstracts(klass, abstracts))


def meets_interface(klass, interface):
    """Maybe problem - pulling __abstractmethods__ from interface might
    be a problem. collections.abc does not do this - and I'm assuming there is a
    good reason.
    """
    return meets(klass, interface.__abstractmethods__)


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
