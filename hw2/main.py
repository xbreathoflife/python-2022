import csv
import operator
import os
from functools import reduce

from ast_fib.main import generate_ast


def start_document() -> str:
    return '\\documentclass[10pt]{article}\n' + \
           '\\usepackage[a4paper,left=15mm,right=15mm,top=10mm,bottom=15mm]{geometry}\n' + \
           '\\usepackage{graphicx}\n\n' + \
           '\\begin{document}'


def end_document() -> str:
    return '\\end{document}'


def start_table(row: list) -> str:
    return '\\begin{tabular}{ ' + reduce(operator.add, map(lambda r: '|c', row)) + '| }\n'


def end_table() -> str:
    return '\\end{tabular}\n'


def transform_row(row: list) -> str:
    return " & ".join(row) + " \\\\ \n"


def combine_rows(row_prev: str, cur_row: str) -> str:
    return row_prev + '\\hline \n' + cur_row


def add_hlines(table: str) -> str:
    return '\\hline \n' + table + '\\hline \n'


def get_table(data: list) -> str:
    return start_table(data[0]) + add_hlines(reduce(combine_rows, map(transform_row, data))) + end_table() + '\n'


def get_picture(path: str) -> str:
    return f'\\includegraphics[width=0.9\\linewidth]{{{path}}}\n'


def get_tex(data: list, path: str):
    return start_document() + get_table(data) + get_picture(path) + end_document()


def generate_tex(csv_filename: str, image_path: str):
    data = list(csv.reader(open(csv_filename)))
    return get_tex(data, image_path)


if __name__ == '__main__':
    pic = "artifacts/ast.png"
    generate_ast(pic)
    with open("artifacts/result.tex", "w") as text_file:
        text_file.write("%s" % generate_tex('artifacts/addresses.csv', pic))
    os.system("/Library/TeX/texbin/pdflatex -output-directory=artifacts artifacts/result.tex")
    os.system("rm artifacts/result.aux artifacts/result.log")

