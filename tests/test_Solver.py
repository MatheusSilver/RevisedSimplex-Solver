import os

import numpy as np
import pytest
from src.Solver import RevisedSimplex, RevisedSimplexWithoutFile


@pytest.mark.parametrize("filename,expected_solution,expected_basis", [
    ("default.lp", {"x": 0, "y": 3, "s_1": 1, "s_2": 0}, ["s_1", "y"]),
    ("underscore.lp", {"x_123": 3.33333, "y_456": 0, "s_1": 0, "s_2": 11.66666}, ["x_123", "s_2"]),
    ("mixed_vars.lp", {"zx_a21": 4.5, "k_9": 0, "s_1": 7.5}, ["zx_a21", "s_1"]),
    ("single_var.lp", {"z": 5, "s_1": 0}, ["z"]),
    ("four_vars.lp", {"x1": 11.42857, "x2": 2.142857, "x3": 0, "x4": 0, "s_1": 3.571428, "s_2": 0, "s_3": 0}, ["x1", "x2", "s_1"]),
    ("redundant_constraints.lp", {"x1": 0, "x2": 20, "x3": 6.666666, "s_1": 0, "s_2": 33.333333, "s_3": 3.333333, "s_4": 0}, ["x2", "x3", "s_2", "s_3"]),
    ("equalities.lp", {"x": 6.666666, "y": 1.666666, "z": 0, "s_2": 0, "s_3": 3.6666666}, ["x", "y", "s_3"]),
])
def test_revised_simplex_optimal(setup_test_files, filename, expected_solution, expected_basis):
    test_directory, _ = setup_test_files
    file_path = os.path.join(test_directory, filename)

    solver = RevisedSimplex(file_path)
    solver.solve(show_steps=False)

    solution = solver.get_solution()
    basis = solver.basis

    for var, expected_value in expected_solution.items():
        assert solution[var] == pytest.approx(expected_value, rel=1e-5)
    assert solver.status == "optimal"

    assert sorted(basis) == sorted(expected_basis)

@pytest.mark.parametrize("filename,expected_solution,expected_basis", [
    ("degenerate.lp", {"x": 1, "y": 1, "s_1": 0, "s_2": 0, "s_3": 0}, ["x", "y", "s_3"]),
    ("three_vars.lp", {"x": 0, "y": 30, "z": 0, "s_1": 0, "s_2": 10, "s_3": 0}, ["x", "y", "s_2"]),
])

def test_revised_simplex_degenerate_case(setup_test_files, filename, expected_solution, expected_basis):
    test_directory, _ = setup_test_files
    file_path = os.path.join(test_directory, filename)

    solver = RevisedSimplex(file_path)
    solver.solve(show_steps=False)

    solution = solver.get_solution()
    basis = solver.basis

    for var, expected_value in expected_solution.items():
        assert solution[var] == pytest.approx(expected_value, rel=1e-5)

    assert solver.status == "degenerate"
    assert sorted(basis) == sorted(expected_basis)


@pytest.mark.parametrize("filename", [
    "unbounded.lp",
])
def test_revised_simplex_unbounded_case(setup_test_files, filename):
    test_directory, _ = setup_test_files
    file_path = os.path.join(test_directory, filename)

    solver = RevisedSimplex(file_path)
    solver.solve(show_steps=False)

    assert solver.status == "unbounded"


@pytest.mark.parametrize("filename", [
    "infeasible.lp",
])
def test_revised_simplex_infeasible_case(setup_test_files, filename):
    test_directory, _ = setup_test_files
    file_path = os.path.join(test_directory, filename)

    solver = RevisedSimplex(file_path)
    solver.solve(show_steps=False)

    assert "infeasible" in solver.status


@pytest.mark.parametrize("objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols, expected_solution, expected_basis", [
    (np.array([3, 5], dtype=np.float64),
     np.array([[1, 0], [0, 2], [3, 2]], dtype=np.float64),
     True,
     np.array([4, 12, 18], dtype=np.float64),
     ["<=", "<=", "<="],
     {"x1": 2.0, "x2": 6.0, "s_1": 2, "s_2": 0, "s_3": 0},
     ["x1", "x2", "s_1"]),
])
def test_revised_simplex_without_file_optimal(objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols, expected_solution, expected_basis):
    solver = RevisedSimplexWithoutFile(objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols)
    solver.solve(show_steps=False)

    solution = solver.get_solution()
    basis = solver.basis

    for var, expected_value in expected_solution.items():
        assert solution[var] == pytest.approx(expected_value, rel=1e-5)
    assert solver.status == "optimal"
    assert sorted(basis) == sorted(expected_basis)


@pytest.mark.parametrize("objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols, expected_solution, expected_basis", [
    (np.array([1, 1], dtype=np.float64),
     np.array([[1, 1], [1, -1], [-1, 1]], dtype=np.float64),
     True,
     np.array([2, 0, 0], dtype=np.float64),
     ["<=", "<=", "<="],
     {"x1": 1.0, "x2": 1.0, "s_1": 0, "s_2": 0, "s_3": 0},
     ["x1", "x2", "s_3"]),

])
def test_revised_simplex_without_file_degenerate_case(objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols, expected_solution, expected_basis):
    solver = RevisedSimplexWithoutFile(objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols)
    solver.solve(show_steps=False)

    solution = solver.get_solution()
    basis = solver.basis

    for var, expected_value in expected_solution.items():
        assert solution[var] == pytest.approx(expected_value, rel=1e-5)

    assert solver.status == "degenerate"
    assert sorted(basis) == sorted(expected_basis)


@pytest.mark.parametrize("objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols", [
    (np.array([1, 1], dtype=np.float64),
     np.array([[1, -1], [-1, 1]], dtype=np.float64),
     True,
     np.array([1, 1], dtype=np.float64),
     ["<=", "<="]),
])
def test_revised_simplex_without_file_unbounded_case(objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols):
    solver = RevisedSimplexWithoutFile(objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols)
    print()
    print(solver.degeneracy_points)
    solver.solve(show_steps=False)

    assert solver.status == "unbounded"


@pytest.mark.parametrize("objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols", [
    (np.array([1, 1], dtype=np.float64),
     np.array([[1, 1], [-1, -1]], dtype=np.float64),
     True,
     np.array([2, -3], dtype=np.float64),
     ["<=", "<="]),
])
def test_revised_simplex_without_file_infeasible_case(objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols):
    solver = RevisedSimplexWithoutFile(objective, constraint_matrix, is_maximization, restrictions, restrictions_symbols)
    solver.solve(show_steps=False)

    assert "infeasible" in solver.status
