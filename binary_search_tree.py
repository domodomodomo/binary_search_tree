

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


#
# functions returning iterators
#
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
