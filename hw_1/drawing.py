import matplotlib.pyplot as plt
import networkx as nx

from hw_1.astvisitor import NxVisitor


def get_sizes(tree, root, sizes):
    children = list(tree.neighbors(root))
    my_width = 0
    my_height = 3
    if len(children):
        for child in children:
            sizes, child_width, child_height = get_sizes(tree, child, sizes)
            my_width += child_width
            my_height = max(my_height, 3 + child_height)
    else:
        my_width = 3
    sizes[root] = my_width
    return sizes, my_width, my_height


def tree_layout(tree, root):
    sizes, width, height = get_sizes(tree, root, {})

    def _tree_layout(node, pos, root_x=0., root_y=0.):
        pos[node] = (root_x, root_y)
        children = list(tree.neighbors(node))
        if len(children):
            x = root_x - sizes[node] / 2
            for child in children:
                pos = _tree_layout(child, pos, x + sizes[child] / 2, root_y - 2)
                x += sizes[child]
        return pos

    return _tree_layout(root, {}), width, height


def draw_tree(tree):
    visitor = NxVisitor()
    visitor.visit(tree)
    graph = nx.tree_graph(visitor.root)
    pos, w, h = tree_layout(graph, visitor.root["id"])
    plt.figure(1, figsize=(w * 0.5, h * 0.5))
    colors = [visitor.colors[node] for node in graph]
    nx.draw(graph, pos, node_color=colors, labels=visitor.labels, with_labels=True, node_size=4000, node_shape="s")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=visitor.edge_labels)
    plt.show()
