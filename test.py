import random

import puzzle
import unittest


class TestPuzzleOperations(unittest.TestCase):

    def test_check_if_solvable(self):
        false_state = [[8, 1, 2],
                       [0, 4, 3],
                       [7, 6, 5]]

        false_state2 = [[8, 1, 2],
                        [0, 4, 3],
                        [7, 6, 5]]

        true_state = [[1, 8, 2],
                      [0, 4, 3],
                      [7, 6, 5]]

        goal_state = [[0, 1, 2],
                      [3, 4, 5],
                      [6, 7, 8]]

        self.assertFalse(puzzle.check_if_solvable(false_state))
        self.assertFalse(puzzle.check_if_solvable(false_state2))
        self.assertTrue(puzzle.check_if_solvable(true_state))
        self.assertTrue(puzzle.check_if_solvable(goal_state))

    def test_if_creat_100_puzzle_length_is_100(self):
        list_to_test = puzzle.creat_100_solvable_puzzles()

        length_of_list = len(list_to_test)
        self.assertEqual(length_of_list, 100, f"length of list: {length_of_list} : is not 100")

    def test_if_all_puzzles_in_list_of_100_solvable_puzzle_is_solvable(self):
        list_to_test = puzzle.creat_100_solvable_puzzles()

        for current_puzzle in list_to_test:
            self.assertTrue(puzzle.check_if_solvable(current_puzzle))


if __name__ == '__main__':
    unittest.main()
