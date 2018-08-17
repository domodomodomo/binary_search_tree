import random
import unittest


def sample_code():
    bst = BinarySearchTree()

    #
    # 1. insert
    #
    print('### 1. insert')
    bst.insert(8)
    bst.insert(3)
    bst.insert(1)
    bst.insert(6)
    bst.insert(10)
    bst.insert(4)
    bst.insert(7)
    bst.insert(14)
    bst.insert(13)
    print(Debug.log(bst))
    print()
    """
                  08
          03              10
      01      06              14
            04  07          13
    """

    #
    # 2. search
    #
    print('### 2. search')
    print(bst.search(13).value)
    print()
    """
    13
    """

    #
    # 3. list
    #
    print('### 3. list')
    print(bst.list())
    print(bst.list_sequentially())
    print()
    """
    [1, 3, 4, 6, 7, 8, 10, 13, 14]
    """

    #
    # 4. delete
    #
    print('### 4. delete')
    bst.delete_right(8)
    print(Debug.log(bst))
    print()
    """
                  10
          03              14
      01      06      13
            04  07
    """

    bst.delete_left(10)
    print(Debug.log(bst))
    print()
    """
                  07
          03              14
      01      06      13
            04
    """


#
# BinarySearchTree
#
class BinarySearchTree(object):
    def __init__(self):
        self.root = None

    # 1. insert
    def insert(self, value):
        if self.root:
            self.root.insert(value)
        else:
            self.root = BinarySearchNode(value)

    # 2. search
    def search(self, value):
        if self.root:
            return self.root.search(value)
        else:
            raise ValueError

    # 3. list
    def list(self):
        if self.root:
            return self.root.list()
        else:
            return []

    def list_sequentially(self):
        if self.root:
            return self.root.list_sequentially()
        else:
            return []

    # 4. delete
    def delete_left(self, value):
        if self.root:
            self.root = self.root.delete_left(value)
        else:
            raise ValueError

    def delete_right(self, value):
        if self.root:
            self.root = self.root.delete_right(value)
        else:
            raise ValueError

    def __iter__(self):
        if self.root:
            return iter(self.root)
        else:
            return iter([])  # empty iterator


#
# BinarySearchNode
#
class BinarySearchNode(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    #
    # 1. insert
    #
    def insert(self, value):
        if value < self.value:
            if self.left:
                self.left.insert(value)
            else:
                self.left = BinarySearchNode(value)
        elif value >= self.value:
            if self.right:
                self.right.insert(value)
            else:
                self.right = BinarySearchNode(value)

    #
    # 2. search
    #
    def search(self, value):
        if value < self.value:
            if self.left:
                return self.left.search(value)
            else:
                raise ValueError
        elif value > self.value:
            if self.right:
                return self.right.search(value)
            else:
                raise ValueError
        elif value == self.value:
            return self

    def search_max(self):
        if self.right:
            return self.right.search_max()
        else:
            return self

    def search_min(self):
        if self.left:
            return self.left.search_min()
        else:
            return self

    #
    # 3. list
    #
    def list(self):
        if self.left:
            left_sorted_list = self.left.list()
        else:
            left_sorted_list = []

        center = self.value

        if self.right:
            right_sorted_list = self.right.list()
        else:
            right_sorted_list = []

        return left_sorted_list + [center] + right_sorted_list

    def list_sequentially(self):
        sorted_list = []
        path = Path(self)
        while True:
            try:
                value = next(path)
            except StopIteration:
                break
            else:
                sorted_list.append(value)
        return sorted_list

    #
    # 4. delete
    #
    def delete_left(self, value):
        if value < self.value:
            if self.left:
                self.left = self.left.delete_left(value)
            else:
                raise ValueError
        elif value > self.value:
            if self.right:
                self.right = self.right.delete_left(value)
            else:
                raise ValueError
        elif value == self.value:
            old_self = self
            if old_self.left:
                self = old_self.left.search_max()
                self.left = old_self.left.delete_max()
                self.right = old_self.right
            else:
                self = old_self.right
            old_self.left = None
            old_self.right = None
        return self

    def delete_right(self, value):
        if value < self.value:
            if self.left:
                self.left = self.left.delete_right(value)
            else:
                raise ValueError
        elif value > self.value:
            if self.right:
                self.right = self.right.delete_right(value)
            else:
                raise ValueError
        elif value == self.value:
            old_self = self
            if old_self.right:
                self = old_self.right.search_min()
                self.right = old_self.right.delete_min()
                self.left = old_self.left
            else:
                self = old_self.left
            old_self.left = None
            old_self.right = None
        return self

    def delete_max(self):
        if self.right:
            self.right = self.right.delete_max()
        else:
            self = self.left
        return self

    def delete_min(self):
        if self.left:
            self.left = self.left.delete_min()
        else:
            self = self.right
        return self

    def __iter__(self):
        raise NotImplementedError


#
# Path
#   iterator
#
class Path(object):
    def __init__(self, root):
        pseudo_node = BinarySearchNode(None)
        pseudo_node.right = root
        self._route = [pseudo_node]

    def __next__(self):
        if self._current_node().right:
            self._seek_right_min()
        else:
            self._seek_right_parent()
        return self._current_node().value

    def _seek_right_min(self):
        self._route.append(self._current_node().right)
        while self._current_node().left:
            self._route.append(self._current_node().left)

    def _seek_right_parent(self):
        try:
            while self._route.pop() == self._current_node().right:
                pass
        except IndexError:
            raise StopIteration

    def _current_node(self):
        return self._route[-1]

    def __iter__(self):
        return self


def list_iterator(binary_search_node):
    return iter(binary_search_node.list())


def iterator(binary_search_node):
    return Path(binary_search_node)


def generator(binary_search_node):
    bsn = binary_search_node
    if bsn.left:
        yield from bsn.left
    yield bsn.value
    if bsn.right:
        yield from bsn.right


#
# Test
#
#   $ python -m unittest binary_search_tree.py
#
class Test(unittest.TestCase):
    def runTest(self):
        self.test_insert_list_delete_left()

    #
    # 1. insert, delete, list
    #
    def test_insert_list_delete_left(self):
        bst = BinarySearchTree()
        for value in (random.randint(0, 99) for value in range(1000)):
            bst.insert(value)
        lst = bst.list()
        random.shuffle(lst)
        for value in lst:
            bst.delete_left(value)
        self.assertEqual(bst.list(), [])

    def test_insert_list_sequentially_delte_right(self):
        bst = BinarySearchTree()
        for value in (random.randint(0, 99) for value in range(1000)):
            bst.insert(value)
        lst = bst.list_sequentially()
        random.shuffle(lst)
        for value in lst:
            bst.delete_right(value)
        self.assertEqual(bst.list(), [])

    #
    # 2. iterator
    #
    def test_iterator(self):
        bst = BinarySearchTree()
        for value in (random.randint(0, 99) for value in range(1000)):
            bst.insert(value)

        BinarySearchNode.__iter__ = iterator
        self.assertEqual(bst.list(), list(bst))

    def test_generator(self):
        bst = BinarySearchTree()
        for value in (random.randint(0, 99) for value in range(1000)):
            bst.insert(value)
        BinarySearchNode.__iter__ = generator
        self.assertEqual(bst.list(), list(bst))


#
# Debug
#
class Debug:
    def __new__(cls):
        raise NotImplementedError(
            'Debug is namespace, and not intended to instantiate.')

    #
    # log
    #
    def log(binary_search_tree):
        return Debug.log_node(binary_search_tree.root)

    def log_node(root):
        if not root:
            return '\n'

        if not all(0 <= value <= 99 for value in root.list()):
            raise ValueError('A value shoud be between 0 and 99.')

        node_list = [node for node in Debug._node_generator(root)]
        route_list = [list(Debug._route(root, node)) for node in node_list]
        value_list = [str(value).zfill(2) for value in root.list()]
        index_list = [Debug._index(Debug._path(route)) for route in route_list]
        depth_list = [len(route) - 1 for route in route_list]
        height_list = [max(depth_list) - depth for depth in depth_list]
        position_list = [Debug._position(height, index) for height, index in
                         zip(height_list, index_list)]

        # layer_list
        layer_len = (4 * 2**max(depth_list) - 2)
        layer = ' ' * layer_len
        layer_list = [layer] * (max(depth_list) + 1)
        for depth, position, value\
                in zip(depth_list, position_list, value_list):
            layer_list[depth] = Debug._paste(
                pasted=layer_list[depth], seal=value, position=position,)

        return '\n'.join(layer_list)

    def _node_generator(binary_search_node):
        bsn = binary_search_node
        if bsn.left:
            yield from Debug._node_generator(bsn.left)
        yield bsn
        if bsn.right:
            yield from Debug._node_generator(bsn.right)

    def _route(root, node):
        yield root

        if node.value < root.value:
            if root.left:
                yield from Debug._route(root.left, node)
            else:
                raise ValueError
        elif node.value > root.value:
            if root.right:
                yield from Debug._route(root.right, node)
            else:
                raise ValueError
        elif node.value == root.value:
            if node is not root:
                yield from Debug._route(root.right, node)
            else:
                StopIteration

    def _path(route):
        path = []
        iterator = iter(route)
        next(iterator)
        for parent, child in zip(route, iterator):
            path.append(0 if parent.left is child else 1)
        return path

    def _index(path):
        index = 0
        n = len(path)
        for digit, exponent in zip(path, reversed(range(n))):
            index += digit * 2**exponent
        return index

    def _paste(pasted, seal, position):
        pasted = list(pasted)
        for i, c in enumerate(seal):
            pasted[position + i] = c
        return ''.join(pasted)

    def _position(height, index):
        initial = 2 * (2**height - 1)
        space = 4 * 2**height
        position = initial + space * index
        return position

    #
    #
    #
    def register_printer():
        BST = BinarySearchTree
        BST.insert = Debug._register_printer(BST.insert)
        BST.delete_left = Debug._register_printer(BST.delete_left)
        BST.delete_right = Debug._register_printer(BST.delete_right)

    def _register_printer(func):
        def decorated_func(binary_search_tree, *args, **kwargs):
            if not(0 <= args[0] <= 99):
                raise ValueError('A value shoud be between 0 and 99.')

            result = func(binary_search_tree, *args, **kwargs)

            print(Debug.log(binary_search_tree))
            return result
        return decorated_func

    #
    #
    #
    def dot_file(binary_search_tree, max_depth=0):
        import graphviz

        root = binary_search_tree.root
        node_list = [node for node in Debug._node_generator(root)]
        diagraph = graphviz.Digraph('BST')
        for node in node_list:
            diagraph.node(str(id(node)), str(node.value))

        for node in node_list:
            if node.left:
                diagraph.edge(str(id(node)), str(id(node.left)))
            if node.right:
                diagraph.edge(str(id(node)), str(id(node.right)))

        #
        # fill by blank node
        #
        route_list = [list(Debug._route(root, node)) for node in node_list]
        depth_list = [len(route) - 1 for route in route_list]
        height_list = [max(depth_list) - depth for depth in depth_list]
        for node, height in zip(node_list, height_list):
            if height:
                if not node.left:
                    diagraph.edge(
                        str(id(node)),
                        Debug._blank_tree(diagraph, height - 1))
                if not node.right:
                    diagraph.edge(
                        str(id(node)),
                        Debug._blank_tree(diagraph, height - 1))

        # return diagraph.source
        diagraph.render('test-output/round-table.gv', view=True)

    def _blank_tree(diagraph, height):
        print('here')
        identity = str(random.randint(0, 10000000000000))
        diagraph.node(identity, 'apple', fontcolor='white')
        if height:
            diagraph.edge(identity, Debug._blank_tree(diagraph, height - 1))
            diagraph.edge(identity, Debug._blank_tree(diagraph, height - 1))
        return identity


#
#
#
if __name__ == '__main__':
    sample_code()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test)
    unittest.TextTestRunner().run(suite)
