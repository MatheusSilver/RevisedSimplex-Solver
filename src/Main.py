import os
import numpy as np

from src.Formatter import FormatUtils as formatter
from src.Solver import RevisedSimplex


class Main:

    DEFAULT_PROBLEM = (
        "max 3x + 5y + 2z\n"
        "#sujeito a:\n"              # Essa linha não é obrigatória e é ignorada pelo programa.
        "1x - 2y + 1z <= 10\n"
        "2x + 1y + 3z <= 15\n"
        "x, y, z >= 0\n"
    )
    DEFAULT_FILE = "../data/LP_Problem.txt"

    DEFAULT_RESTRICTIONS = ["<=", "=", ">="]


    @staticmethod
    def start():
        lp_problem = Main.read_problem()
        lp_problem = formatter.format_file(lp_problem)

        lp_variables = Main.get_lp_variables(lp_problem[:-1])
        constraint_matrix = Main.setup_constraint_matrix(lp_problem[1:-1], lp_variables)
        isMaximization = Main.__checkMaximization(lp_problem[0])
        objective_expression = " ".join(lp_problem[0].split(" ")[1:])
        objective_function = formatter.string_to_array(objective_expression, lp_variables)
        restrictions_vector = Main.__get_restrictions(lp_problem[1:-1])

    @staticmethod
    def __get_restrictions(constraints: list) -> np.ndarray[np.float64]:
        np_array = np.empty((len(constraints)))
        for i in range(len(constraints)):
            symbol = Main._identify_restrictions(constraints[i])
            if (len(symbol) < 2):
                continue
            else:
                np_array[i] = constraints[i].split(symbol)[1]
        return np_array.astype(np.float64)

    @staticmethod
    def _identify_restrictions(expression: str) -> str:
        for symbol in Main.DEFAULT_RESTRICTIONS:
            if expression.startswith(symbol):
                return symbol
        return ""



    @staticmethod
    def setup_constraint_matrix(constraints: list, variables: list) -> np.ndarray:
        constraint_matrix = np.zeros((len(constraints),len(variables)), dtype=np.float64)
        for i in range(len(constraints)):
            constraint_matrix[i] = formatter.string_to_array(constraints[i], variables)
        return constraint_matrix



    @staticmethod
    def get_lp_variables(lp_problem: list) -> list:
        global_vars = []

        for line in lp_problem:
            local_variables = formatter.get_variables_vector(line)
            for variable in local_variables:
                if variable not in global_vars:
                    global_vars.append(variable)

        return sorted(list(global_vars))


    @staticmethod
    def __checkMaximization(objective_function: str) -> bool:
        if "max" in objective_function or "min" in objective_function:
            return True if "max" in objective_function else False
        raise ValueError(f"O problema não é reconhecido como maximização ou minimização.")

    @staticmethod
    def read_problem():
        directory = os.path.dirname(Main.DEFAULT_FILE)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(Main.DEFAULT_FILE):
            with open(Main.DEFAULT_FILE, "x") as file:
                file.write(Main.DEFAULT_PROBLEM)
            with open(Main.DEFAULT_FILE, "r") as file:
                return file.read()
        else:
            with open(Main.DEFAULT_FILE, "r") as file:
                return file.read()


if (__name__ == "__main__"):
    Main.start()
