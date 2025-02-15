"""Script to run the backtracking solver.

This script creates the sudoku puzzle using the py-sudoku package.
"""

from backtracking_solver import BacktrackingSolver

from sudoku import Sudoku

if __name__ == "__main__":
    # The value 'difficulty' should be a float in the range (0, 1).
    # It corresponds to the percentage of empty cells.
    puzzle = Sudoku().difficulty(0.7)
    solver = BacktrackingSolver(board=puzzle.board, verbose=True)
    solver.solve()
