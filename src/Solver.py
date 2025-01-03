"""
@file Solver.py
@brief Implementa o método Simplex Revisado para resolver problemas de otimização linear.
@details Este arquivo contém a implementação principal da classe RevisedSimplex para resolução
de problemas de otimização linear, suportando:
- Entrada de dados via arquivo ou manual,
- Exportação dos resultados para LaTeX,
- Resolução em duas fases (remoção de variáveis artificiais e busca da solução ótima).

@author Matheus Silveira Feitosa - NUSP: 11836692
@date 10/01/2025
"""

import numpy as np

from src.LatexWriter import LatexWriter
from src.Parser import FileParser
from src.Utils import LatexUtils, LanguageUtils


class RevisedSimplex:
    """
    @class RevisedSimplex
    @brief Classe para resolver problemas de programação linear com o Simplex Revisado.

    @details
    Esta classe lida com as principais etapas do algoritmo Simplex Revisado:
    - Padronização do problema (adição de variáveis de folga ou artificiais),
    - Fase 1: Remoção de variáveis artificiais,
    - Fase 2: Busca pela solução ótima.
    Também permite a exportação dos resultados em LaTeX para facilitar relatórios e análises.

    @note
    Esta classe é dependente do fornecimento de um arquivo com os dados do problema.
    """
    def __init__(self, file:str = "", show_steps: bool = False, latex_writer: LatexWriter = None) -> None:
        """
        @brief Construtor da classe RevisedSimplex.

        @param file Nome do arquivo que contém os dados do problema de otimização linear.
        O padrão é uma string vazia (não utiliza arquivo).
        @param show_steps Indica se os passos intermediários do processo devem ser exibidos no LaTeX.
        @param latex_writer Instância de LatexWriter para gerar a saída em LaTeX. Opcional caso mais de um problema vá ser resolvido.

        @details
        Este construtor inicializa e configura a classe RevisedSimplex. Ele pode usar informações de um arquivo
        ou ser configurado manualmente através de sua classe filha para resolver problemas lineares passados através de uma matriz.

        @see RevisedSimplexWithoutFile
        """
        self.__exercise_number = 1
        if not file == "":
            self._load_problem_data(file)
        if latex_writer is None:
            self._setup_support_variables()
            if show_steps:
                self.should_close = True
                self.latexWriter = LatexWriter(file.split("/")[-1].split(".")[0])
        else:
            self.should_close = False
            self.latexWriter = latex_writer


    def _load_problem_data(self, file:str) -> None:
        """
        @brief Carrega os dados do problema de um arquivo.

        @param file Caminho para o arquivo contendo os dados do problema linear.

        @details
        Os dados são lidos e processados utilizando o `FileParser`. Após a leitura,
        as informações são configuradas nos atributos da classe, como variáveis, matriz de restrição e função objetivo
        por uma outra função auxiliar.
        """
        data = FileParser(file).parse_file()
        self.__setup_from_data(data)

    def _setup_support_variables(self) -> None:
        """
            @brief Configura variáveis de suporte internas para o problema carregado.

            @details
            Esta função inicializa e define várias variáveis necessárias para resolver o problema:
            - `variable_values` para armazenar os valores das variáveis,
            - `slack_variables` e `artificial_variables` para rastrear as variáveis introduzidas na padronização,
            - `status` para indicar o estado atual do problema, e qual a condição da solução,
            - `degeneracy_points` para lidar com casos degenerados durante o Simplex e indicar em quais iterações eles aconteceram.

            @warning Deve ser chamado após o problema ter sido carregado, caso contrário, as variáveis dependentes do problema não serão configuradas corretamente.
        """
        self.variable_values = [0 for _ in self.variables]
        self.slack_variables = []
        self.artificial_variables = []
        self.status = None  # Ideia vinda do scipy pra organizar melhor qual a conclusão do simplex.
        self.degeneracy_points = []
        self.current_interaction = 0

    def __setup_from_data(self, data) -> None:
        """
            @brief Define os dados do problema com base nas informações fornecidas.

            @param data Um dicionário contendo os seguintes elementos:
                - `lp_variables`: Lista com os nomes das variáveis de decisão,
                - `constraint_matrix`: Matriz de restrições (A),
                - `is_maximization`: Booleano que indica se o problema é de maximização,
                - `objective_function`: Vetor da função objetivo (c),
                - `restrictions_vector`: Vetor das restrições (b),
                - `symbols`: Lista de símbolos das restrições (≤, =, ≥).

            @details
            Esse método inicializa os dados principais do problema (variáveis, matriz de restrições, função objetivo, etc.)
            com base no dicionário resultante do parser de arquivo passado anteriormente.

            @warning Só deve ser usado após ter dados carregados no Parser
        """
        self.variables = data["lp_variables"]
        self.constraint_matrix = data["constraint_matrix"]
        self.isMaximization = data["is_maximization"]
        self.objective = data["objective_function"]
        self.restrictions = data["restrictions_vector"]
        self.restriction_symbols = data["symbols"]

    def reload_problem(self, file: str) -> None:
        """
            @brief Recarrega os dados de um novo problema a partir de um arquivo.

            @param file O caminho para o arquivo contendo os dados do novo problema.

            @details
            Este método lê um novo problema do arquivo fornecido e redefine as variáveis configuradas
            para que o algoritmo possa ser executado novamente.

            @note
            Usado especialmente para quando queremos escrever várias soluções num mesmo arquivo.
        """
        data = FileParser(file).parse_file()
        self.__setup_from_data(data)
        self._setup_support_variables()

    def solve(self, show_steps: bool = False):
        """
        @brief Resolve o problema de programação linear carregado.

        @param show_steps Exibe os passos do algoritmo em LaTeX, se definido como True.

        @details
        Executa cada etapa do algoritmo do Simplex Revisado, de forma sequencial:
        - Padroniza o problema com variáveis artificiais e de folga,
        - Resolve a Fase 1 para remoção de variáveis artificiais,
        - Resolve a Fase 2 para obter a solução ótima.

        @note
        A solução final ou mensagens de erro (problema inviável ou ilimitado) são impressas
        ou registradas no arquivo gerado em LaTeX.
        """
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
        if self.status != "infeasible/phase_1" and not "unbounded" in str(self.status):
            self.__solve_phase_two(from_phase_one, show_steps)

        self.__show_process_results(show_steps)

    def __get_initial_artificial_basis(self) -> list[str]:
        """
            @brief Obtém a base inicial com variáveis artificiais para a Fase 1.

            @return Uma lista contendo a base factível inicial do problema para a Fase 1.

            @details
            Durante a Fase 1, as variáveis artificiais são inseridas na base inicial para resolver o problema.
            Este método retorna a base inicial factível com base na matriz de restrições fornecida
            A ordem das linhas e adições de variável de folga e artificial é respeitada durante a construção.
        """
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
        """
            @brief Obtém o conjunto de variáveis não basicas inicial complementando a base inicial.

            @param initial_basis Lista contendo o conjunto de variáveis básicas inicial.
            @return Lista com as variáveis que não estão na base factível inicial.

            @details
            As variáveis que não estão na base inicial factível são classificadas como não básicas no início do algoritmo.
            Esse método retorna essas variáveis com base nas variáveis básicas para ser usado em iterações posteriores.

            @warning Deve ser executado após obter a base inicial.
            @see __get_initial_artificial_basis
        """
        initial_non_basis = []
        possible_variables = self.variables + self.slack_variables+self.artificial_variables
        for i in (range(len(possible_variables))):
            if possible_variables[i] not in initial_basis:
                initial_non_basis.append(possible_variables[i])
        return initial_non_basis



    def __solve_phase_one(self, show_steps: bool = False) -> int:
        """
            @brief Resolve a Fase 1 do Simplex Revisado para remover as variáveis artificiais acrescentadas na padronização do problema.

            @param show_steps Exibe os detalhes da resolução passo a passo no LaTeX, se `True`.
            @return Retorna:
                - `0` se a Fase 1 for concluída com sucesso,
                - `-1` se a fase 1 não foi necessária, ou não pode ser concluida.

            @details
            Na Fase 1, o algoritmo tenta remover as variáveis artificiais da base procurando por uma solução factível
            e em seguida, verificar se o problema é viável.
            Caso ele não seja, o status do problema é atualizado para "inviável" ou para "ilimitado".
        """
        if len(self.artificial_variables) < 1:
            return -1
        
        artificial_costs = np.zeros(len(self.variables) + len(self.slack_variables) + len(self.artificial_variables))
        artificial_costs[-len(self.artificial_variables):] = 1

        if show_steps:
            self.latexWriter.break_page()
            self.latexWriter.write("\subsection{"+LanguageUtils.get_translated_text("phase_one_text")+":}") #Phase_one_text
            self.latexWriter.write(LanguageUtils.get_translated_text("artificial_variables_removal"))
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
                self.__print_current_exercise_status("summarized/infeasible/phase_1_text")
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
        """
            @brief Verifica a inviabilidade do problema durante a Fase 1.

            @return Retorna `True` se o problema for inviável, `False` caso contrário.

            @details
            Esse método analisa se ainda há variáveis artificiais na base ou
            se algum valores dessas variáveis é diferente de 0.
            Se ambas as condições não forem satisfeitas, então o problema é viável e procedemos para a segunda fase.
        """
        any_artificial_remaining = any(basic_var in self.artificial_variables for basic_var in self.basis)
        any_negative_artificial = any(artificial_value != 0 for artificial_value in self.variable_values[-len(self.artificial_variables):])
        return any_artificial_remaining or any_negative_artificial

    def __solve_phase_two(self, from_phase_one: bool, show_steps: bool = False) -> None:
        """
            @brief Resolve a Fase 2 do Simplex Revisado para encontrar a solução ótima.

            @param from_phase_one Indica se a Fase 1 ocorreu anteriormente, influenciando na escolha da base.
            @param show_steps Exibe os detalhes das operações no LaTeX, se `True`.

            @details
            Durante a Fase 2, o método busca encontrar a solução ótima do problema, para além de
            durante o processo, verificar a inviabilidade, ou ilimitabilidade do problema.
        """
        if show_steps:
            self.latexWriter.break_page()
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
                self.__print_current_exercise_status("summarized/infeasible/phase_2_text")
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
        """
            @brief Exibe ou salva os resultados finais do problema.

            @param show_steps Indica se os detalhes devem ser incluídos no LaTeX.

            @details
            Baseado no status final do problema (solução ótima, degenerada, inviável ou ilimitado),
            este método também apresentará a solução numérica do problema
            de forma detalhada ou simplificada a depender do lugar onde este estiver escrevendo.
        """
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
        elif self.status == "unbounded":
            self.__print_current_exercise_status("summarized_unbounded_text")

    def __check_infeasibility_phase_two(self):
        """
            @brief Verifica a inviabilidade do problema ao final da Fase 2.

            @return Retorna `True` se o problema for inviável, `False` caso contrário.

            @details
            Esse método analisa se alguma variável possui valores negativos.
            Caso não possua, então o problema é viável e procedemos para a elucidação dos resultados.
        """
        any_negative_variable = any(var < 0 for var in self.variable_values)
        return any_negative_variable

    def get_solution(self) -> dict:
        """
            @brief Retorna a solução das variáveis do problema.

            @return Um dicionário onde as chaves são os nomes das variáveis e os valores
                    correspondem à solução encontrada para cada uma delas.

            @details
            Esse método formata o resultado final do problema, associando os nomes das variáveis
            a seus valores obtidos na solução ótima ou degenerada de forma a facilitar
            sua representação.
        """
        variables_list = self.__get_variables_list()
        return {variables_list[i]: self.variable_values[i] for i in range(len(variables_list))}

    def __solver_loop(self, basic_matrix: np.ndarray[np.float64], basic_indexes: list[int],
                      non_basic_indexes: list[int], profit_vector: np.array(np.float64),
                      restrictions_vector: np.ndarray[np.float64], is_phase_one: bool, show_steps: bool = False) -> int:
        """
        @brief Realiza as iterações do Simplex até alcançar a solução ótima, ou até que as variáveis artificiais
                sejam removidas para o caso da Fase 1.

        @param basic_matrix Matriz básica (B) na iteração atual.
        @param basic_indexes Lista com os índices das variáveis básicas. (Com respeito a lista de todas as variáveis do problema)
        @param non_basic_indexes Lista com os índices das variáveis não básicas. (Com respeito a lista de todas as variáveis do problema)
        @param profit_vector Vetor de lucros (c).
        @param restrictions_vector Vetor de restrições (b).
        @param is_phase_one Define se a iteração faz parte da Fase 1.
        @param show_steps Exibe os passos em um arquivo LaTeX, se `True`.

        @return Indica o estado final do algoritmo:
            - `0`: Solução ótima alcançada,
            - `-1`: Problema ilimitado,
            - `-3`: Iteração máxima excedida.

        @details
        Este método realiza os cálculos centrais do algoritmo Simplex, incluindo:
        1. Solução básica (x_b),
        2. Cálculo dos custos reduzidos,
        3. Seleção de pivôs (tanto de entrada quanto de saída),
        4. Atualizações da base e das matrizes com base nos pivôs selecionados.

        @note Este método é uma implementação genérica para ambas as fases do Simplex, sendo aproveitado pro ambas.
        A ideia principal é garantir que, ao analisar o código, seja notado que a diferença entre cada fase,
        é apenas com respeito a condição de parada e condição inicial do problema, mas o intermédio é o mesmo.

        Esse seria o equivalente ao chamado "Coração do simplex" de acordo com os autores do SciPy.
        """
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
                    self.__print_current_exercise_status("maximum_iterations_exceeded_text")
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
                return 0

    def __update_variable_values(self, basic_indexes, variables_list: list[str], x_b, y, out_index,
                                 in_index_non_basic, out_index_basic) -> (int, int):
        """
            @brief Atualiza os valores das variáveis básicas e não básicas após pivotar.

            @param basic_indexes Índices das variáveis que compõem a matriz básica (B).
            @param variables_list Lista geral com os nomes das variáveis do problema.
                    # Provavelmente este aqui não precisaria ser passado através da função...

            @param x_b Vetor de soluções básicas atuais.
            @param y Vetor direção para o cálculo da variável pivotada.
            @param out_index Índice da variável básica com respeito a lista de variáveis básicas, e não de variáveis globais.
            @param in_index_non_basic Índice da variável não básica que entrará na base.
            @param out_index_basic Índice da variável básica que sairá da base.

            @return Uma tupla `(in_index_non_basic, out_index_basic)` após trocar os valores.
            (Utilizado posteriormente para atualizar as posições da matriz básica de forma mais eficiente)

            @details
            Atualiza os valores das variáveis e realiza a troca entre variáveis básicas e não
            básicas, conforme indicado pelos pivôs calculados em iterações anteriores.
        """

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
        """
            @brief Obtém a matriz das variáveis básicas usando os índices fornecidos.

            @param basic_indexes Lista com os índices das variáveis básicas na matriz de restrições.
            @return A matriz de restrições apenas com as colunas correspondentes as variáveis básicas.

            @details
            Usa os índices passados para selecionar as colunas da matriz de restrições
            que correspondem às variáveis atuais da base.
        """
        b = self.constraint_matrix[:, basic_indexes]
        return b

    def __get_basic_indexes(self) -> list[int]:
        """
            @brief Retorna os índices das variáveis básicas no problema.

            @return Uma lista de índices das variáveis que compõem a base atual na
                    lista de todas as variáveis do problema.

            @details
            Esse método acessa a lista de variáveis básicas e retorna os respectivos índices consoante
            à lista concatenada de todas as variáveis do problema.

            @note Utilizada na obtenção da matriz básica em cada iteração.
        """
        variables_list = self.__get_variables_list()
        return [variables_list.index(var) for var in self.basis]

    def __get_non_basic_indexes(self) -> list[int]:
        """
            @brief Retorna os índices das variáveis não básicas no problema.

            @return Uma lista de índices das variáveis que não compõem a base atual na
                    lista de todas as variáveis do problema.

            @details
            Funciona de forma similar a `__get_basic_indexes`, mas acessa diretamente
            as variáveis classificadas como não básicas e retorna seus índices.

            @note Utilizada no calculo dos custos reduzidos em cada iteração.
        """
        variables_list = self.__get_variables_list()
        return [variables_list.index(var) for var in self.non_basis]

    def __get_negative_pivot(self, reduced_costs: np.ndarray[np.float64], show_steps: bool = False) -> int:
        """
            @brief Determina o índice da variável que entrará na base (pivô de entrada).

            @param reduced_costs Um vetor contendo os custos reduzidos das variáveis não básicas.
            @param show_steps Booleano que indica se os detalhes do processo serão escritos no LaTeX.

            @return Retorna o índice da variável não básica com menor custo reduzido (menor valor negativo):
                - Índice inteiro do pivô escolhido,
                - `-1` se não houver valores negativos (indica que a solução é ótima).

            @details
            Identifica a variável que entrará na base ao procurar o menor valor negativo em
            `reduced_costs`. Este valor define a direção de melhoria para o custo da função objetivo.
            1. Valores negativos em `reduced_costs` indicam possíveis melhorias no custo.
            2. O pivô é selecionado com base no menor custo reduzido negativo.
            3. Se houver múltiplos candidatos com o mesmo valor, o método detecta
            degeneração, e registra a iteração em que ocorreu.
        """
        negative_indexes = np.where(reduced_costs < 0)[0]
        if show_steps:
            self.latexWriter.write(LanguageUtils.get_translated_text("get_negative_pivot_details"))
            min_value_string = LatexUtils.format_numbers_vector(reduced_costs)
            self.latexWriter.write(r"\textbf{"+LanguageUtils.get_translated_text_variable_text("get_negative_pivot_entering_element_details", [min_value_string])+"}", True) #get_negative_pivot_entering_element_details, [min_value_string]

        if negative_indexes.size == 0:
            return -1


        min_value = np.min(reduced_costs[negative_indexes])
        options = np.where(reduced_costs == min_value)[0].size
        if options > 1:
            self.degeneracy_points.append(self.current_interaction)

        min_index = negative_indexes[np.argmin(reduced_costs[negative_indexes])]

        if show_steps:
            self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("get_negative_pivot_element_index_text", [str(min_index+1), LatexUtils.format_string_vector(self.non_basis)]))
            self.latexWriter.write(LanguageUtils.get_translated_text_variable_text("get_negative_pivot_chosen_element_text", [ LatexUtils.format_variable( self.non_basis[min_index] ) ]))
            if options > 1:
                self.latexWriter.write(LanguageUtils.get_translated_text("get_negative_pivot_degeneracy")) #get_negative_pivot_degeneracy

        return int(min_index)

    def __get_positive_pivot(self, ratios: np.array(np.float64), show_steps: bool = False) -> int:
        """
            @brief Determina o índice da variável que sairá da base (pivô de saída).

            @param ratios Um vetor contendo os coeficientes das razões entre as variáveis básicas (`x_b`)
            e os valores correspondentes em `y`.

            @param show_steps Booleano que indica se os detalhes do método serão escritos no LaTeX.

            @return Retorna o índice da variável básica que será removida da base:
                - Índice inteiro do pivô escolhido para sair,
                - `-1` se não houver índices válidos (indica problema ilimitado).

            @details
            Este método calcula o pivô de saída seguindo o critério da razão mínima,
            onde as razões `x_b / y` são analisadas. Apenas valores positivos em `y` são
            considerados:
            1. O menor valor da razão determina o pivô que sairá.
            2. Em casos onde há múltiplos mínimos, a degeneração é identificada
            para que seja rastreada durante o processo.
        """
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
        """
        @brief Padroniza o problema para o formato compatível com o método Simplex.

        @param show_steps Exibe o detalhamento das alterações no LaTeX, se True.

        @details
        - Adiciona variáveis de folga para equações '≤',
        - Adiciona variáveis artificiais para equações '=' ou '≥',
        - Atualiza a matriz de restrição (A) e os vetores de variáveis.
        O algoritmo realiza essas alterações para transformar o problema em sua forma padrão.

        @note Este método é chamado internamente antes de resolver o problema para colocá-lo na forma padrão.
        """

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
        """
            @brief Adiciona uma nova variável (folga ou artificial) à matriz de restrições.

            @param line_to_add Índice da linha onde a variável deve ser adicionada.
            @param value O valor do multiplicador da variável na matriz (1 para folga ou -1 caso uma variável artificial esteja presente).

            @details
            Este método modifica a matriz de restrições (A) e ajusta o vetor de variáveis com
            a adição de novas colunas representando as variáveis introduzidas na padronização.

            @note Este método é uma etapa necessária durante a padronização do problema.
        """
        col = np.zeros((len(self.restriction_symbols), 1))
        col[line_to_add, 0] = value
        self.constraint_matrix = np.hstack((self.constraint_matrix, col))
        self.__add_variable_value_to_vector(line_to_add, value)

    def __add_variable_value_to_vector(self, line_to_add: int, value: int) -> None:
        """
            @brief Adiciona o valor inicial de uma variável no vetor de valores das variáveis.

            @param line_to_add Linha de dada variável na matriz de restrições.
            @param value Multiplicador específico para a variável adicionada.

            @details
            Esse método ajusta os valores iniciais do vetor de variáveis com base na
            linha da matriz de restrições onde a nova variável foi introduzida.

            - Se a variável é uma variável de folga mas com multiplicador (`-1`),
              o valor é automaticamente ajustado como `0`.
            - Caso contrário, usa o valor correspondente multiplicador no vetor de restrições (`1` geralmente).

            @note Essa função é usada durante a inicialização das variáveis no problema padronizado.
        """

        restriction_value = self.restrictions[line_to_add]
        if value==-1:
            self.variable_values.append(0)
        else:
            self.variable_values.append(restriction_value)

    def __remove_artificial_variables(self):
        """
        @brief Remove as variáveis artificiais de todos os lugares do problema

        @details
        Este método só é executado após a conclusão bem sucedida da Fase 1, garantindo que
        as variáveis artificiais não sejam consideradas durante a Fase 2
        para além de facilitar a visualização e elucidação da Fase 2 como seria feito manualmente.

        @note Deve ser chamado APENAS após a finalização da Fase 1 bem sucedida da Fase 1.
        """
        for i in range(len(self.artificial_variables)):
            self.variable_values.pop()
            self.non_basis.remove(self.artificial_variables[i])
            self.artificial_variables.pop()

    def __get_variables_list(self) -> list[str]:
        """
            @brief Retorna a lista completa de variáveis no problema.

            @return Uma lista contendo os nomes das variáveis originais, de folga e artificiais,
            nesta exata ordem de concatenação.
        """
        return self.variables + self.slack_variables + self.artificial_variables

    def __get_degenerate_string(self) -> str:
        """
            @brief Retorna uma string representando os pontos de degeneração ocorridos durante o processo separados por vírgula.

            @return Uma string contendo os índices das interações que resultaram em degeneração.

            @details
            O método constrói uma string formatada que lista, por iteração, os pontos
            onde a degeneração foi identificada. Usado especialmente para apresentar
            os pontos onde diferentes escolhas poderiam ser tomadas para resolver o problema.

            @warning Deve ser usado somente após uma iteração com degeneração.
        """
        degenerate_string = ""
        for i in range(len(self.degeneracy_points)):
            degenerate_string += str(self.degeneracy_points[i])
            if (i + 1) < len(self.degeneracy_points):
                degenerate_string += ","
        return degenerate_string

    def set_next_exercise(self):
        """
            @brief Configura o documento latex e o solver para resolver outro problema.

            @details Incrementa o contador de exercícios em 1, e adiciona uma quebra de linha ao
            documento LaTeX para separar cada exercício resolvido.
        """
        self.latexWriter.break_page()
        self.__exercise_number+=1

    def __print_current_exercise_status(self, status:str) -> None:
        """
        @brief Identifica o exercício e imprime o status da tela.

        @param status identificador do erro ou da conclusão obtida durante a execução do algoritmo.

        @details
        Imprime de forma simplificada o identificador do exercício atual,
        e faz um leve detalhamento do seu status atual.
        """
        cur_exercise = LanguageUtils.get_translated_text_variable_text("exercise_text",[str(self.__exercise_number)]) + ":"
        print(cur_exercise)
        LanguageUtils.print_translated(status)

    def __write_current_problem(self):
        """
            @brief Escreve no documento em Latex, o problema formatado.

            @details
            O método reconstrói o problema através dos dados fornecidos pelo Parser.
            de forma a adaptar sua estrutura para uma forma mais facilmente visível.
            E de forma a destacar as mudanças antes da padronização e após padronização.
        """
        variables_list = self.__get_variables_list()
        restrictions_symbols = self.restriction_symbols
        if len(self.slack_variables) > 0 or len(self.artificial_variables) > 0:
            restrictions_symbols = ["="]*len(variables_list)
        problem_text = LatexUtils.format_problem_to_latex(self.objective, self.constraint_matrix, variables_list,
                                                          self.restrictions, restrictions_symbols,
                                                          self.isMaximization)
        self.latexWriter.write(problem_text)

class RevisedSimplexWithoutFile(RevisedSimplex):
    """
    @class RevisedSimplexWithoutFile
    @brief Uma subclasse derivada de `RevisedSimplex` que fornece suporte para problemas manuais.
            #Provavelmente é a que será usada para a correção do EP...

    @details
    Permite inicializar e resolver problemas de programação linear sem fornecer um arquivo,
    aceitando diretamente como entrada a matriz de restrições, a função objetivo e os sinais das restrições.

    @note
    Os dados devem ser passados diretamente ao construtor dessa classe, que irá tratá-los
    da mesma forma que na implementação base de forma similar a como é feito no scipy.
    """

    def __init__(self, objective_function: np.array(np.float64), constraint_matrix: np.ndarray[np.float64],
                 is_maximization: bool, restrictions: np.array(np.float64), restrictions_symbols: list[str] = None):
        """
            @brief Inicializa um problema linear diretamente a partir dos parâmetros fornecidos sem depender de arquivos.

            @param objective_function Array representando o vetor da função objetivo.
            @param constraint_matrix Matriz de restrições do problema.
            @param is_maximization Booleano que indica se o problema é de maximização.
            @param restrictions Vetor das restrições.
            @param restrictions_symbols Lista de símbolos das restrições (≤, =, ≥).
                    #todo: Talvez tornar isto independente da lista de simbolos e só assumir que tudo é do tipo ≤

            @details
            Configura diretamente as variáveis e a matriz de restrições, utilizando o mesmo
            algoritmo de base para executar o método Simplex. As variáveis são automaticamente
            nominais na forma `x_1, x_2, ...` para simplificar a visualização.
        """
        self.variables = [f"x{i+1}" for i in range(len(objective_function))]
        self.constraint_matrix = constraint_matrix
        self.isMaximization = is_maximization
        self.objective = objective_function
        self.restrictions = restrictions
        if restrictions_symbols is not None:
            self.restriction_symbols = restrictions_symbols
        else:
            self.restriction_symbols = ["<="]*len(self.variables)
        self._setup_support_variables()
        super().__init__()
