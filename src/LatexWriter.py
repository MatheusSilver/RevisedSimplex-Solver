import numpy as np
from Utils import LatexUtils, LanguageUtils
import Constants


class LatexWriter:
    def __init__(self, filename: str):
        self.filename = f"{Constants.DATA_OUTPUT}{LanguageUtils.get_language()}/{filename}_{LanguageUtils.get_translated_text('solution_file_id')}.tex"
        self.file = open(self.filename, "w", encoding="utf-8")
        self.write(Constants.LATEX_INITIALIZATION, break_line=True)

    def close(self):
        self.write(r"\end{document}", break_line=False)
        self.file.close()

    def write(self, content: str = "", break_line: bool = True):
        if break_line:
            content += "\n\n"
        self.file.write(content)

    def write_matrices_with_labels(self, labels: list[str], matrices: list[np.ndarray]):
        if len(labels) != len(matrices):
            raise ValueError("O número de rótulos deve ser igual ao número de matrizes.")

        content = r"\begin{align*}" + "\n"
        for label, matrix in zip(labels, matrices):
            content += f"\\text{{{label}}} & " + self.__format_matrix(matrix) + r" \\ " + "\n"
        content += r"\end{align*}"

        self.write(content, break_line=True)

    def write_column_identifiers(self, matrix: np.ndarray, column_labels: list[str]):
        converted_labels = LatexUtils.format_variables(column_labels)
        if matrix.ndim == 1:
            #todo: Talvez converter os outros casos para usar o Join ao invés de is_first...
            content = r"\[\begin{array}{|" + "c|" * len(converted_labels) + "}" + "\n"
            content += r"\hline" + "\n"
            content += " & ".join(converted_labels) + r" \\" + "\n"
            content += r"\hline" + "\n"
            content += " & ".join(LatexUtils.format_value(str(matrix[i])) for i in range(len(matrix))) + r" \\" + "\n"
            content += r"\hline" + "\n"
            content += r"\end{array}\]" + "\n"

        else:
            content = r"\[\begin{array}{|" + "c|" * len(converted_labels) + "}" + "\n"
            content += r"\hline" + "\n"
            content += " & ".join(converted_labels) + r" \\" + "\n"
            content += r"\hline" + "\n"
            for row in matrix:
                content += " & ".join(LatexUtils.format_value(str(val)) for val in row) + r" \\" + "\n"
            content += r"\hline" + "\n"
            content += r"\end{array}\]" + "\n"

        self.write(content, True)

    def write_vectors_with_identifiers(self, identifiers: list[str], vectors: list[list[str]]):
        formated_identifiers = LatexUtils.format_variables(identifiers)
        content = ""
        for identifier, vector in zip(formated_identifiers, vectors):
            content += r"\["+"\n"
            content += f"{identifier}: {LatexUtils.format_string_vector(vector)}"
            content += "\n"+r"\]"

        self.write(content, break_line=True)

    def write_matrix_equations(self, symbol: str, equations: list[np.ndarray[np.float64]], result: np.ndarray):
        content = r"\[ "
        content += f"{symbol} = "
        content += LatexUtils.format_matrices(equations) + " = "
        content += LatexUtils.format_matrix(result)
        content += r" \]"
        self.write(content, break_line=True)

    def break_page(self) -> None:
        self.write("\n\n"+r"\newpage", True)

    def __format_matrix(self, matrix: np.ndarray) -> str:
        if matrix.ndim == 1:
            rows = " & ".join(LatexUtils.format_value(str(val)) for val in matrix)
            return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"
        else:
            rows = " \\\\\n".join(
                " & ".join(LatexUtils.format_value(str(val)) for val in row) for row in matrix
            )
            return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"
