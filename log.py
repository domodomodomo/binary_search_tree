def output(binary_search_tree):
    return output_node(binary_search_tree.root)


def output_node(root):
    if not root:
        return '\n'

    if not all(0 <= value <= 99 for value in root.list()):
        raise ValueError('A value shoud be between 0 and 99.')

    node_list = [node for node in _node_generator(root)]
    route_list = [list(_route(root, node)) for node in node_list]
    value_list = [str(value).zfill(2) for value in root.list()]
    index_list = [_index(_path(route)) for route in route_list]
    depth_list = [len(route) - 1 for route in route_list]
    height_list = [max(depth_list) - depth for depth in depth_list]
    position_list = [_position(height, index) for height, index in
                     zip(height_list, index_list)]

    # layer_list
    layer_len = (4 * 2**max(depth_list) - 2)
    layer = ' ' * layer_len
    layer_list = [layer] * (max(depth_list) + 1)
    for depth, position, value\
            in zip(depth_list, position_list, value_list):
        layer_list[depth] = _paste(
            pasted=layer_list[depth], seal=value, position=position,)

    return '\n'.join(layer_list)


def _node_generator(binary_search_node):
    bsn = binary_search_node
    if bsn.left:
        yield from _node_generator(bsn.left)
    yield bsn
    if bsn.right:
        yield from _node_generator(bsn.right)


def _route(root, node):
    yield root

    if node.value < root.value:
        if root.left:
            yield from _route(root.left, node)
        else:
            raise ValueError
    elif node.value > root.value:
        if root.right:
            yield from _route(root.right, node)
        else:
            raise ValueError
    elif node.value == root.value:
        if node is not root:
            yield from _route(root.right, node)
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
def register_printer(BST):
    BST.insert = _register_printer(BST.insert)
    BST.delete_left = _register_printer(BST.delete_left)
    BST.delete_right = _register_printer(BST.delete_right)


def _register_printer(func):
    def decorated_func(binary_search_tree, *args, **kwargs):
        if not(0 <= args[0] <= 99):
            raise ValueError('A value shoud be between 0 and 99.')

        result = func(binary_search_tree, *args, **kwargs)

        print(output(binary_search_tree))
        return result
    return decorated_func
