import numpy as np

from src.LatexWriter import LatexWriter
from src.Parser import FileParser
from src.Utils import LatexUtils, LanguageUtils


class RevisedSimplex:
    def __init__(self, file:str = "", show_steps: bool = False, latex_writer: LatexWriter = None):
        if not file == "":
            self.load_problem_data(file)
        if show_steps:
            if latex_writer is None:
                self.should_close = True
                self.latexWriter = LatexWriter(file.split("/")[-1].split(".")[0])
                self.__exercise_number = 1
            else:
                self.should_close = False
                self.latexWriter = latex_writer

        self._setup_without_data()

    def load_problem_data(self, file:str):
        data = FileParser(file).parse_file()
        self.__setup_from_data(data)

    def _setup_without_data(self):
        self.variable_values = [0 for _ in self.variables]
        self.slack_variables = []
        self.artificial_variables = []
        self.status = None  # Ideia vinda do scipy pra organizar melhor qual a conclusão do simplex.
        self.degeneracy_points = []
        self.current_interaction = 0

    def __setup_from_data(self, data):
        self.variables = data["lp_variables"]
        self.constraint_matrix = data["constraint_matrix"]
        self.isMaximization = data["is_maximization"]
        self.objective = data["objective_function"]
        self.restrictions = data["restrictions_vector"]
        self.restriction_symbols = data["symbols"]



    def solve(self, show_steps: bool = False):

        if show_steps:
            self.latexWriter.write(r"\section{" + LanguageUtils.get_translated_text_variable_text("exercise_text", [str(self.__exercise_number)]) + "}")
            self.__write_current_problem()

            self.latexWriter.write()
            self.latexWriter.write("O problema de otimização linear pode ser descrito pelas seguintes matrizes e vetores:") # initial_problem_description
            vector_names = [f"{LanguageUtils.get_translated_text('restriction_matrix_text')} ($A$)", f"{LanguageUtils.get_translated_text('cost_vector_text')} ($c$)", f"{LanguageUtils.get_translated_text('restriction_vector_text')} ($b$)"]
            self.latexWriter.write_matrices_with_labels(vector_names, [self.constraint_matrix, self.objective, self.restrictions])

        self.__standardize_problem(show_steps)

        if self.isMaximization:
            self.objective *= -1
            if show_steps:
                self.latexWriter.write(LanguageUtils.get_translated_text("cost_change_max_text"))
                self.latexWriter.write_matrices_with_labels([f"{LanguageUtils.get_translated_text('cost_vector_text')} (c)"], [self.objective])

        from_phase_one = False
        if self.__solve_phase_one(show_steps) == 0:
            from_phase_one = True
        if self.status != "infeasible" and not "unbounded" in str(self.status):
            self.__solve_phase_two(from_phase_one, show_steps)

        self.__show_process_results(show_steps)

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
        artificial_costs[-len(self.artificial_variables):] = 1

        if show_steps:
            self.latexWriter.write("\subsection{"+LanguageUtils.get_translated_text("phase_one_text")+":}") #Phase_one_text
            self.latexWriter.write(LanguageUtils.get_translated_text("artificial_variable_removal"))
            self.latexWriter.write(LanguageUtils.get_translated_text("artificial_variables_cost"))
            self.latexWriter.write_column_identifiers(artificial_costs, self.__get_variables_list())

        self.basis = self.__get_initial_artificial_basis()
        self.non_basis = self.__get_initial_artificial_non_basis(self.basis)

        if show_steps:
            self.latexWriter.write(LanguageUtils.get_translated_text("initial_basic_non_basic_definition"))
            self.latexWriter.write(LanguageUtils.get_translated_text("artificial_basis_definition"))
            self.latexWriter.write(LanguageUtils.get_translated_text("following_bases_text"))
            self.latexWriter.write_vectors_with_identifiers(["x_b", "x_n"], [self.basis, self.non_basis])
        profit = artificial_costs

        basic_indexes = self.__get_basic_indexes()
        non_basic_indexes = self.__get_non_basic_indexes()
        b = self.__get_basic_matrix(basic_indexes)

        result = self.__solver_loop(b, basic_indexes, non_basic_indexes, profit, self.restrictions, True, show_steps)
        
        if self.__check_infeasibility_phase_one() and result == 0:
            if not show_steps:
                self.__print_current_exercise_status("infeasible/phase_1")
            self.status = "infeasible/phase_1"
            return -1

        if show_steps:
            self.latexWriter.write(LanguageUtils.get_translated_text("phase_1_success_text")) #phase_1_success_text
            self.latexWriter.write_column_identifiers(np.array(self.variable_values), self.__get_variables_list())
            basic_variables_list = self.basis
            non_basic_variables_list = self.non_basis
            self.latexWriter.write_vectors_with_identifiers(["x_b", "x_n"], [basic_variables_list, non_basic_variables_list])
            self.latexWriter.write(LanguageUtils.get_translated_text("phase_1_next_step"))

        self.__remove_artificial_variables()

        return 0

    def __check_infeasibility_phase_one(self) -> bool:
        any_artificial_remaining = any(basic_var in self.artificial_variables for basic_var in self.basis)
        any_negative_artificial = any(artificial_value != 0 for artificial_value in self.variable_values[-len(self.artificial_variables):])
        return any_artificial_remaining or any_negative_artificial

    def __solve_phase_two(self, from_phase_one: bool, show_steps: bool = False) -> None:
        if show_steps:
            self.latexWriter.write("\subsection{"+LanguageUtils.get_translated_text("phase_two_text")+":}")
        if not from_phase_one:
            self.basis = self.slack_variables.copy()
            self.non_basis = self.variables.copy()
            if show_steps:
                self.latexWriter.write(LanguageUtils.get_translated_text("phase_1_skip"))
                self.latexWriter.write(LanguageUtils.get_translated_text("phase_2_direct"))
                self.latexWriter.write_vectors_with_identifiers(["x_b", "x_n"], [self.basis, self.non_basis])
        elif show_steps:
            self.latexWriter.write(LanguageUtils.get_translated_text("from_phase_1"))
            self.latexWriter.write_vectors_with_identifiers(["x_b", "x_n"], [self.basis, self.non_basis])

        profit = np.concatenate((self.objective, np.zeros(len(self.slack_variables))))
        basic_indexes = self.__get_basic_indexes()
        non_basic_indexes = self.__get_non_basic_indexes()
        b = self.__get_basic_matrix(basic_indexes)

        result = self.__solver_loop(b, basic_indexes, non_basic_indexes, profit, self.restrictions, False, show_steps)

        if result == 0 and self.__check_infeasibility_phase_two():
            if not show_steps:
                self.__print_current_exercise_status("infeasible/phase_2")
            self.status = "infeasible/phase_2"
            return

        if result == 0:
            if len(self.degeneracy_points) == 0:
                self.status = "optimal"
            else:
                self.status = "degenerate"

        if self.isMaximization:
            self.objective *= -1

    def __show_process_results(self, show_steps: bool = False) -> None:
        problem_value = self.objective @ self.variable_values[0:len(self.variables)]
        min_max_string = "max_text" if self.isMaximization else "min_text"
        min_max_string = LanguageUtils.get_translated_text(min_max_string)
        if show_steps:
            self.latexWriter.write(r"\subsection{"+LanguageUtils.get_translated_text("conclusion_text")+"}")
            if self.status == "optimal" or self.status == "degenerate":
                self.latexWriter.write(LanguageUtils.get_translated_text("optimal_solution_text"))
                self.latexWriter.write_column_identifiers(np.array(self.variable_values), self.__get_variables_list())
                self.latexWriter.write_vectors_with_identifiers(["x_b", "x_n"], [self.basis, self.non_basis])
                self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("numerical_solution_text", [min_max_string, LatexUtils.format_value(str(problem_value))]))
                if self.status == "degenerate":
                    degenerate_string = self.__get_degenerate_string()
                    self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("degenerate_solution_text", [degenerate_string, min_max_string]))
            elif self.status == "unbounded":
                self.latexWriter.write(LanguageUtils.get_translated_text("unbounded_solution_text"))
            elif self.status == "infeasible/phase_1":
                self.latexWriter.write(LanguageUtils.get_translated_text("infeasible/phase_1_text"))
            elif self.status == "infeasible/phase_2":
                self.latexWriter.write(LanguageUtils.get_translated_text("infeasible/phase_2_text"))

            if self.should_close:
                self.latexWriter.close()
        elif self.status == "optimal" or self.status == "degenerate":
            print(LanguageUtils.get_translated_text("optimal_solution_found"))
            print(LanguageUtils.get_translated_text("basic_variables_text"), self.basis)
            print(LanguageUtils.get_translated_text("values_text"), self.get_solution())
            print(f"{min_max_string} = {problem_value:.4f}")
            if self.status == "degenerate":
                LanguageUtils.print_translated("simple_degenerate_text")

    def __check_infeasibility_phase_two(self):
        any_negative_variable = any(var < 0 for var in self.variable_values)
        return any_negative_variable

    def get_solution(self) -> dict:
        variables_list = self.__get_variables_list()
        return {variables_list[i]: self.variable_values[i] for i in range(len(variables_list))}

    def __solver_loop(self, basic_matrix: np.ndarray[np.float64], basic_indexes: list[int],
                      non_basic_indexes: list[int], profit_vector: np.array(np.float64),
                      restrictions_vector: np.ndarray[np.float64], is_phase_one: bool, show_steps: bool = False) -> int:

        restrictions_vector = restrictions_vector.reshape(-1, 1)
        variables_list = self.__get_variables_list()
        phase_indicator = "phase_one_text" if is_phase_one else "phase_two_text"
        phase_indicator = LanguageUtils.get_translated_text(phase_indicator)

        while True:
            self.current_interaction += 1
            if self.current_interaction > 100:
                if show_steps:
                    self.latexWriter.write(LanguageUtils.get_translated_text("maximum_iterations_exceeded_text"))
                else:
                    self.__print_current_exercise_status("maximum_iterations_exceeded")
                self.status = "maximum_iterations_exceeded"
                return -3
            inv_b = np.linalg.inv(basic_matrix)

            x_b = inv_b @ restrictions_vector

            if show_steps:
                self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("iteration_text", [str(self.current_interaction), phase_indicator]))
                self.latexWriter.write(LanguageUtils.get_translated_text("current_status_text"))
                self.latexWriter.write_column_identifiers(np.array(self.variable_values), self.__get_variables_list())
                self.latexWriter.write_vectors_with_identifiers(["x_b", "x_n"], [self.basis, self.non_basis])
                self.latexWriter.write()
                self.latexWriter.write(r"\textbf{"+LanguageUtils.get_translated_text("step_1_text")+"}")

                # Paramos por aqui.
                self.latexWriter.write(LanguageUtils.get_translated_text("step_1_details"))
                self.latexWriter.write_matrix_equations("x_b", [inv_b, restrictions_vector], x_b)

            p_t = profit_vector[basic_indexes] @ inv_b


            c_r = profit_vector[non_basic_indexes] - p_t @ self.constraint_matrix[:, non_basic_indexes]

            if show_steps:
                self.latexWriter.write(r"\textbf{"+LanguageUtils.get_translated_text("step_2_text")+"}")
                self.latexWriter.write(LanguageUtils.get_translated_text("step_2_details"))
                self.latexWriter.write(r"\[ c_r = c_n - (c_b \cdot B^{-1}) \]")
                self.latexWriter.write_matrix_equations("c_r", [profit_vector[non_basic_indexes], "-", p_t, self.constraint_matrix[:, non_basic_indexes]], c_r)

            if show_steps:
                self.latexWriter.write(r"\textbf{"+LanguageUtils.get_translated_text("step_3_text")+"}") #step_3_text

            in_index = self.__get_negative_pivot(c_r, show_steps)
            if in_index == -1:
                if show_steps:
                    self.latexWriter.write(LanguageUtils.get_translated_text("no_negative_pivot_found_details"))
                return 0


            c_n = self.constraint_matrix[:, in_index].reshape(-1, 1)
            y = inv_b @ c_n

            if show_steps:
                self.latexWriter.write(r"\textbf{"+LanguageUtils.get_translated_text("step_4_text")+"}")
                self.latexWriter.write(LanguageUtils.get_translated_text("step_4_details"))
                self.latexWriter.write(r"\[ y =  B^{-1} \cdot A_n \]")
                self.latexWriter.write_matrix_equations("y", [inv_b, c_n], y)
                self.latexWriter.write(LanguageUtils.get_translated_text("step_4_variable_details"))


            if np.all(y <= 0):
                self.status = "unbounded"
                return -1

            ratios = np.full_like(y, np.inf)
            valid_indices = y > 0
            ratios[valid_indices] = x_b[valid_indices] / y[valid_indices]
            if show_steps:
                self.latexWriter.write(r"\textbf{"+LanguageUtils.get_translated_text("step_5_text")+"}")
                self.latexWriter.write(LanguageUtils.get_translated_text("step_5_details"))
                self.latexWriter.write_matrix_equations(r"\text{"+LanguageUtils.get_translated_text("step_5_formula_variable")+"}", [x_b, "/", y], ratios)

            out_index = self.__get_positive_pivot(ratios, show_steps)

            out_index_basic = basic_indexes[out_index]
            in_index_non_basic = non_basic_indexes[in_index]

            basic_indexes[out_index], non_basic_indexes[in_index] = self.__update_variable_values(basic_indexes, variables_list, x_b, y,
                                                                                        out_index, in_index_non_basic, out_index_basic)

            basic_matrix[:, out_index] = self.constraint_matrix[:, in_index_non_basic]

            if is_phase_one and not any(artificial_var in self.basis for artificial_var in self.artificial_variables):
                if show_steps:
                    self.latexWriter.write(r"\subsubsection{"+LanguageUtils.get_translated_text("phase_1_conclusion")+"}")
                    self.latexWriter.write(LanguageUtils.get_translated_text("phase_1_success_details"))
                    self.latexWriter.write_vectors_with_identifiers(["x_b", "x_n"], [self.basis, self.non_basis])
                return 0

    def __update_variable_values(self, basic_indexes, variables_list: list[str], x_b, y, out_index,
                                 in_index_non_basic, out_index_basic) -> (int, int):
        pivot_value = np.float64(x_b[out_index] / y[out_index])
        x_b -= pivot_value * y
        self.variable_values[in_index_non_basic] = pivot_value
        for i, basic_index in enumerate(basic_indexes):
                self.variable_values[basic_index] = np.float64(x_b[i])



        out_variable, in_variable = variables_list[out_index_basic], variables_list[in_index_non_basic]
        self.basis[self.basis.index(out_variable)] = in_variable
        self.non_basis[self.non_basis.index(in_variable)] = out_variable

        return in_index_non_basic, out_index_basic



    def __get_basic_matrix(self, basic_indexes: list[int]) -> np.ndarray[np.float64]:
        b = self.constraint_matrix[:, basic_indexes]
        return b

    def __get_basic_indexes(self) -> list[int]:
        variables_list = self.__get_variables_list()
        return [variables_list.index(var) for var in self.basis]

    def __get_non_basic_indexes(self) -> list[int]:
        variables_list = self.__get_variables_list()
        return [variables_list.index(var) for var in self.non_basis]

    def __get_negative_pivot(self, relative_costs: np.ndarray[np.float64], show_steps: bool = False) -> int:
        negative_indexes = np.where(relative_costs < 0)[0]
        if show_steps:
            self.latexWriter.write(LanguageUtils.get_translated_text("get_negative_pivot_details"))
            min_value_string = LatexUtils.format_numbers_vector(relative_costs)
            self.latexWriter.write(r"\textbf{"+LanguageUtils.get_translated_text_variable_text("get_negative_pivot_entering_element_details", [min_value_string])+"}", True) #get_negative_pivot_entering_element_details, [min_value_string]

        if negative_indexes.size == 0:
            return -1


        min_value = np.min(relative_costs[negative_indexes])
        options = np.where(relative_costs == min_value)[0].size
        if options > 1:
            self.degeneracy_points.append(self.current_interaction)

        min_index = negative_indexes[np.argmin(relative_costs[negative_indexes])]

        if show_steps:
            self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("get_negative_pivot_element_index_text", [str(min_index+1), LatexUtils.format_string_vector(self.non_basis)]))
            self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("get_negative_pivot_chosen_element_text", [ LatexUtils.format_variable( self.non_basis[min_index] ) ]))
            if options > 1:
                self.latexWriter.write(LanguageUtils.get_translated_text("get_negative_pivot_degeneracy")) #get_negative_pivot_degeneracy

        return int(min_index)

    def __get_positive_pivot(self, ratios: np.array(np.float64), show_steps: bool = False) -> int:
        positive_indexes = np.where(ratios >= 0)[0]

        if positive_indexes.size == 0:
            return -1

        min_value = np.min(ratios[positive_indexes])
        options = np.where(ratios == min_value)[0].size
        if options > 1 and self.current_interaction not in self.degeneracy_points:
            self.degeneracy_points.append(self.current_interaction)

        min_index = positive_indexes[np.argmin(ratios[positive_indexes])]
        if show_steps:
            min_value_string = LatexUtils.format_numbers_vector(ratios.reshape(-1, 1)[:, 0])
            self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("get_positive_pivot_leaving_element_details", [min_value_string]), True)
            self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("get_positive_pivot_element_index_text", [str(min_index + 1), LatexUtils.format_string_vector(self.basis)]))
            self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("get_positive_pivot_chosen_element_text", [LatexUtils.format_variable(self.basis[min_index])]), True)
            if options > 1:
                self.latexWriter.write(LanguageUtils.get_translated_text("get_positive_pivot_degeneracy"))

        return int(min_index)

    def __standardize_problem(self, show_steps: bool = False) -> None:
        self.artificial_variables = []
        self.slack_variables = []

        num_restrictions = len(self.restriction_symbols)
        artificial_lines = []
        slack_lines = []

        if show_steps:
            self.latexWriter.write(r"\subsection{"+LanguageUtils.get_translated_text("problem_standardization_text")+"}") #problem_standardization_text
            self.latexWriter.write(LanguageUtils.get_translated_text("problem_standardization_details"))
            self.latexWriter.write(r"\begin{itemize}")
            self.latexWriter.write(r"\item " + LanguageUtils.get_translated_text("problem_standardization_lt")) #problem_standardization_lt
            self.latexWriter.write(r"\item " + LanguageUtils.get_translated_text("problem_standardization_eq"))
            self.latexWriter.write(r"\item " + LanguageUtils.get_translated_text("problem_standardization_gt"))
            self.latexWriter.write(r"\end{itemize}")

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

        if show_steps:
            self.latexWriter.write(LanguageUtils.get_translated_text("problem_standardization_after")) #problem_standardization_after
            variables_list = self.__get_variables_list()
            self.latexWriter.write_column_identifiers(self.constraint_matrix, variables_list)
            self.latexWriter.write(LanguageUtils.get_translated_text("problem_standardization_result")) #problem_standardization_result
            self.__write_current_problem()

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

    def __get_variables_list(self) -> list[str]:
        return self.variables + self.slack_variables + self.artificial_variables

    def __get_degenerate_string(self) -> str:
        degenerate_string = ""
        for i in range(len(self.degeneracy_points)):
            degenerate_string += str(self.degeneracy_points[i])
            if (i + 1) < len(self.degeneracy_points):
                degenerate_string += ","
        return degenerate_string

    def __set_next_exercise(self):
        self.latexWriter.write("\n\n"+r"\newpage", True)
        self.__exercise_number+=1

    def __print_current_exercise_status(self, status:str) -> None:
        cur_exercise = LanguageUtils.get_translated_text_variable_text("exercise_text",[str(self.__exercise_number)]) + ":"
        print(cur_exercise)
        LanguageUtils.print_translated(status)

    def __write_current_problem(self):
        variables_list = self.__get_variables_list()
        restrictions_symbols = self.restriction_symbols
        if len(self.slack_variables) > 0 or len(self.artificial_variables) > 0:
            restrictions_symbols = ["="]*len(variables_list)
        problem_text = LatexUtils.format_problem_to_latex(self.objective, self.constraint_matrix, variables_list,
                                                          self.restrictions, restrictions_symbols,
                                                          self.isMaximization)
        self.latexWriter.write(problem_text)

class RevisedSimplexWithoutFile(RevisedSimplex):
    def __init__(self, objective_function: np.array(np.float64), constraint_matrix: np.ndarray[np.float64],
                 is_maximization: bool, restrictions: np.array(np.float64), restrictions_symbols: list[str]):
        self.variables = [f"x{i+1}" for i in range(len(objective_function))]
        self.constraint_matrix = constraint_matrix
        self.isMaximization = is_maximization
        self.objective = objective_function
        self.restrictions = restrictions
        self.restriction_symbols = restrictions_symbols
        self._setup_without_data()
        super().__init__()
