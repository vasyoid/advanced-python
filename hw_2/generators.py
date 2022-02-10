import operator
from functools import reduce
from itertools import chain


__all__ = ['gen_header', 'gen_footer', 'gen_table', 'gen_image']


def gen_header():
    return """\\documentclass[12pt]{article}
\\usepackage[left=0.50in, right=0.50in]{geometry}
\\usepackage{graphicx}
\\begin{document}
"""


def gen_footer():
    return "\\end{document}"


def are_all(predicate, sequence):
    return reduce(operator.and_, map(predicate, sequence), True)


def are_valid_row_types(data):
    return are_all(lambda line: isinstance(line, list), data)


def are_valid_row_sizes(data):
    return len(data) > 0 and len(data[0]) > 0 and \
           reduce(lambda res, l: (l, res[1] and (res[0] < 0 or res[0] == l)), map(len, data), (-1, True))[1]


def is_data_valid(data):
    return are_valid_row_types(data) and are_valid_row_sizes(data)


def gen_col_pattern(data):
    return reduce(lambda res, _: res + "c|", data[0], "|")


def gen_row(row):
    return f"{' & '.join(map(str, row))}\\\\"


def gen_rows(data):
    return "\n\\hline\n".join(chain([""], map(gen_row, data), [""]))


def do_gen_table(data):
    return f"\\begin{{tabular}}{{{gen_col_pattern(data)}}}{gen_rows(data)}\\end{{tabular}}\n"


def gen_table(data):
    return is_data_valid(data) and do_gen_table(data) or "Invalid input\n"


def gen_image(path):
    return f"\n\\includegraphics[width=1\\textwidth]{{{path}}}\n"
