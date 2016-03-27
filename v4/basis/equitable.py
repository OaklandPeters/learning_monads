from ...support.typecheckable import TypeCheckableMeta


class Equitable(metaclass=TypeCheckableMeta):
    """
    Almost all classes will inherit __eq__ from 'object', but many should
    actually override this anyway.
    """
    def __eq__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return not self == other
