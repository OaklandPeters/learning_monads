"""
python3 -m unittest v4.tests.dfs.test_dfs
"""
import unittest

from .dfs import List, Node, traverse, iterator_traversal, identity


def _DFS(node, check):
    return (
        List([node.value])
        .filter(check)
        .append(
            node.children  # if children is Zero --> map returns zero
            .map(lambda child: _DFS(child, check))
            .filter(check)
        )
        .join()
    )


def DFS(node, check):
    return (
        List
        .zero()
        .append(
            _DFS(node, check)
        )
    )

def BFS(node, check):
    base = _BFS(node, check)
    return base

def _BFS(node, check):
    return (
        List([node.value])
        .append(
            node.children
            .map(lambda child: _BFS(child, check))
        )
        .join()
    )

    flatter = node.join()
    return (
        List
        .zero()
        .append

    )


def node_join(self):
    """
    Basically Node.join(), but self is a list
    """
    cls = type(self)
    accumulator = cls()  #  List
    tail = cls()
    for element in self:
        if not isinstance(element, cls):
            accumulator = accumulator.append([element])
        else:  # it's a List -- treat as Node
            value = element[0]
            children = element[1:]
            accumulator = accumulator.append([value])
            # now somehow children need to go at the end
            tail = tail.append(children)
    return accumulator.append(tail)


def pre_merge(node):
    """This correctly gets the order of visitation for DFS."""
    return (
        List
        .zero()
        .append(
            node.children
            .map(pre_merge)
            .join()
        )
        .append([node.value])
        # .join()
    )

def post_merge(node):
    return _post_merge(Node('None', [node]))

def _post_merge(node):
    """This approximately gets the ordering correct of BFS, 
    but is ~joining them incorrectly.

    post = post_merge(explicit)
    post[0] == '0'
    post[1] == List['0-0', ... the descendants of 0-0, ...
    post[2] == List['0-1', ... the descendants of 0-1, ...]
    """
    return (
        List
        .zero()
        # .append([node.value])
        .append(
            node.children
            .map(lambda child: child.value)
        )
        .append(
            node.children
            .map(_post_merge)
            .join()
        )        
    )







#
# Testing utility functions
#

def add2(x):
    return int.__add__(x, 2)

def counter(initial=0, step=1):
    counter = initial
    while(True):
        yield counter
        counter += 1
from_zero = counter(initial=0)

def inc():
    return next(from_zero)

def is_all(x):
    return (x % 1 == 0)

def is_even(x):
    return (x % 2 == 0)

def is_odd(x):
    return (x % 2 == 1)
def last_char_is_odd(word):
    return is_odd(int(word[-1]))

def last_char_is_even(word):
    return is_even(int(word[-1]))




#
#   Data
#
explicit = Node('0', [
    Node('0-0', [
        Node('0-0-0', [
            Node('0-0-0-0'),
            Node('0-0-0-1'),
        ]),
        Node('0-0-1'),
        Node('0-0-2', [
            Node('0-0-2-0'),
            Node('0-0-2-1'),
            Node('0-0-2-2'),
        ])
    ]),
    Node('0-1'),
    Node('0-2', [
         Node('0-2-0')
    ]),
])
tree = Node(inc(), [
    Node(inc(), [
        Node(inc(), [
            Node(inc()),
            Node(inc()),
        ]),
        Node(inc(), []),
    ]),
    Node(inc(), []),
    Node(inc(), [
         Node(inc(), [])
    ]),
])




dfs_result = DFS(explicit, lambda x: True)
bfs_result = BFS(explicit, lambda x: True)


# joined = node_join(bfs_result)


print()
print("dfs_result:", type(dfs_result), dfs_result)
print("bfs_result:", type(bfs_result), bfs_result)
# print("joined:", type(joined), joined)
print()
import ipdb
ipdb.set_trace()
print()


#
#   Todo: Incorporate unit-tests for these
#
bush = tree.map(identity)

twig = Node(1, [Node(2), Node(3)])
twiggy = twig.map(identity)
ttwiggy = twig.traverse(identity)
twiggy_plus2 = twig.traverse(add2)
twig_flat = twig.join()



thing = List([1, 2, List([3, 4])])
thingy = thing.map(identity)
thing_flat = thing.join()
tthingy = thing.traverse(identity)



#d_result = DFS(tree, is_odd)
#b_result = BFS(tree, is_odd)


pre = pre_merge(explicit)
post = post_merge(explicit)

print()
#print("d_result:", type(d_result), d_result)
#print("b_result:", type(b_result), b_result)
# print("pre_result:", type(pre_result), pre_result)
# print("post_result:", type(post_result), post_result)
print("pre:", type(pre), pre)
print("post:", type(post), post)
print()
import ipdb
ipdb.set_trace()
print()






class ListTests(unittest.TestCase):
    def test_append(self):
        self.assertEqual(
        )
        pass

    def test_map_identity(self):
        pass

    def test_map(self):
        pass

    def test_join(self):
        pass

    def test_traverse_identity(self):
        pass

    def test_traverse(self):
        pass

class NodeTests(unittest.TestCase):
    def test_join(self):
        self.assertEqual(
            Node(1, List([Node(3, List([4, 5]))])),
            Node(1, List([3, 4, 5]))
        )



class TreeSearchTests(unittest.TestCase):
    def test_simple(self):
        pass
