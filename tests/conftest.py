import os
import pytest

@pytest.fixture(scope="module")
def setup_test_files():
    test_directory = "test_files"
    os.makedirs(test_directory, exist_ok=True)

#Problemas pequenos
#Feitos primeiramente pra testar o Parser (mas serviram pra testar o solver depois)
    default_problem = """max 3x + 5y
#sujeito a:
x + y <= 4
2x + 3y <= 9
x, y >= 0"""
    problem_with_underscore = """min 2x_123 + 4y_456
#sujeito a:
3x_123 + y_456 >= 10
x_123 + 5y_456 <= 15
x_123, y_456 >= 0"""
    problem_with_mixed_vars = """max 5zx_a21 + 3k_9
#sujeito a:
zx_a21 + 2k_9 <= 12
4zx_a21 + 3k_9 = 18
zx_a21, k_9 >= 0"""
    problem_no_solution = """min 7a + 8b
#sujeito a:
2a + b <= -3
-a + 4b <= -7
a, b >= 0"""
    problem_with_single_var = """max 6z
#sujeito a:
z <= 5
z >= 0"""

    problems = {
        "default.lp": default_problem,
        "underscore.lp": problem_with_underscore,
        "mixed_vars.lp": problem_with_mixed_vars,
        "no_solution.lp": problem_no_solution,
        "single_var.lp": problem_with_single_var,
    }

    for filename, content in problems.items():
        with open(os.path.join(test_directory, filename), "w") as file:
            file.write(content)

    yield test_directory, problems

    for file in os.listdir(test_directory):
        os.remove(os.path.join(test_directory, file))
    os.rmdir(test_directory)
