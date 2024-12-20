from src.Parser import *
import os
import numpy as np
import pytest

POSITIVE_INFINITY = np.inf
NEGATIVE_INFINITY = -np.inf

def test_file_reading(setup_test_files):
    test_directory, problems = setup_test_files
    for filename, content in problems.items():
        with open(os.path.join(test_directory, filename), "r") as file:
            read_content = file.read()
            assert read_content == content, f"Content mismatch in file {filename}"


def test_parse_default_problem(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "default.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["x", "y"]
    assert parsed["is_maximization"] is True
    np.testing.assert_array_equal(parsed["objective_function"], np.array([3, 5], dtype=np.float64))
    np.testing.assert_array_almost_equal(parsed["constraint_matrix"], np.array([[1, 1], [2, 3]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([4, 9], dtype=np.float64))
    assert parsed["symbols"] == ["<=", "<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0, 0], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([POSITIVE_INFINITY, POSITIVE_INFINITY], dtype=np.float64))


def test_parse_problem_with_underscore(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "underscore.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["x_123", "y_456"]
    assert parsed["is_maximization"] is False
    np.testing.assert_array_equal(parsed["objective_function"], np.array([2, 4], dtype=np.float64))
    np.testing.assert_array_almost_equal(parsed["constraint_matrix"], np.array([[3, 1], [1, 5]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([10, 15], dtype=np.float64))
    assert parsed["symbols"] == [">=", "<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0, 0], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([POSITIVE_INFINITY, POSITIVE_INFINITY], dtype=np.float64))


def test_parse_problem_with_mixed_vars(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "mixed_vars.lp"))
    parsed = parser.parse_file()
    assert parsed["lp_variables"] == ["k_9", "zx_a21"]
    assert parsed["is_maximization"] is True
    np.testing.assert_array_equal(parsed["objective_function"], np.array([3, 5], dtype=np.float64))
    np.testing.assert_array_almost_equal(parsed["constraint_matrix"], np.array([[2, 1], [3, 4]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([12, 18], dtype=np.float64))
    assert parsed["symbols"] == ["<=", "="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0, 0], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([POSITIVE_INFINITY, POSITIVE_INFINITY], dtype=np.float64))


def test_parse_problem_with_single_var(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "single_var.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["z"]
    assert parsed["is_maximization"] is True
    np.testing.assert_array_equal(parsed["objective_function"], np.array([6], dtype=np.float64))
    np.testing.assert_array_almost_equal(parsed["constraint_matrix"], np.array([[1]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([5], dtype=np.float64))
    assert parsed["symbols"] == ["<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([POSITIVE_INFINITY], dtype=np.float64))


def test_parse_problem_with_three_vars(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "three_vars.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["x", "y", "z"]
    assert parsed["is_maximization"] is True
    np.testing.assert_array_equal(parsed["objective_function"], np.array([3, 4, 2], dtype=np.float64))
    np.testing.assert_array_almost_equal(parsed["constraint_matrix"], np.array([[1, 2, 3], [2, 1, 1], [1, 1, 1]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([60, 40, 30], dtype=np.float64))
    assert parsed["symbols"] == ["<=", "<=", "<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0, 0, 0], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([POSITIVE_INFINITY, POSITIVE_INFINITY, POSITIVE_INFINITY], dtype=np.float64))


def test_parse_problem_with_degenerate_case(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "degenerate.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["x", "y"]
    assert parsed["is_maximization"] is True
    np.testing.assert_array_equal(parsed["objective_function"], np.array([1, 1], dtype=np.float64))
    np.testing.assert_array_almost_equal(parsed["constraint_matrix"], np.array([[1, 1], [1, 0], [0, 1]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([2, 1, 1], dtype=np.float64))
    assert parsed["symbols"] == ["<=", "<=", "<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0, 0], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([POSITIVE_INFINITY, POSITIVE_INFINITY], dtype=np.float64))

def test_parse_single_var_problem(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "single_var_and_restrictions.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["x"]
    assert parsed["is_maximization"] is True
    np.testing.assert_array_equal(parsed["objective_function"], np.array([8], dtype=np.float64))
    np.testing.assert_array_equal(parsed["constraint_matrix"], np.array([[2]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([10], dtype=np.float64))
    assert parsed["symbols"] == ["<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([5], dtype=np.float64))

# Teste para o problema com duas variáveis e suas restrições (versão 1)
def test_parse_two_vars_problem_1(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "two_vars_and_restrictions_1.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["x", "y"]
    assert parsed["is_maximization"] is False
    np.testing.assert_array_equal(parsed["objective_function"], np.array([3, 7], dtype=np.float64))
    np.testing.assert_array_equal(parsed["constraint_matrix"], np.array([[1, 2], [2, 1]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([6, 12], dtype=np.float64))
    assert parsed["symbols"] == [">=", "<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0, 1], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([POSITIVE_INFINITY, 5], dtype=np.float64))

# Teste para o problema com duas variáveis e suas restrições (versão 2)
def test_parse_two_vars_problem_2(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "two_vars_and_restrictions_2.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["a", "b"]
    assert parsed["is_maximization"] is True
    np.testing.assert_array_equal(parsed["objective_function"], np.array([4, 5], dtype=np.float64))
    np.testing.assert_array_equal(parsed["constraint_matrix"], np.array([[3, 2], [1, 1]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([15, 4], dtype=np.float64))
    assert parsed["symbols"] == ["<=", ">="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0, 2], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([6, POSITIVE_INFINITY], dtype=np.float64))

# Teste para o problema com três variáveis e suas restrições (versão 1)
def test_parse_three_vars_problem_1(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "three_vars_and_restrictions_1.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["x", "y", "z"]
    assert parsed["is_maximization"] is False
    np.testing.assert_array_equal(parsed["objective_function"], np.array([5, 3, 2], dtype=np.float64))
    np.testing.assert_array_equal(parsed["constraint_matrix"], np.array([[1, 1, 1], [2, 0, 1], [1, 3, 0]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([10, 6, 9], dtype=np.float64))
    assert parsed["symbols"] == ["<=", ">=", "<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0, 1, 0], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([POSITIVE_INFINITY, POSITIVE_INFINITY, 4], dtype=np.float64))

# Teste para o problema com três variáveis e suas restrições (versão 2)
def test_parse_three_vars_problem_2(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "three_vars_and_restrictions_2.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["x", "y", "z"]
    assert parsed["is_maximization"] is True
    np.testing.assert_array_equal(parsed["objective_function"], np.array([6, 4, 1], dtype=np.float64))
    np.testing.assert_array_equal(parsed["constraint_matrix"], np.array([[1, 1, 1], [2, 3, 0], [1, 0, 2]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([8, 15, 10], dtype=np.float64))
    assert parsed["symbols"] == [">=", "<=", "<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([1, 0, 2], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([5, POSITIVE_INFINITY, 6], dtype=np.float64))

# Teste para o problema com três variáveis e suas restrições (versão 3)
def test_parse_three_vars_problem_3(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "three_vars_and_restrictions_3.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["x", "y", "z"]
    assert parsed["is_maximization"] is False
    np.testing.assert_array_equal(parsed["objective_function"], np.array([7, 2, 5], dtype=np.float64))
    np.testing.assert_array_equal(parsed["constraint_matrix"], np.array([[1, 2, 3], [2, 1, 0], [0, 3, 1]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([12, 5, 8], dtype=np.float64))
    assert parsed["symbols"] == ["<=", ">=", "<="]
    np.testing.assert_array_equal(parsed["inferior_boundaries"], np.array([0, 1, 0], dtype=np.float64))
    np.testing.assert_array_equal(parsed["superior_boundaries"], np.array([4, 3, POSITIVE_INFINITY], dtype=np.float64))


