import os
import numpy as np
from src.Utils import FormatUtils

class FileParser:
    DEFAULT_RESTRICTIONS = [">=", "<=", "="]

    def __init__(self, filename: str):
        self.filename = filename

    def parse_file(self):
        lp_problem = self._read_problem()
        lp_problem = FormatUtils.format_file(lp_problem)
        lp_variables = self.__get_lp_variables(lp_problem[:-1])
        constraint_matrix = self.__setup_constraint_matrix(lp_problem[1:-1], lp_variables)
        is_maximization = self.__check_maximization(lp_problem[0])
        objective_expression = " ".join(lp_problem[0].split(" ")[1:])
        objective_function = FormatUtils.string_to_array(objective_expression, lp_variables)
        restrictions_vector = self._get_restrictions(lp_problem[1:-1])
        restriction_simbols = self._get_restrictions_symbols(lp_problem[1:-1])

        return {
            "lp_variables": lp_variables,
            "constraint_matrix": constraint_matrix,
            "is_maximization": is_maximization,
            "objective_function": objective_function,
            "restrictions_vector": restrictions_vector,
            "symbols": restriction_simbols,
        }

    def _read_problem(self):
        directory = os.path.dirname(self.filename)
        if not os.path.exists(directory):
            error_message = f"File {directory} does not exist"
            raise FileNotFoundError(error_message)

        if not os.path.exists(self.filename):
            raise FileNotFoundError

        with open(self.filename, "r") as file:
            return file.read()

    def _get_restrictions_symbols(self, lp_problem: list) -> list:
        symbols = []
        for expression in lp_problem:
            symbol = self._identify_restrictions(expression)
            if symbol != "":
                symbols.append(symbol)

        return symbols

    def _get_restrictions(self, constraints: list) -> np.ndarray:
        np_array = np.empty(len(constraints))
        for i in range(len(constraints)):
            symbol = self._identify_restrictions(constraints[i])
            if len(symbol) < 2 and not symbol == "=":
                continue
            else:
                np_array[i] = constraints[i].split(symbol)[1]
        return np_array.astype(np.float64)

    def _identify_restrictions(self, expression: str) -> str:
        for symbol in self.DEFAULT_RESTRICTIONS:
            if symbol in expression:
                return symbol
        return ""

    @staticmethod
    def __setup_constraint_matrix(constraints: list, variables: list) -> np.ndarray:
        constraint_matrix = np.zeros((len(constraints), len(variables)), dtype=np.float64)
        for i in range(len(constraints)):
            constraint_matrix[i] = FormatUtils.string_to_array(constraints[i], variables)
        return constraint_matrix

    @staticmethod
    def __get_lp_variables(lp_problem: list) -> list:
        global_vars = []
        for line in lp_problem:
            local_variables = FormatUtils.get_variables_vector(line)
            for variable in local_variables:
                if variable not in global_vars:
                    global_vars.append(variable)
        return sorted(global_vars)

    @staticmethod
    def __check_maximization(objective_function: str) -> bool:
        if "max" in objective_function or "min" in objective_function:
            return "max" in objective_function
        raise ValueError("O problema não é reconhecido como maximização ou minimização.")
