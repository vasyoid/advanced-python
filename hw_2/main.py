import os

from ast_vis.main import generate
from generators import *
import sample


def gen_tex(data):
    return gen_header() + gen_table(data) + gen_image("ast.png") + gen_footer()


def build_pdf(name):
    os.system(
        f"xelatex -interaction=nonstopmode -halt-on-error -output-directory . {name}.tex && "
        f"rm artifacts/{name}.aux artifacts_host/{name}.log")


def main():
    generate(None, "artifacts_host/ast.png")
    with open("artifacts_host/output.tex", "wt") as file:
        file.write(gen_tex(sample.table))
    build_pdf("output")


if __name__ == '__main__':
    main()
