import ast
import sys

from drawing import draw_tree


def read_code(path):
    with open(path) as file:
        return file.read()


if __name__ == '__main__':
    code = read_code(sys.argv[1])
    tree = ast.parse(code)
    print(ast.dump(tree, indent=" "))
    draw_tree(tree)
