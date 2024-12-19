import numpy as np
from src.Parser import FileParser


class RevisedSimplex:
    def __init__(self, file):
        data = FileParser(file).parse_file()
        self.variables = data["lp_variables"]
        self.variable_values = [0 for _ in self.variables]
        self.constraint_matrix = data["constraint_matrix"]
        self.isMaximization = data["is_maximization"]
        self.objective = data["objective_function"]
        self.restrictions = data["restrictions_vector"]
        self.restriction_symbols = data["symbols"]
        self.slack_variables = []
        self.artificial_variables = []

    def solve(self, show_steps: bool = False):

        if self.isMaximization:
            self.objective *= -1

        self.__standardize_problem(show_steps)

        from_phase_one = False
        if self.__solve_phase_one(show_steps) == 0:
            from_phase_one = True
        self.__solve_phase_two(from_phase_one, show_steps)

    def __get_initial_artificial_basis(self) -> list[str]:
        number_of_variables = len(self.variables)
        current_artificial_index = 0
        initial_basis = []
        for i in (range(len(self.slack_variables))):
            if self.variable_values[number_of_variables + i] != 0:
                initial_basis.append(self.slack_variables[i])
            else:
                initial_basis.append(self.artificial_variables[current_artificial_index])
                current_artificial_index += 1
        while current_artificial_index < len(self.artificial_variables):
            initial_basis.append(self.artificial_variables[current_artificial_index])
            current_artificial_index += 1

        return initial_basis

    def __get_initial_artificial_non_basis(self, initial_basis: list[str]) -> list[str]:
        initial_non_basis = []
        possible_variables = self.variables + self.slack_variables+self.artificial_variables
        for i in (range(len(possible_variables))):
            if possible_variables[i] not in initial_basis:
                initial_non_basis.append(possible_variables[i])
        return initial_non_basis



    def __solve_phase_one(self, show_steps: bool = False) -> int:
        if len(self.artificial_variables) < 1:
            return -1
        
        artificial_costs = np.zeros(len(self.variables) + len(self.slack_variables) + len(self.artificial_variables))
        artificial_costs[-len(self.artificial_variables):] = 1  # Custos das artificiais

        # Configuração inicial
        self.basis = self.__get_initial_artificial_basis()
        self.non_basis = self.__get_initial_artificial_non_basis(self.basis)
        profit = artificial_costs

        # Matriz básica inicial
        basic_indexes = self.__get_basic_indexes()
        non_basic_indexes = self.__get_non_basic_indexes()
        b = self.__get_basic_matrix(basic_indexes)

        # Resolver usando o loop principal
        result = self.__solver_loop(b, basic_indexes, non_basic_indexes, profit, self.restrictions, True, show_steps)

        # Validar viabilidade
        if result == -1 or any(basic_var in self.artificial_variables for basic_var in self.basis):
            raise ValueError("Problema inviável: solução inicial não encontrada.")
        print("Fase 1 concluída com sucesso.")

        self.__remove_artificial_variables()

        return 0

    def __solve_phase_two(self, from_phase_one: bool, show_steps: bool = False) -> None:
        if not from_phase_one:
            self.basis = self.slack_variables.copy()
            self.non_basis = self.variables.copy()

        profit = np.concatenate((self.objective, np.zeros(len(self.slack_variables) + len(self.artificial_variables))))
        basic_indexes = self.__get_basic_indexes()
        non_basic_indexes = self.__get_non_basic_indexes()
        b = self.__get_basic_matrix(basic_indexes)

        result = self.__solver_loop(b, basic_indexes, non_basic_indexes, profit, self.restrictions, False, show_steps)

        #Todo: Implementar um indicador melhor disso.
        if result == 0 and self.basis == self.slack_variables:
            print("problema não factível")
            return

        if result == 0:
            print("Solução ótima encontrada!")
            print("Variáveis básicas:", self.basis)
            print("Valores:", self.get_solution())

    def get_solution(self) -> dict:
        variables_list = self.variables + self.slack_variables + self.artificial_variables
        return {variables_list[i]: self.variable_values[i] for i in range(len(variables_list))}

    def __solver_loop(self, basic_matrix: np.ndarray[np.float64], basic_indexes: list[int],
                      non_basic_indexes: list[int], profit_vector: np.ndarray[np.float64],
                      restrictions_vector: np.ndarray[np.float64], is_phase_one: bool, show_steps: bool = False) -> int:

        restrictions_vector = restrictions_vector.reshape(-1, 1)
        variables_list = self.variables + self.slack_variables + self.artificial_variables

        while True:
            inv_b = np.linalg.inv(basic_matrix)

            x_b = inv_b @ restrictions_vector

            p_t = profit_vector[basic_indexes] @ inv_b

            c_r = profit_vector[non_basic_indexes] - p_t @ self.constraint_matrix[:, non_basic_indexes]
            in_index = self.__get_negative_pivot(c_r, show_steps)
            if in_index == -1:
                return 0  # Código de sucesso

            c_n = self.constraint_matrix[:, in_index].reshape(-1, 1)
            y = inv_b @ c_n
            if np.all(y <= 0):
                print("Solução ilimitada detectada")
                return -1  # Solução ilimitada

            ratios = np.where(y > 0, x_b / y, np.inf)
            out_index = self.__get_positive_pivot(ratios, show_steps)

            out_index_basic = basic_indexes[out_index]
            in_index_non_basic = non_basic_indexes[in_index]

            basic_indexes[out_index], non_basic_indexes[in_index] = self.__update_variable_values(basic_indexes, variables_list, x_b, y,
                                                                                        out_index, in_index_non_basic, out_index_basic)

            basic_matrix[:, out_index] = self.constraint_matrix[:, in_index_non_basic]

            if show_steps:
                print(f"Iteração concluída: variável {in_index_non_basic} entrou, {out_index_basic} saiu")

            if is_phase_one and not any(index in self.artificial_variables for index in basic_indexes):
                return 0

    def __update_variable_values(self, basic_indexes, variables_list: list[str], x_b, y, out_index,
                                 in_index_non_basic, out_index_basic) -> (int, int):
        pivot_value = np.float64(x_b[out_index] / y[out_index])
        self.variable_values[in_index_non_basic] = pivot_value
        for i, basic_index in enumerate(basic_indexes):
                self.variable_values[basic_index] -= np.float64(pivot_value * y[i])



        out_variable, in_variable = variables_list[out_index_basic], variables_list[in_index_non_basic]
        self.basis[self.basis.index(out_variable)] = in_variable
        self.non_basis[self.non_basis.index(in_variable)] = out_variable

        return in_index_non_basic, out_index_basic



    def __get_basic_matrix(self, basic_indexes: list[int]) -> np.ndarray[np.float64]:
        b = self.constraint_matrix[:, basic_indexes]
        return b

    def __get_basic_indexes(self) -> list[int]:
        variables_list = self.variables + self.slack_variables + self.artificial_variables
        return [variables_list.index(var) for var in self.basis]

    def __get_non_basic_indexes(self) -> list[int]:
        variables_list = self.variables + self.non_basis + self.artificial_variables
        return [variables_list.index(var) for var in self.non_basis]

    @staticmethod
    def __get_basic_profits(basic_indexes: list[int], costs: np.ndarray[np.float64]) -> np.ndarray[np.float64]:
        return costs[basic_indexes]

    @staticmethod
    def __get_negative_pivot(relative_costs: np.ndarray[np.float64], show_steps: bool = False) -> int:
        negative_indexes = np.where(relative_costs < 0)[0]
        if negative_indexes.size == 0:
            return -1

        min_index = negative_indexes[np.argmin(relative_costs[negative_indexes])]

        return int(min_index)

    @staticmethod
    def __get_positive_pivot(ratios: np.ndarray[np.float64], show_steps: bool = False) -> int:
        positive_indexes = np.where(ratios > 0)[0]
        if positive_indexes.size == 0:
            return -1
        min_index = positive_indexes[np.argmin(ratios[positive_indexes])]

        return int(min_index)

    def __standardize_problem(self, show_steps: bool = False) -> None:
        self.artificial_variables = []
        self.slack_variables = []

        num_restrictions = len(self.restriction_symbols)
        artificial_lines = []
        slack_lines = []
        for i in range(num_restrictions):
            symbol = self.restriction_symbols[i]

            if symbol == "<=":
                slack = f"s_{i + 1}"
                self.slack_variables.append(slack)
                slack_lines.append(i)

            elif symbol == ">=":
                slack = f"s_{i + 1}"
                self.slack_variables.append(slack)
                artificial_variable = f"a_{i + 1}"
                self.artificial_variables.append(artificial_variable)
                artificial_lines.append(i)
                slack_lines.append(i)
            elif symbol == "=":
                artificial_variable = f"a_{i + 1}"
                self.artificial_variables.append(artificial_variable)
                artificial_lines.append(i)

        for i in slack_lines:
            if i in artificial_lines:
                self.__add_variable_to_matrix(i, -1)
            else:
                self.__add_variable_to_matrix(i, 1)

        for i in artificial_lines:
            self.__add_variable_to_matrix(i, 1)

    def __add_variable_to_matrix(self, line_to_add: int, value: int) -> None:
        col = np.zeros((len(self.restriction_symbols), 1))
        col[line_to_add, 0] = value
        self.constraint_matrix = np.hstack((self.constraint_matrix, col))
        self.__add_variable_value_to_vector(line_to_add, value)

    def __add_variable_value_to_vector(self, line_to_add: int, value: int) -> None:
        restriction_value = self.restrictions[line_to_add]
        if value==-1:
            self.variable_values.append(0)
        else:
            self.variable_values.append(restriction_value)

    def __remove_artificial_variables(self):
        for i in range(len(self.artificial_variables)):
            self.variable_values.pop()
            self.non_basis.remove(self.artificial_variables[i])
            self.artificial_variables.pop()
