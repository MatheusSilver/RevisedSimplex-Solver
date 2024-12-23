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
        "select_file_intro": "Por favor, selecione o arquivo que deseja resolver:",
        "select_file_options": "Digite o número correspondente ao arquivo:",
        "show_steps": "Deseja visualizar os passos da resolução? (s/n): ",
        "exit_state": "Encerrando o programa...",
        "main_menu": "Selecione uma opção",
        "number_to_do": "Escolha o número correspondente ao que deseja fazer: ",
        "language_menu": "Escolha um idioma",
        "language_options": "Escolha o número correspondente ao idioma: ",
        "invalid_state": "Não é um menu válido.",
        "invalid_choice": "Escolha inválida. Por favor, selecione um número entre 1 e",
        "invalid_option_error": "Erro: Entrada inválida. Por favor, insira um número válido."
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
            return f"[Tradução de {key} não encontrada]"
