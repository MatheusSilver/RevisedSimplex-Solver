import os
from src.UserInterface import UI

DATA_INPUT = "../data/input"

DATA_OUTPUT = "../data/output"


class Main:

    data_input = DATA_INPUT
    data_output = DATA_OUTPUT

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


        if not os.path.exists(DATA_OUTPUT):
            os.makedirs(DATA_OUTPUT)


        if not os.path.exists(DATA_INPUT):
            os.makedirs(DATA_INPUT)


        if not any(os.scandir(DATA_INPUT)):
            example_file_path = os.path.join(DATA_INPUT, example_file)
            with open(example_file_path, "x") as file:
                file.write(default_problem)
                file.close()



if __name__ == "__main__":
    Main.setup()
    Main.run()
