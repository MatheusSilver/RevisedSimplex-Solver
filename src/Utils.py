import os

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
            value = "-" + value
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

    # Setter para __language
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

class FileUtils:
    @staticmethod
    def get_files(directory: str) -> list:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            LanguageUtils.print_translated("no_files_to_solve_error")
        return files