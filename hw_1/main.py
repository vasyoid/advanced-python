import ast
import click

from drawing import draw_tree


def read_code(path):
    with open(path) as file:
        return file.read()


@click.command()
@click.argument('path')
def main(path):
    code = read_code(path)
    tree = ast.parse(code)
    print(ast.dump(tree, indent=" "))
    draw_tree(tree)


if __name__ == '__main__':
    main()
