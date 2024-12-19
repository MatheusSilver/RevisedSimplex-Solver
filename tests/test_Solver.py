import os
import pytest
import numpy as np
from src.Solver import RevisedSimplex

@pytest.mark.parametrize("filename,expected_solution,expected_basis", [
    ("default.lp", {"x": 0, "y": 3, "s_1": 1, "s_2": 0}, ["s_1", "y"]),
    ("underscore.lp", {"x_123": 3.33333, "y_456": 0, "s_1": 0, "s_2": 11.66666}, ["x_123", "s_2"]),
    ("mixed_vars.lp", {"zx_a21": 4.5, "k_9": 0, "s_1": 7.5}, ["zx_a21", "s_1"]),
    ("single_var.lp", {"z": 5, "s_1": 0}, ["z"]),
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
        #5  casas de precisão no mínimo, provavelmente se estiver errado vai ser
        #por bem mais do que isso mas né, professor Jose Roberto já dizia
        #Se o coiso for zero, é bem provavel que o aproximadamente errado se torne certo.

    assert sorted(basis) == sorted(expected_basis)

@pytest.mark.parametrize("filename", [
    "no_solution.lp",
])

#Todo: Terminar de implementar testes para casos onde a solução é infactível.
def test_revised_simplex_infeasible(setup_test_files, filename):
    test_directory, _ = setup_test_files
    file_path = os.path.join(test_directory, filename)

    solver = RevisedSimplex(file_path)
    solver.solve(show_steps=False)
