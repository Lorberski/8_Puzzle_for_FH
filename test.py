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


if __name__ == '__main__':
    unittest.main()

