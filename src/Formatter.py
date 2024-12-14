import numpy as np

class FormatUtils:
    SPECIAL_SIMBOLS = ["<=", ">=", "=", "+", "-"]

    @staticmethod
    def string_to_array(string: str, variables_order: list) -> np.ndarray[np.float64]:
        np_array = np.empty((len(variables_order)))
        for idx, var in enumerate(variables_order):
            np_array[idx] = FormatUtils._read_number(string, var)
        np_array = np_array.astype(np.float64)
        return np_array


    @staticmethod
    def get_variables_vector(string):
        variables = []

        curIndex = 0
        stringList = string.split(" ")
        for term in stringList:
            if term in FormatUtils.SPECIAL_SIMBOLS or term.startswith("max") or term.startswith("min"):
                continue
            charIndex = 0
            while charIndex < len(term):
                if term[charIndex].isdigit():
                    charIndex += 1
                else:
                    break
            variable = term[charIndex:]
            if variable not in variables and not variable == "":
                variables.append(variable)


        return variables

    @staticmethod
    def _read_number(expression: str, variable: str) -> str:
        variable_index = expression.find(variable)
        if variable_index == -1:
            return "0"
        half_expression = expression[:variable_index].split(" ")[-2:]
        if not half_expression[-1].isdigit():
            value = 1
        else:
            value = half_expression[-1]
        if len(half_expression) >= 2 and half_expression[-2] == "-":
            value = "-" + value
        return value






    @staticmethod
    def format_file(input: str) -> list:
        input = input.split('\n')

        clearedFile = []

        for line in input:
            if (not line.startswith("#") and len(line) > 3):
                line = line.strip().split("#")[0]
                if (line not in clearedFile):
                    clearedFile.append(line)

        return clearedFile