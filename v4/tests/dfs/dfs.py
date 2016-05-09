"""
Goal:    write breadth-first-search and depth-first-search as differing only by 1 swapped line

Note - this is the type of thing that category-theory structures should be able to
express clearly, but I'm not writing it using the full category-theory structure.
... at least, not at this time.
"""
import types

from ...support.methods import pedanticmethod


class List:
    """
    append
    map
    join
    filter
    """
    def __init__(self, values=None):
        if values is None:
            self.values = []
        else:
            self.values = [elm for elm in values]

    def __repr__(self):
        return str.format(
            "{0}[{1}]",
            self.__class__.__name__,
            ", ".join(repr(elm) for elm in self)
        )

    @classmethod
    def zero(cls):
        return cls()

    def __iter__(self):
        return iter(self.values)

    def append(self, other):
        return type(self)([elm for array in (self, other) for elm in array])
    
    def map(self, function):
        return type(self)(function(elm) for elm in self)

    @classmethod
    def _traverse(cls, elm, function):
        if isinstance(elm, cls):
            return elm.traverse(function)
        else:
            return function(elm)
    
    def traverse(self, function):
        # return type(self)(self._traverse(elm, function) for elm in self)
        return type(self)(self.map(lambda elm: self._traverse(elm, function)))


    def filter(self, function):
        return type(self)(elm for elm in self if function(elm))

    def join(self):
        cls = type(self)
        accumulator = cls.zero()
        for elm in self:
            if isinstance(elm, cls):
                accumulator = accumulator.append(elm)
            else:
                accumulator = accumulator.append(cls([elm]))
        return accumulator

    def front(self):
        return type(self)(self[0])

    def back(self):
        return type(self)(self[-1])

    # list magic methods
    def __len__(self):
        return len(self.values)

    def __contains__(self, value):
        return value in self.values

    def __getitem__(self, index):
        return self.values[index]

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        elif len(self) != len(other):
            return False
        else:
            for left, right in zip(self, other):
                # This step may recurse when left is a List
                if left != right:
                    return False
            return True

    def __ne__(self, other):
        return not (self == other)

    @classmethod
    def recurse(cls, function):
        def wrapper(element):
            if isinstance(element, cls):
                return wrapper(element)
            else:
                return function(element)
        return wrapper




class Node:
    value = None
    children = []

    def __init__(self, value=None, children=None):
        self.value = value

        if children is None:
            self.children = List.zero()
        else:
            self.children = List([elm for elm in children])

    def __repr__(self):
        return str.format(
            "{0}({1}, {2})",
            self.__class__.__name__,
            repr(self.value),
            repr(self.children)
        )


    @classmethod
    def zero(cls):
        return cls()

    def __iter__(self):
        return iter(self.children)

    def append(self, other):
        cls = type(self)
        accumulator = (List
                       .zero()
                       .append(self.children)
                       .append(other)
                       # .append(List([other.value]))
                       # .append(other.children)
        )
        return cls(self.value, accumulator)

    def join(self):
        cls = type(self)
        accumulator = cls.zero()
        for elm in self:
            if isinstance(elm, cls):
                accumulator = accumulator.append(elm)
            else:
                accumulator = accumulator.append(cls(elm))
        return cls(self.value, accumulator)

    def filter(self, function):
        """Applies to children"""
        cls = type(self)
        accumulator = cls.zero()
        for child in self.children:
            if function(child):
                accumulator = accumulator.append(child)
        return cls(self.value, *accumulator)

    def map(self, function):
        cls = type(self)
        return cls(
            function(self),
            List(function(elm) for elm in self.children)
        )

    @classmethod
    def _traverse(cls, elm, function):
        if isinstance(elm, cls):
            return elm.traverse(function)
        elif isinstance(elm, List):
            return elm.traverse(function)
        else:
            return function(elm)
    
    def traverse(self, function):
        cls = type(self)
        return cls(
            function(self.value),
            List(cls._traverse(elm, function) for elm in self.children)
        )
        # return self.map(lambda elm: self._traverse(elm, function))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        elif self.value != other.value:
            return False
        elif len(self.children) != len(other.children):
            return False
        else:
            for left, right in zip(self.children, other.children):
                # This step may recurse when left is a List
                if left != right:
                    return False
            return True

    def __iter__(self):
        return iter(self.children)

    @pedanticmethod
    def join(cls, self):
        cls = type(self)
        accumulator = cls(self.value)  #  List
        tail = List()
        for element in self:
            if isinstance(element, cls):
                accumulator = accumulator.append([element.value])
                tail = tail.append(element.children)
            else:  # Not a Node
                accumulator = accumulator.append([element])
        accumulator.children = accumulator.children.append(tail)
        return accumulator



#
#   Traversal functions
#
def traverse(elm, function):
    """Utility function in recursive traversals."""
    if hasattr(elm, 'traverse'):
        return elm.traverse(function)
    else:
        return function(elm)

def identity(x):
    return x

def iterator_traversal(node, function=identity):
    """~ BFS flat iterator for a tree.
    @todo: Write this with .traverse
    """    
    yield function(node.value)
    for child in node.children:
        yield from iterator_traversal(child, function)
