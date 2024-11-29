import copy
import heapq
import random
from typing import List
import puzzle

puzzle_with_31_steps_to_solve = [[8, 6, 7],
                                 [2, 5, 4],
                                 [3, 0, 1]]

puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_hamming)

puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_manhattan_distance)
