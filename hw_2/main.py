import os

from ast_vis.main import generate
from generators import *
from hw_2 import sample


def gen_tex(data):
    return gen_header() + gen_table(data) + gen_image("ast.png") + gen_footer()


def build_pdf(name):
    # os.system("docker build -t dockertex .")
    os.system(f"""docker run -d -it -v {os.path.abspath(os.getcwd())}/artifacts:/root/ --name dockertex dockertex
    docker exec dockertex xelatex -interaction=nonstopmode -halt-on-error -output-directory . {name}.tex
    docker kill dockertex
    docker rm dockertex
    rm artifacts/{name}.aux artifacts/{name}.log
    """)


def main():
    generate(None, "artifacts/ast.png")
    with open("artifacts/output.tex", "wt") as file:
        file.write(gen_tex(sample.table))
    build_pdf("output")


if __name__ == '__main__':
    main()
