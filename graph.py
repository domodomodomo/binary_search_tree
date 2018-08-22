import graphviz
import random
import log


def source(binary_search_tree, max_depth=0):
    return _create_diagraph(binary_search_tree, max_depth).source


def render(binary_search_tree, max_depth=0):
    _create_diagraph(binary_search_tree, max_depth).render(
        'sample.gv', view=True)


def _create_diagraph(binary_search_tree, max_depth=0):

    root = binary_search_tree.root
    node_list = [node for node in log._node_generator(root)]
    diagraph = graphviz.Digraph('BST')
    for node in node_list:
        diagraph.node(str(id(node)), str(node.value))

    for node in node_list:
        if node.left:
            diagraph.edge(str(id(node)), str(id(node.left)))
        if node.right:
            diagraph.edge(str(id(node)), str(id(node.right)))

    # fill by blank node
    route_list = [list(log._route(root, node)) for node in node_list]
    depth_list = [len(route) - 1 for route in route_list]
    height_list = [max(depth_list) - depth for depth in depth_list]
    for node, height in zip(node_list, height_list):
        if height:
            if not node.left:
                diagraph.edge(
                    str(id(node)),
                    _blank_tree(diagraph, height - 1))
            if not node.right:
                diagraph.edge(
                    str(id(node)),
                    _blank_tree(diagraph, height - 1))

    return diagraph.source


def _blank_tree(diagraph, height):
    identity = str(random.randint(0, 10000000000000))
    diagraph.node(identity, 'apple', fontcolor='white')
    if height:
        diagraph.edge(identity, _blank_tree(diagraph, height - 1))
        diagraph.edge(identity, _blank_tree(diagraph, height - 1))
    return identity
