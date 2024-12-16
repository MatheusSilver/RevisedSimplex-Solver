import os

from src.LanguageDictionary import LanguageDictionary
from src.Main import Main
from src.Solver import RevisedSimplex
from src.Utils import FileUtils

class UI:
    MENU_OPTIONS = ["solve_one", "solve_all", "language_menu", "exit_state"]

    def __init__(self):
        self.language = None
        self.__select_language()
        os.system('cls||clear')

    def __switch_menu(self, next_state: str) -> int:
        os.system('cls||clear')
        states = {
            "main_menu": self.main_menu(),
            "exit_state": self.__exit_state(),
            "language_menu": self.__language_menu(),
            "solve_one": self.__select_file_state(),
            "convert_all": self.__select_method_state()
        }

        if next_state in states:
            return states.get(next_state)
        else:
            raise ValueError(f"{next_state} {self.__get_translated_text('invalid_state')}")



    def __select_file_state(self) -> int:
        files = FileUtils.get_files(Main.data_input)
        if not files:
            self.__print_translated("no_file_error")
            return self.main_menu()
        self.__print_translated("select_file_intro")

        file_options = {file: file.split("/input/")[1] for file in files}
        file_list = list(file_options.keys())
        selected_file = self.__select_option(file_list, "select_file_options")
        show_steps = input(LanguageDictionary.get_text("show_steps", self.language))
        problem = RevisedSimplex(selected_file)
        problem.solve(show_steps.lower() == "s")

        return self.main_menu()


    def __select_method_state(self) -> int:
        problem_list = FileUtils.get_files(Main.data_input)
        if not problem_list:
            self.__print_translated("no_file_error")
            return self.main_menu()
        self.__print_translated("select_method_intro")



    def __language_menu(self) -> int:
        self.__select_language()
        return self.__switch_menu("main_menu")


    def __exit_state(self) -> int:
        self.__print_translated("exit_state")
        return 0

    def main_menu(self) -> int:
        self.__print_translated("main_menu")
        selected_option = self.__select_option(self.MENU_OPTIONS, self.__get_translated_text("number_to_do"))
        selected_option = self.__switch_menu(selected_option)
        return selected_option

    def __select_language(self) -> None:
        self.__print_translated("language_menu")
        self.language = self.__select_option(LanguageDictionary.LANGUAGE_REFERENCE.keys(), self.__get_translated_text("language_options"))


    def __select_option(self, options: list, option_detail: str, should_translate:bool = False) -> str:
        for index, key in enumerate(options, start=1):
            if should_translate:
                print(f"{index} - {self.__get_translated_text(key)}")
            else:
                print(f"{index} - {key}")
        while True:
            try:
                choice = int(input(option_detail))
                if 1 <= choice <= len(options):

                    selected_code = options[choice - 1]
                    return selected_code
                else:
                    print(f"{self.__get_translated_text('invalid_choice')} {len(options)}")
                    #print(f"Invalid choice. Please select a number between 1 and {len(options)}.")
            except ValueError:
                self.__print_translated("invalid_option_error")
                #print("Invalid input. Please enter a valid number.")


    def __print_translated(self, key):
        print(self.__get_translated_text(key))

    def __get_translated_text(self, key: str) -> str:
        return LanguageDictionary.get_text(key, self.language)