import os

from src import Constants
from src.UserInterface import UI


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
        default_problem = """max z = 3x + 5y
x + y <= 4
2x + 3y <= 9
x, y >= 0"""

        example_file = "example.txt"


        if not os.path.exists(Constants.DATA_OUTPUT):
            os.makedirs(Constants.DATA_OUTPUT)


        if not os.path.exists(Constants.DATA_INPUT):
            os.makedirs(Constants.DATA_INPUT)


        if not any(os.scandir(Constants.DATA_INPUT)):
            example_file_path = os.path.join(Constants.DATA_INPUT, example_file)
            with open(example_file_path, "x") as file:
                file.write(default_problem)
                file.close()



if __name__ == "__main__":
    Main.setup()
    Main.run()
