import unittest

from sudoku import DIFFICULTIES, SudokuBoard, SudokuGenerator, count_solutions


class SudokuTests(unittest.TestCase):
    def test_generated_puzzles_have_unique_solution_at_each_level(self):
        for difficulty, blanks in DIFFICULTIES.items():
            with self.subTest(difficulty=difficulty):
                puzzle, solution = SudokuGenerator.generate(difficulty)
                self.assertEqual(sum(value == 0 for row in puzzle for value in row), blanks)
                self.assertEqual(count_solutions(puzzle), 1)
                self.assertEqual(count_solutions(solution), 1)

    def test_solution_is_valid_in_rows_columns_and_boxes(self):
        _, solution = SudokuGenerator.generate("Fácil")
        expected = set(range(1, 10))
        self.assertTrue(all(set(row) == expected for row in solution))
        self.assertTrue(all({solution[row][col] for row in range(9)} == expected for col in range(9)))
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box = {
                    solution[row][col]
                    for row in range(box_row, box_row + 3)
                    for col in range(box_col, box_col + 3)
                }
                self.assertEqual(box, expected)

    def test_board_protects_clues_and_tracks_entry_notes_and_hint(self):
        puzzle, solution = SudokuGenerator.generate("Fácil")
        board = SudokuBoard(puzzle, solution)
        given = next(iter(board.givens))
        self.assertFalse(board.set_value(*given, 1))

        empty = next((row, col) for row in range(9) for col in range(9) if puzzle[row][col] == 0)
        self.assertTrue(board.set_value(*empty, 1, notes_mode=True))
        self.assertIn(1, board.notes[empty])
        self.assertTrue(board.clear(*empty))
        self.assertTrue(board.hint(*empty))
        self.assertEqual(board.values[empty[0]][empty[1]], solution[empty[0]][empty[1]])
        self.assertEqual(board.hints_used, 1)

    def test_wrong_entries_are_counted_and_conflicts_detected(self):
        puzzle, solution = SudokuGenerator.generate("Fácil")
        board = SudokuBoard(puzzle, solution)
        empty = next(
            (row, col)
            for row in range(9)
            for col in range(9)
            if puzzle[row][col] == 0 and any(puzzle[row][other] for other in range(9))
        )
        wrong = next(
            value
            for value in puzzle[empty[0]]
            if value != 0 and value != solution[empty[0]][empty[1]]
        )
        board.set_value(*empty, wrong)
        self.assertEqual(board.mistakes, 1)
        self.assertIn(empty, board.conflicts())

    def test_invalid_level_is_rejected(self):
        with self.assertRaises(ValueError):
            SudokuGenerator.generate("Experto")


if __name__ == "__main__":
    unittest.main()
