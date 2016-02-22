def standard_repr(obj, *sequence, **mapping):
    keywords = tuple("{0}={1}".format(repr(key), repr(value)) for key, value in mapping.items())
    return str.format(
        "{0}({1})",
        getattr(obj, '__name__', obj.__class__.__name__),
        ", ".join(repr(elm) for elm in (sequence + keywords))
    )


def standard_str(obj, *sequence, **mapping):
    keywords = tuple("{0}={1}".format(key, value) for key, value in mapping.items())
    return str.format(
        "{0}({1})",
        getattr(obj, '__name__', obj.__class__.__name__),
        ", ".join(str(elm) for elm in (sequence + keywords))
    )
