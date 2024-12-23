import os
import pytest

@pytest.fixture(scope="module")
def setup_test_files():
    test_directory = "test_files"
    os.makedirs(test_directory, exist_ok=True)

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
    problem_with_single_var = """max 6z
#sujeito a:
z <= 5
z >= 0"""

    problem_with_three_vars = """max 3x + 4y + 2z
#sujeito a:
x + 2y + 3z <= 60
2x + y + z <= 40
x + y + z <= 30
x, y, z >= 0"""

    problem_with_four_vars = """max 5x1 + 4x2 + 3x3 + 2x4
#sujeito a:
- x1 - x2 - x3 - x4 <= -10
2x1 + x2 + 3x3 + 4x4 <= 25
x1 + 4x2 + 2x3 + x4 <= 20
x1, x2, x3, x4 >= 0"""

    problem_with_redundant_constraints = """max 4x1 + 6x2 + 5x3
#sujeito a:
x1 + 2x2 + 3x3 <= 60
2x1 + x2 + 4x3 <= 80
x1 + x2 + x3 <= 30
x1 + x2 <= 20
x1, x2, x3 >= 0"""

    problem_with_equalities = """max 3x + 2y + z
#sujeito a:
x + 2y + z = 10
2x + y + 3z <= 15
x + y + z <= 12
x, y, z >= 0"""

    problem_degenerate = """max x + y
#sujeito a:
x + y <= 2
x <= 1
y <= 1
x, y >= 0"""

    problem_infeasible = """max x + y
#sujeito a:
x >= 5
x <= 3
x, y >= 0"""

    problem_unbounded = """max x
#sujeito a:
x >= 0"""

    problems = {
        "default.lp": default_problem,
        "underscore.lp": problem_with_underscore,
        "mixed_vars.lp": problem_with_mixed_vars,
        "single_var.lp": problem_with_single_var,
        "three_vars.lp": problem_with_three_vars,
        "four_vars.lp": problem_with_four_vars,
        "redundant_constraints.lp": problem_with_redundant_constraints,
        "equalities.lp": problem_with_equalities,
        "infeasible.lp": problem_infeasible,
        "unbounded.lp": problem_unbounded,
        "degenerate.lp": problem_degenerate
    }

    for filename, content in problems.items():
        with open(os.path.join(test_directory, filename), "w") as file:
            file.write(content)

    yield test_directory, problems

    for file in os.listdir(test_directory):
        os.remove(os.path.join(test_directory, file))
    os.rmdir(test_directory)
