from binary_search_tree import BinarySearchTree
from binary_search_tree import BinarySearchNode
from binary_search_tree import sample_code


class BinarySearchTree(BinarySearchTree):
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root:
            self.root.insert(value)
        else:
            self.root = BinarySearchNode(value, None)


class BinarySearchNode(BinarySearchNode):
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None

    #
    # insert
    #
    def insert(self, value):
        if value < self.value:
            if self.left:
                self.left.insert(value)
            else:
                self.left = BinarySearchNode(value, self)
        elif value >= self.value:
            if self.right:
                self.right.insert(value)
            else:
                self.right = BinarySearchNode(value, self)

    #
    # delete
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
                if self.left:
                    self.left.parent = self
                self.right = old_self.right
                if self.right:
                    self.right.parent = self
                self.parent = old_self.parent
            else:
                self = old_self.right
                if self:
                    self.parent = old_self.parent
            old_self.parent = None
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
                if self.right:
                    self.right.parent = self
                self.left = old_self.left
                if self.left:
                    self.left.parent = self
                self.parent = old_self.parent
            else:
                self = old_self.left
                if self:
                    self.parent = old_self.parent
            old_self.parent = None
            old_self.left = None
            old_self.right = None
        return self

    def delete_max(self):
        if self.right:
            self.right = self.right.delete_max()
        else:
            if self.right:
                self.left.parent = self.parent
            self = self.left
        return self

    def delete_min(self):
        if self.left:
            self.left = self.left.delete_min()
        else:
            if self.right:
                self.right.parent = self.parent
            self = self.right
        return self


class Path(object):
    def __init__(self, root):
        self._current_node = root

    def __next__(self):
        if self._current_node.right:
            self._seek_right_min()
        else:
            self._seek_right_parent()
        return self._current_node.value

    def _seek_right_min(self):
        self._current_node = self._current_node.right
        while self._current_node.left:
            self._current_node = self._current_node.left

    def _seek_right_parent(self):
        try:
            self._current_node = self._current_node.parent
            while self._current_node is self._current_node._parent.righ:
                self._current_node = self._current_node.parent
        except AttributeError:
            raise StopIteration

    def __iter__(self):
        return self


if __name__ == '__main__':
    sample_code()
