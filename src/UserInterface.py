import os

from src.LanguageDictionary import LanguageDictionary
import Constants
from src.LatexWriter import LatexWriter
from src.Utils import FileUtils, LanguageUtils
from src.Solver import RevisedSimplex

class UI:
    MENU_OPTIONS = ["solve_one", "solve_all", "language_menu", "exit_state"]

    def __init__(self):
        self.__select_language()
        os.system('cls||clear')

    def __switch_menu(self, next_state: str) -> int:
        os.system('cls||clear')
        states = {
            "main_menu": self.main_menu,
            "exit_state": self.__exit_state,
            "language_menu": self.__language_menu,
            "solve_one": self.__select_file_state,
            "solve_all": self.__select_method_state
        }
        if next_state in states:
            return states[next_state]()
        else:
            raise ValueError(f"{next_state} {LanguageUtils.get_translated_text('invalid_state')}")



    def __select_file_state(self) -> int:
        files = FileUtils.get_files(Constants.DATA_INPUT)
        if not files:
            LanguageUtils.print_translated("no_file_error")
            return self.main_menu()
        LanguageUtils.print_translated("select_file_intro")

        file_options = {os.path.basename(file):file  for file in files}
        file_list = list(file_options.keys())
        selected_file = self.__select_option(file_list, LanguageUtils.get_translated_text("select_file_options"), False)
        file_path = file_options[selected_file]
        show_steps = input(LanguageUtils.get_translated_text("show_steps")).strip().lower() in Constants.valid_yes
        problem = RevisedSimplex(file_path, show_steps, None)
        problem.solve(show_steps)

        return self.main_menu()


    def __select_method_state(self) -> int:
        problem_list = FileUtils.get_files(Constants.DATA_INPUT)
        if not problem_list:
            LanguageUtils.print_translated("no_file_error")
            return self.main_menu()
        confirmation_message = LanguageUtils.get_translated_text_variable_text("conv_all_confirmation", [str(len(problem_list))])
        confirmation_input = input(confirmation_message).strip().lower()

        if confirmation_input not in Constants.valid_yes:
            return self.__switch_menu("main_menu")

        latex_writer = LatexWriter("general")
        problem = RevisedSimplex("", True, latex_writer)
        for i in range(len(problem_list)):
            problem.reload_problem(problem_list[i])
            problem.solve(True)
            print(LanguageUtils.get_translated_text_variable_text("exercise_solved", [ problem_list[i].split("/")[-1] ]))
            if i < len(problem_list) - 1:
                problem.set_next_exercise()
            else:
                latex_writer.close()
        exit_message = LanguageUtils.get_translated_text("all_exercises_solved")
        exit_input = input(exit_message).strip().lower()
        if exit_input in Constants.valid_yes:
            return self.__switch_menu("exit_state")
        else:
            return self.__switch_menu("main_menu")



    def __language_menu(self) -> int:
        self.__select_language()
        return self.__switch_menu("main_menu")


    def __exit_state(self) -> int:
        LanguageUtils.print_translated("exit_text")
        return 0

    def main_menu(self) -> int:
        LanguageUtils.print_translated("main_menu")
        selected_option = self.__select_option(self.MENU_OPTIONS, LanguageUtils.get_translated_text("number_to_do"))
        selected_option = self.__switch_menu(selected_option)
        return selected_option

    def __select_language(self) -> None:
        LanguageUtils.print_translated("language_menu")
        language_keys = list(LanguageDictionary.LANGUAGE_REFERENCE.keys())
        new_language = self.__select_option(language_keys, LanguageUtils.get_translated_text("language_options"))
        LanguageUtils.set_language(new_language)

    @staticmethod
    def __select_option(options: list, option_detail: str, should_translate:bool = True) -> str:
        for index, key in enumerate(options, start=1):
            if should_translate:
                print(f"{index} - {LanguageUtils.get_translated_text(key)}")
            else:
                print(f"{index} - {key}")
        while True:
            try:
                choice = input(option_detail).strip()
                if choice.isdigit() and 1 <= int(choice) <= len(options):
                    return options[int(choice) - 1]


                else:
                    print(f"{LanguageUtils.get_translated_text('invalid_choice')} {len(options)}")
            except ValueError:
                LanguageUtils.print_translated("invalid_option_error")