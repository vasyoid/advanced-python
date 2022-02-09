import ast
import click
import inspect

from drawing import draw_tree
from hw_1 import sample


def read_code(path):
    with open(path) as file:
        return file.read()


@click.command()
@click.option('-p', '--path', default=None)
@click.option('-o', '--output', default=None)
def main(path, output):
    if path is None:
        code = inspect.getsource(sample.fib)
    else:
        code = read_code(path)
    print(code)
    ast.parse(code)
    tree = ast.parse(code)
    print(ast.dump(tree, indent=" "))
    draw_tree(tree, output)


if __name__ == '__main__':
    main()
