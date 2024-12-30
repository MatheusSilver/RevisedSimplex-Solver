import numpy as np
from src.Utils import LatexUtils
from src import Constants


class LatexWriter:
    def __init__(self, filename: str):
        self.filename = f"{Constants.DATA_OUTPUT}{filename}_solution.tex"
        self.file = open(self.filename, "w", encoding="utf-8")
        self.write(Constants.LATEX_INITIALIZATION, break_line=True)

    def close(self):
        """Fecha o arquivo e adiciona o final do documento LaTeX."""
        self.write(r"\end{document}", break_line=False)
        self.file.close()

    def write(self, content: str = "", break_line: bool = True):
        """Escreve conteúdo no arquivo LaTeX."""
        if break_line:
            content += "\n\n"
        self.file.write(content)

    def write_matrices_with_labels(self, labels: list[str], matrices: list[np.ndarray]):
        """Escreve múltiplas matrizes com rótulos."""
        if len(labels) != len(matrices):
            raise ValueError("O número de rótulos deve ser igual ao número de matrizes.")

        content = r"\begin{align*}" + "\n"
        for label, matrix in zip(labels, matrices):
            content += f"\\text{{{label}}} & " + self.__format_matrix(matrix) + r" \\ " + "\n"
        content += r"\end{align*}"

        self.write(content, break_line=True)

    def write_column_identifiers(self, matrix: np.ndarray, column_labels: list[str]):
        # Caso de vetor 1D
        converted_labels = LatexUtils.format_variables(column_labels)
        if matrix.ndim == 1:
            if len(matrix) != len(converted_labels):
                raise ValueError("O número de elementos no vetor deve ser igual ao número de rótulos.")
            content = r"\[\begin{array}{|" + "c|" * len(converted_labels) + "}" + "\n"
            content += r"\hline" + "\n"
            content += " & ".join(converted_labels) + r" \\" + "\n"
            content += r"\hline" + "\n"
            content += " & ".join(LatexUtils.format_value(str(matrix[i])) for i in range(len(matrix))) + r" \\" + "\n"
            content += r"\hline" + "\n"
            content += r"\end{array}\]" + "\n"

        # Caso de matriz 2D
        elif matrix.ndim == 2:
            if matrix.shape[1] != len(converted_labels):
                raise ValueError("O número de colunas na matriz deve ser igual ao número de rótulos.")
            content = r"\[\begin{array}{|" + "c|" * len(converted_labels) + "}" + "\n"
            content += r"\hline" + "\n"
            content += " & ".join(converted_labels) + r" \\" + "\n"
            content += r"\hline" + "\n"
            for row in matrix:
                content += " & ".join(LatexUtils.format_value(str(val)) for val in row) + r" \\" + "\n"
            content += r"\hline" + "\n"
            content += r"\end{array}\]" + "\n"

        else:
            raise ValueError("A matriz deve ser 1D ou 2D.")

        self.write(content, True)

    def write_vectors_with_identifiers(self, identifiers: list[str], vectors: list[list[str]]):
        """Escreve vetores com identificadores."""
        formated_identifiers = LatexUtils.format_variables(identifiers)
        content = ""
        for identifier, vector in zip(formated_identifiers, vectors):
            content += "\[\n"
            content += f"{identifier}: {LatexUtils.format_string_vector(vector)}"
            content += "\n\]"

        self.write(content, break_line=True)

    def write_matrix_equations(self, symbol: str, equations: list[np.ndarray], result: np.ndarray):
        """Escreve equações de multiplicação de matrizes."""
        content = "\[ "
        content += f"{symbol} = "
        content += LatexUtils.format_matrices(equations) + " = "
        content += LatexUtils.format_matrix(result)
        content += " \]"
        self.write(content, break_line=True)

    def __format_matrix(self, matrix: np.ndarray) -> str:
        """Formata uma matriz para LaTeX."""
        if matrix.ndim == 1:  # Vetor
            rows = " & ".join(LatexUtils.format_value(str(val)) for val in matrix)
            return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"
        elif matrix.ndim == 2:  # Matriz 2D
            rows = " \\\\\n".join(
                " & ".join(LatexUtils.format_value(str(val)) for val in row) for row in matrix
            )
            return r"\begin{bmatrix}" + rows + r"\end{bmatrix}"
        else:
            raise ValueError("A matriz deve ser 1D ou 2D.")
