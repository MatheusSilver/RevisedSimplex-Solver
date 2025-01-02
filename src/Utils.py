import os
from fractions import Fraction

import numpy as np

from src.LanguageDictionary import LanguageDictionary


class FormatUtils:
    SPECIAL_SIMBOLS = ["<=", ">=", "=", "+", "-"]

    @staticmethod
    def string_to_array(string: str, variables_order: list) -> np.array:
        np_array = np.empty((len(variables_order)))
        for idx, var in enumerate(variables_order):
            np_array[idx] = FormatUtils._read_number(string, var)
        np_array = np_array.astype(np.float64)
        return np_array


    @staticmethod
    def get_variables_vector(string):
        variables = []

        string_list = string.split(" ")
        for term in string_list:
            if term in FormatUtils.SPECIAL_SIMBOLS or term.startswith("max") or term.startswith("min"):
                continue
            char_index = 0
            while char_index < len(term):
                if term[char_index].isdigit() or term[char_index] in FormatUtils.SPECIAL_SIMBOLS:
                    char_index += 1
                else:
                    break
            variable = term[char_index:]
            if variable not in variables and not variable == "":
                variables.append(variable)


        return variables

    @staticmethod
    def _read_number(expression: str, variable: str) -> str:
        variable_index = expression.find(variable)
        if variable_index == -1:
            return "0"
        half_expression = expression[:variable_index].split(" ")[-2:]
        if half_expression[-1] == "-":
            value = -1
        elif not half_expression[-1].isdigit():
            value = 1
        else:
            value = half_expression[-1]
        if len(half_expression) >= 2 and half_expression[-2] == "-":
            value = -float(value)
        return value

    @staticmethod
    def format_file(file_content: str) -> list:
        file_content = file_content.split('\n')

        cleared_file = []

        for line in file_content:
            line = line.strip()
            if not line.startswith("#") and len(line) > 1:
                line = line.split("#")[0]
                if line not in cleared_file:
                    cleared_file.append(line)

        return cleared_file

class LanguageUtils:
    __language = "pt"

    @staticmethod
    def get_language() -> str:
        return LanguageUtils.__language

    @staticmethod
    def set_language(language: str) -> None:
        if language not in LanguageDictionary.LANGUAGE_REFERENCE:
            error_message = LanguageUtils.get_translated_text(
                "language_not_found_error") + f"{', '.join(LanguageDictionary.LANGUAGE_REFERENCE.keys())}"
            raise ValueError(error_message)
        LanguageUtils.__language = language

    @staticmethod
    def print_translated(key: str) -> None:
        print(LanguageUtils.get_translated_text(key))

    @staticmethod
    def get_translated_text(key: str) -> str:
        return LanguageDictionary.get_text(key, LanguageUtils.__language)

    @staticmethod
    def get_translated_text_variable_text(key: str, substitution_variables: list[str]) -> str:
        text = LanguageUtils.get_translated_text(key)
        if len(substitution_variables) == 0:
            return text

        formatted_text = text
        for i in range(len(substitution_variables)):
            formatted_text = formatted_text.replace(f"<x{i+1}>", substitution_variables[i])

        return formatted_text

    @staticmethod
    def get_available_languages() -> list[str]:
        return list(LanguageDictionary.LANGUAGE_REFERENCE.keys())


class FileUtils:
    @staticmethod
    def get_files(directory: str) -> list[str]:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            LanguageUtils.print_translated("no_files_to_solve_error")
        return files

class LatexUtils:
    @staticmethod
    def format_value(value: str) -> str:
        if value == "inf" or value == "-inf":
            return value
        try:
            value_to_check = float(value)
            if value_to_check % 1 != 0:
                fraction = Fraction(value_to_check).limit_denominator()
                return f"\\frac{{{fraction.numerator}}}{{{fraction.denominator}}}"
            else:
                return str(int(value_to_check))
        except ValueError:
            return LatexUtils.format_variable(value)

    @staticmethod
    def format_string_vector(vector: list[str]) -> str:
        result = r"\{"
        for i in range(len(vector)):
            result += f"{LatexUtils.format_value(vector[i])}"
            if i < len(vector) - 1:
                result += ", "

        result += "\}"
        return result

    @staticmethod
    def format_numbers_vector(vector: np.array(np.float64)) -> str:
        result = r"\{"
        for i in range(len(vector)):
            result += f"{LatexUtils.format_value(str(vector[i]))}"
            if i < len(vector) - 1:
                result += ", "

        result += "\}"
        return result

    @staticmethod
    def format_matrix(matrix: np.ndarray) -> str:
        result = r"\begin{bmatrix}"

        if matrix.ndim == 1:
            result += " & ".join(LatexUtils.format_value(str(x)) for x in matrix) + r" \\"
        else:
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    result += f"{LatexUtils.format_value(str(matrix[i][j]))}"
                    if j < len(matrix[i]) - 1:
                        result += " & "
                if i < len(matrix) - 1:
                    result += r"\\ "

        result += r"\end{bmatrix}" + "\n"
        return result

    @staticmethod
    def format_matrices(equations: list[np.ndarray[np.float64]]) -> str:
        content = ""
        for equation in equations:
            if len(equation) == 1:
                content += str(equation)
            else:
                content += LatexUtils.format_matrix(equation)
        return content

    @staticmethod
    def format_problem_to_latex(objective_function: np.array(np.float64), constraint_matrix: np.ndarray[np.float64],
                                lp_variables: list[str], restrictions_vector: np.array(np.float64), symbols: list[str], is_maximization: bool) -> str:

        variables_list = LatexUtils.format_variables(lp_variables)

        max_or_min = "maximize_text" if is_maximization else "minimize_text"
        max_or_min = LanguageUtils.get_translated_text(max_or_min)

        content = r"\begin{align*}" + "\n"

        objective = LatexUtils.format_expression(variables_list, objective_function)
        content += rf"\text{{{max_or_min}}} \quad & {objective} \\ " + "\n"

        content += r"\text{"+LanguageUtils.get_translated_text("subject_to_text")+r":} \quad & \\" + "\n"
        for row, symbol, restriction_value in zip(constraint_matrix, symbols, restrictions_vector):
            constraint_expression = LatexUtils.format_expression(variables_list, row, symbol, restriction_value)
            content += rf"\quad & {constraint_expression} \\ " + "\n"

        non_negativity = "\quad &"
        for i in range(len(variables_list)):
            non_negativity += variables_list[i]
            if (i + 1) < len(variables_list):
                non_negativity += ", "
            else:
                non_negativity += " \geq 0"
        content += non_negativity + "\n"

        content += r"\end{align*}" + "\n"

        return content

    @staticmethod
    def format_expression(problem_variables: list[str], left_side: np.array(np.float64), relation_symbol: str = None, right_side: np.float64 = None) -> str:
        expression = ""
        variables_list = LatexUtils.format_variables(problem_variables)
        is_first = True
        for value, var in zip(left_side, variables_list):
            if value == 0:
                continue
            if not is_first:
                expression += " + " if value >= 0 else " "
            else: is_first = False
            expression += LatexUtils.format_value(value) + var
        if relation_symbol is not None and right_side is not None:
            expression += f" {relation_symbol} "
            expression += LatexUtils.format_value(str(right_side))
        return expression

    @staticmethod
    def format_variables(result: list[str]) -> list[str]:
        result = result.copy()
        for i in range(len(result)):
            if "_" in result[i] and not "{" in result[i] and not "}" in result[i]:
                result[i] = LatexUtils.format_variable(result[i])
        return result

    @staticmethod
    def format_variable(variable: str) -> str:
        if "_" in variable and not "{" in variable and not "}" in variable:
            variable_parts = variable.split("_")
            return variable_parts[0] + "_" + "{" + variable_parts[1] + "}"
        return variable