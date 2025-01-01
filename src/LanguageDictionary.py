class LanguageDictionary:
    PORTUGUESE_DICTIONARY = {
        "pt": "Português Brasileiro",
        "en": "Inglês",
        "es": "Espanhol",
        "return_to_main_menu": "Voltar ao menu principal",
        "solve_one": "Resolver um problema de Otimização Linear",
        "solve_all": "Resolver todos os problemas de Otimização Linear disponíveis",
        "no_files": "Nenhum arquivo disponível para resolver.",
        "directory_not_exists": "O diretório especificado não existe.",
        "no_file_error": "Erro: Nenhum arquivo foi encontrado.",
        "select_file_intro": "Por favor, selecione o arquivo que deseja resolver: ",
        "select_file_options": "Digite o número correspondente ao arquivo: ",
        "show_steps": "Deseja visualizar os passos da resolução? (s/n): ",
        "exit_state": "Encerrando o programa...",
        "main_menu": "Selecione uma opção",
        "number_to_do": "Escolha o número correspondente ao que deseja fazer: ",
        "language_menu": "Escolha um idioma",
        "language_options": "Escolha o número correspondente ao idioma: ",
        "invalid_state": "Não é um menu válido.",
        "invalid_choice": "Escolha inválida. Por favor, selecione um número entre 1 e",
        "invalid_option_error": "Erro: Entrada inválida. Por favor, insira um número válido.",

        "exercise_text": "Exercício: <x1>",
        "initial_problem_description": "O problema de otimização linear pode ser descrito pelas seguintes matrizes e vetores:",
        "restriction_matrix_text": "Matriz de restrições",
        "cost_vector_text": "Vetor de custo",
        "restriction_vector_text": "Vetor de restrições",
        "cost_change_max_text": "Considerando termos um problema de maximização, multiplicamos o vetor de custos por $-1$, obtendo:",
        "phase_one_text": "Fase 1",
        "phase_two_text": "Fase 2",
        "artificial_variables_removal": "Antes de continuar, precisamos nos livrar das variáveis artificiais, e para isso, resolvemos o problema auxiliar de forma a obter uma base sem as variáveis artificiais",
        "artificial_variables_cost": "Com esse objetivo, redefinimos o vetor de custos redefinindo o custo de todos as variáveis para zero, com exceção das variáveis artificiais que agora são custo 1",
        "initial_basic_non_basic_definition": "Começamos definindo nossas variáveis básicas e não básicas por $x_b$ e $x_n$, seguindo a lógica de:",
        "artificial_basis_definition": "Se a linha da matriz possui uma variável artificial, então adicionamos a variável artificial ao conjunto de variáveis básicas, e a variável de folga no conjunto das não básicas",
        "following_bases_text": "Fazendo isso, encontramos as seguintes bases:",

        "infeasible/phase_1_text": "Ao finalizarmos o processo da fase 1, não foi possível remover as variáveis artificiais, com isso, como não há uma solução sem elas, logo podemos concluir que o problema é inviável.",
        "infeasible/phase_2_text": "A solução ótima encontrada possui valores negativos para as variáveis, com isto, podemos concluir que o problema é inviável.",
        "phase_1_success_text": "Com isso, concluimos a fase 1, e obtemos a seguinte base inicial e com os seguintes valores:",
        "phase_1_success_details": "Como conseguimos remover todas as variáveis artificiais da base, concluímos a fase 1. A base atual é:",
        "phase_1_next_step": "Agora, podemos remover as variáveis artificiais do problema e resolver o problema original.",
        "phase_1_skip": "Como não passamos pela fase um, definimos nossas variáveis básicas como sendo as variáveis de folga.",
        "phase_2_direct": "E nossas variáveis não básicas como sendo as variáveis originais do problema, com tal definição, escrevemos:",
        "from_phase_1": "Como viemos da fase 1, então para continuar com a resolução do problema na fase 2, partiremos da solução encontrada na fase 1 definida por:",
        "max_text": "Máximo",
        "min_text": "Mínimo",
        "conclusion_text": "Conclusão",
        "optimal_solution_text": "Com isso, concluimos a fase 2, e obtemos a solução ótima abaixo:",
        "unbounded_solution_text": "Como vimos que na última iteração do Simplex, todos os valores de $y$ eram negativos, conclúimos que a variável não básica que estará entrando poderá crescer indefinidamente, e portanto, teremos uma solução ilimitada.",
        "numerical_solution_text": "Podemos calcular a solução correspondente ao <x1>, multiplicando os valores das variáveis, pelo vetor de custo, e obtemos que o resultado ótimo atingível do problema é <x1> = $<x2>$",
        "degenerate_solution": "Observe que a solução é degenerada, isto é, se tivéssemos tomado escolhas diferentes nas iterações <x1>, de forma a obtermos o mesmo resultado <x2>, mas com outro conjunto de variáveis básicas.",
        "maximum_iterations_exceeded_text": "Erro: Número máximo de interações atingido",
        "iteration_text": "Iteração <x1> (<x2>)",
        "current_status_text": "Estado atual do problema:",
        "step_1_text": "Passo 1: Cálculo do vetor básico ($x_b$)",
        "step_1_details": "Invertemos a matriz básica e multiplicamos pelo vetor de restrições:",
        "step_2_text:": "Passo 2: Cálculo dos custos reduzidos ($c_r$)",
        "step_2_details": "O vetor de custos reduzidos é calculado como:",
        "step_3_text": "Passo 3: Escolha da variável que entra na base",
        "no_negative_pivot_found_details": "Como não temos nenhum candidato a entrar na base de forma a melhorar a solução, concluimos o processo.",
        "step_4_text": "Passo 4: Calculo do vetor direção $y$",
        "step_4_details": "O vetor $y$ é calculado como:",
        "step_4_variable_details": "$A_n$ é o vetor coluna das restrições da variável que irá entrar na base.",
        "step_5_text": "Passo 5: Escolha da variável que sai da base",
        "step_5_details": r"Primeiro, calculamos as razões $\frac{x_b}{y}$, onde $y \geq 0$, caso contrário iremos considerar como infinitamente positivo argumentando que ele certamente não será removido da base.",
        "step_5_formula_variable": "Razões",
        "phase_1_conclusion": "Conclusão da Fase 1",


        "get_negative_pivot_details": "O elemento a entrar na base é obtido ao procurarmos o elemento correspondente ao menor número negativo do vetor de custos reduzidos $c_r$ recém calculado.",
        "get_negative_pivot_entering_element_details": "Elemento a entrar na base $= min_{Negativo} <x1> $",
        "get_negative_pivot_element_index_text": "Com isso, escolhemos um elemento no indíce <x1> da lista de variáveis não básicas $<x2>$ a partir do vetor de custos reduzidos $c_r$.",
        "get_negative_pivot_chosen_element_text": "Ou seja, concluimos que $<x1>$ entrará na base.",
        "get_negative_pivot_degeneracy": "Observe que aqui temos um ponto de degenerescência haja vista que podemos escolher outros elementos para entrar na base.",


        "get_positive_pivot_leaving_element_details": "Elemento a sair da base $= min_{Positivo} <x1> $",
        "get_positive_pivot_element_index_text": "Com isso, escolhemos um elemento no indíce <x1> da lista de variáveis básicas $<x2>$ a partir do vetor coluna de razões.",
        "get_positive_pivot_chosen_element_text": "Ou seja, concluimos que $<x1>$ sairá da base.",
        "get_positive_pivot_degeneracy": "Observe que aqui temos um ponto de degenerescência haja vista que há outras opções igualmente benéficas para saírem da base.",

        "problem_standardization_text": "Padronização do Problema",
        "problem_standardization_details": "Para resolver o problema, precisamos primeiro, escrevê-lo na forma padrão:",
        "problem_standardization_lt": "Para uma desigualdade do tipo $\leq$, adicionamos apenas uma variável de folga.",
        "problem_standardization_eq": "Para o caso de uma igualdade $=$, adicionamos apenas uma variável artificial.",
        "problem_standardization_gt": "Para o caso de uma desigualdade do tipo $\geq$, então subtraímos uma variável de folga e adicionamos uma variável artificial.",
        "problem_standardization_after": "Após a padronização, obteremos uma matriz de restrições no seguinte formato:",
        "problem_standardization_result": "E então, podemos escrever o problema na forma padrão como:",

        "maximize_text": "Maximizar",
        "minimize_text": "Minimizar",
        "subject_to_text": "Sujeito a",

        "optimal_solution_found": "Solução ótima encontrada!",
        "values_text": "Valores: ",
        "basic_variables_text": "Variáveis básicas: ",
        "simple_degenerate_text": "A solução é degenerada, isto é, pode haver mais do que um conjunto de variáveis básicas."
    }

    ENGLISH_DICTIONARY = {
        "pt": "Brazilian Portuguese",
        "en": "English",
        "es": "Spanish",
        "return_to_main_menu": "Return to main menu",
        "solve_one": "Solve a Linear Optimization problem",
        "solve_all": "Solve all available Linear Optimization problems",
        "no_files": "No files available to solve.",
        "directory_not_exists": "The specified directory does not exist.",
        "no_file_error": "Error: No file was found.",
        "select_file_intro": "Please select the file you want to solve:",
        "select_file_options": "Enter the number corresponding to the file:",
        "show_steps": "Would you like to view the solution steps? (y/n): ",
        "exit_state": "Exiting the program...",
        "main_menu": "Select an option",
        "number_to_do": "Choose the number corresponding to what you want to do: ",
        "language_menu": "Choose a language",
        "language_options": "Choose the number corresponding to the language: ",
        "invalid_state": "This is not a valid menu.",
        "invalid_choice": "Invalid choice. Please select a number between 1 and",
        "invalid_option_error": "Error: Invalid input. Please enter a valid number."
    }

    SPANISH_DICTIONARY = {
        "pt": "Portugués Brasileño",
        "en": "Inglés",
        "es": "Español",
        "return_to_main_menu": "Volver al menú principal",
        "solve_one": "Resolver un problema de Optimización Lineal",
        "solve_all": "Resolver todos los problemas de Optimización Lineal disponibles",
        "no_files": "No hay archivos disponibles para resolver.",
        "directory_not_exists": "El directorio especificado no existe.",
        "no_file_error": "Error: No se encontró ningún archivo.",
        "select_file_intro": "Por favor, seleccione el archivo que desea resolver:",
        "select_file_options": "Ingrese el número correspondiente al archivo:",
        "show_steps": "¿Desea visualizar los pasos de la resolución? (s/n): ",
        "exit_state": "Saliendo del programa...",
        "main_menu": "Seleccione una opción",
        "number_to_do": "Elija el número correspondiente a lo que desea hacer: ",
        "language_menu": "Elija un idioma",
        "language_options": "Elija el número correspondiente al idioma: ",
        "invalid_state": "No es un menú válido.",
        "invalid_choice": "Opción inválida. Por favor, seleccione un número entre 1 y",
        "invalid_option_error": "Error: Entrada inválida. Por favor, ingrese un número válido."
    }

    LANGUAGE_REFERENCE = {
        "pt": PORTUGUESE_DICTIONARY,
        "en": ENGLISH_DICTIONARY,
        "es": SPANISH_DICTIONARY,
    }



    @staticmethod
    def get_text(key: str, language: str) -> str:
        try:
            return LanguageDictionary.LANGUAGE_REFERENCE[language][key]
        except KeyError:
            return "Tradução indisponível no momento."