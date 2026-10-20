"""Sudoku puzzle generation and game state."""

from __future__ import annotations

import random
from typing import Iterable

Grid = list[list[int]]

DIFFICULTIES = {
    "Fácil": 36,
    "Intermedio": 46,
    "Difícil": 54,
}


def candidates(grid: Grid, row: int, col: int) -> list[int]:
    """Return the values that can legally be placed in an empty cell."""
    used = set(grid[row])
    used.update(grid[index][col] for index in range(9))
    box_row, box_col = row // 3 * 3, col // 3 * 3
    used.update(
        grid[r][c]
        for r in range(box_row, box_row + 3)
        for c in range(box_col, box_col + 3)
    )
    return [value for value in range(1, 10) if value not in used]


def _next_empty(grid: Grid) -> tuple[int, int] | None:
    """Choose the most constrained empty cell to keep solving efficient."""
    best: tuple[int, int] | None = None
    fewest = 10
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                count = len(candidates(grid, row, col))
                if count < fewest:
                    best, fewest = (row, col), count
                    if count <= 1:
                        return best
    return best


def count_solutions(grid: Grid, limit: int = 2) -> int:
    """Count solutions up to ``limit`` without changing the supplied grid."""
    working = [row[:] for row in grid]
    total = 0

    def search() -> None:
        nonlocal total
        if total >= limit:
            return
        empty = _next_empty(working)
        if empty is None:
            total += 1
            return
        row, col = empty
        for value in candidates(working, row, col):
            working[row][col] = value
            search()
            working[row][col] = 0
            if total >= limit:
                return

    search()
    return total


class SudokuGenerator:
    """Create randomized, uniquely solvable Sudoku puzzles."""

    @staticmethod
    def generate(difficulty: str) -> tuple[Grid, Grid]:
        if difficulty not in DIFFICULTIES:
            raise ValueError(f"Nivel desconocido: {difficulty}")

        solution: Grid = [[0] * 9 for _ in range(9)]

        def fill() -> bool:
            empty = _next_empty(solution)
            if empty is None:
                return True
            row, col = empty
            options = candidates(solution, row, col)
            random.shuffle(options)
            for value in options:
                solution[row][col] = value
                if fill():
                    return True
            solution[row][col] = 0
            return False

        fill()
        puzzle = [row[:] for row in solution]
        cells = [(row, col) for row in range(9) for col in range(9)]
        random.shuffle(cells)
        removed = 0
        target = DIFFICULTIES[difficulty]

        for row, col in cells:
            if removed >= target:
                break
            original = puzzle[row][col]
            puzzle[row][col] = 0
            if count_solutions(puzzle) == 1:
                removed += 1
            else:
                puzzle[row][col] = original

        return puzzle, solution


class SudokuBoard:
    """Mutable player board with immutable clues and answer checking."""

    def __init__(self, puzzle: Grid, solution: Grid) -> None:
        self.puzzle = [row[:] for row in puzzle]
        self.solution = [row[:] for row in solution]
        self.values = [row[:] for row in puzzle]
        self.givens = {
            (row, col)
            for row in range(9)
            for col in range(9)
            if puzzle[row][col] != 0
        }
        self.notes: dict[tuple[int, int], set[int]] = {}
        self.mistakes = 0
        self.hints_used = 0

    def is_editable(self, row: int, col: int) -> bool:
        return (row, col) not in self.givens

    def set_value(self, row: int, col: int, value: int, notes_mode: bool = False) -> bool:
        if not self.is_editable(row, col):
            return False
        if value not in range(1, 10):
            raise ValueError("El valor debe estar entre 1 y 9.")
        if notes_mode:
            cell_notes = self.notes.setdefault((row, col), set())
            if value in cell_notes:
                cell_notes.remove(value)
            else:
                cell_notes.add(value)
            return True

        self.notes.pop((row, col), None)
        self.values[row][col] = value
        if value != self.solution[row][col]:
            self.mistakes += 1
        return True

    def clear(self, row: int, col: int) -> bool:
        if not self.is_editable(row, col):
            return False
        self.values[row][col] = 0
        self.notes.pop((row, col), None)
        return True

    def hint(self, row: int, col: int) -> bool:
        if not self.is_editable(row, col) or self.values[row][col] == self.solution[row][col]:
            return False
        self.values[row][col] = self.solution[row][col]
        self.notes.pop((row, col), None)
        self.hints_used += 1
        return True

    def conflicts(self) -> set[tuple[int, int]]:
        """Return filled cells that conflict in a row, column, or 3x3 box."""
        conflict_cells: set[tuple[int, int]] = set()
        for row in range(9):
            for col in range(9):
                value = self.values[row][col]
                if value == 0:
                    continue
                peers: Iterable[tuple[int, int]] = (
                    [(row, other) for other in range(9) if other != col]
                    + [(other, col) for other in range(9) if other != row]
                    + [
                        (r, c)
                        for r in range(row // 3 * 3, row // 3 * 3 + 3)
                        for c in range(col // 3 * 3, col // 3 * 3 + 3)
                        if (r, c) != (row, col)
                    ]
                )
                if any(self.values[r][c] == value for r, c in peers):
                    conflict_cells.add((row, col))
        return conflict_cells

    def is_complete(self) -> bool:
        return self.values == self.solution
