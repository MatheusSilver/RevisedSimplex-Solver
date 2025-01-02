DATA_INPUT = "../data/input/"
DATA_OUTPUT = "../data/output/"
VALID_YES = ["s", "y", "yes", "sim", "si"]

EXAMPLE_FILE = "example.txt"
DEFAULT_PROBLEM = """max 3x + 5y
#sujeito a:
x + y <= 4
2x + 3y <= 9
x, y >= 0"""

LATEX_INITIALIZATION = r"""\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath} 
\usepackage{amssymb}
\usepackage{graphicx} 
\usepackage{xcolor} 

\begin{document}"""