import os

from src import Constants
from src.UserInterface import UI
from src.Utils import LanguageUtils


class Main:
    @staticmethod
    def setup():
        Main.__check_directory()

    @staticmethod
    def run():
        ui = UI()
        ui.main_menu()


    @staticmethod
    def __check_directory() -> None:
        if not os.path.exists(Constants.DATA_OUTPUT):
            os.makedirs(Constants.DATA_OUTPUT)

        for language in LanguageUtils.get_available_languages():
            language_directory = os.path.join(Constants.DATA_OUTPUT, language)
            if not os.path.exists(language_directory):
                os.makedirs(language_directory)

        if not os.path.exists(Constants.DATA_INPUT):
            os.makedirs(Constants.DATA_INPUT)

        if not any(os.scandir(Constants.DATA_INPUT)):
            example_file_path = os.path.join(Constants.DATA_INPUT, Constants.EXAMPLE_FILE)
            with open(example_file_path, "x") as file:
                file.write(Constants.DEFAULT_PROBLEM)
                file.close()

if __name__ == "__main__":
    Main.setup()
    Main.run()
