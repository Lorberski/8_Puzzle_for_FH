import copy
import heapq
import random
from typing import List
import puzzle

heap1 = []
visited_nodes_set1 = set()

puzzle_with_31_steps_to_solve = [[8, 6, 7],
                                 [2, 5, 4],
                                 [3, 0, 1]]

goal_state_as_a_node = puzzle.Node(puzzle.goal_state, 0, puzzle.calc_hamming, None)
random_note = puzzle.Node(puzzle.create_random_puzzle(), 0, puzzle.calc_hamming, None)
max_note = puzzle.Node(puzzle_with_31_steps_to_solve, 0, puzzle.calc_hamming, None)

puzzle.init_solve_puzzle(random_note, visited_nodes_set1, heap1)
