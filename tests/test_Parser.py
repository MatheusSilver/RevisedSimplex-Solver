from src.Parser import *
import os
import numpy as np
import pytest



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


def test_parse_problem_no_solution(setup_test_files):
    test_directory, _ = setup_test_files
    parser = FileParser(os.path.join(test_directory, "no_solution.lp"))
    parsed = parser.parse_file()

    assert parsed["lp_variables"] == ["a", "b"]
    assert parsed["is_maximization"] is False
    np.testing.assert_array_equal(parsed["objective_function"], np.array([7, 8], dtype=np.float64))
    np.testing.assert_array_almost_equal(parsed["constraint_matrix"], np.array([[2, 1], [-1, 4]], dtype=np.float64))
    np.testing.assert_array_equal(parsed["restrictions_vector"], np.array([-3, -7], dtype=np.float64))
    assert parsed["symbols"] == ["<=", "<="]


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
