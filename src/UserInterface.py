import os

from src.LanguageDictionary import LanguageDictionary
import Constants
from src.Utils import FileUtils, LanguageUtils
from src.Solver import RevisedSimplex

class UI:
    MENU_OPTIONS = ["solve_one", "solve_all", "language_menu", "exit_state"]

    def __init__(self):
        self.language = "pt"
        self.__select_language()
        os.system('cls||clear')

    def __switch_menu(self, next_state: str) -> int:
        os.system('cls||clear')
        states = {
            "main_menu": self.main_menu,
            "exit_state": self.__exit_state,
            "language_menu": self.__language_menu,
            "solve_one": self.__select_file_state,
            "convert_all": self.__select_method_state
        }
        if next_state in states:
            return states[next_state]()
        else:
            raise ValueError(f"{next_state} {LanguageUtils.get_translated_text('invalid_state', self.language)}")



    def __select_file_state(self) -> int:
        files = FileUtils.get_files(Constants.DATA_INPUT)
        if not files:
            LanguageUtils.print_translated("no_file_error", self.language)
            return self.main_menu()
        LanguageUtils.print_translated("select_file_intro", self.language)

        file_options = {file: os.path.basename(file) for file in files}
        file_list = list(file_options.keys())
        selected_file = self.__select_option(file_list, "select_file_options", False)
        problem = RevisedSimplex(selected_file)
        valid_yes = ["s", "y", "yes", "sim"]
        show_steps = input(LanguageDictionary.get_text("show_steps", self.language)).strip().lower()
        problem.solve(show_steps in valid_yes)

        return self.main_menu()


    def __select_method_state(self) -> int:
        problem_list = FileUtils.get_files(Constants.DATA_INPUT)
        if not problem_list:
            LanguageUtils.print_translated("no_file_error", self.language)
            return self.main_menu()
        LanguageUtils.print_translated("select_method_intro", self.language)



    def __language_menu(self) -> int:
        self.__select_language()
        return self.__switch_menu("main_menu")


    def __exit_state(self) -> int:
        LanguageUtils.print_translated("exit_state", self.language)
        return 0

    def main_menu(self) -> int:
        LanguageUtils.print_translated("main_menu", self.language)
        selected_option = self.__select_option(self.MENU_OPTIONS, LanguageUtils.get_translated_text("number_to_do", self.language))
        selected_option = self.__switch_menu(selected_option)
        return selected_option

    def __select_language(self) -> None:
        LanguageUtils.print_translated("language_menu", self.language)
        language_keys = list(LanguageDictionary.LANGUAGE_REFERENCE.keys())
        self.language = self.__select_option(language_keys, LanguageUtils.get_translated_text("language_options", self.language))

    def __select_option(self, options: list, option_detail: str, should_translate:bool = True) -> str:
        for index, key in enumerate(options, start=1):
            if should_translate:
                print(f"{index} - {LanguageUtils.get_translated_text(key, self.language)}")
            else:
                print(f"{index} - {key}")
        while True:
            try:
                choice = input(option_detail).strip()
                if choice.isdigit() and 1 <= int(choice) <= len(options):
                    return options[int(choice) - 1]


                else:
                    print(f"{LanguageUtils.get_translated_text('invalid_choice', self.language)} {len(options)}")
            except ValueError:
                LanguageUtils.print_translated("invalid_option_error", self.language)