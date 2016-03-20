from ...support.typecheckable import Interface


class Equitable(Interface):
    """
    Almost all classes will inherit __eq__ from 'object', but many should
    actually override this anyway.
    """
    def __eq__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return not self == other
