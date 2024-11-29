import copy
import heapq
import random
from typing import List
import puzzle

heap1 = []
visited_nodes_set1 = set()
nodes_in_heap1 = set()

puzzle_with_31_steps_to_solve = [[8, 6, 7],
                                 [2, 5, 4],
                                 [3, 0, 1]]

puzzle.init_solve_puzzle(
    puzzle.create_random_puzzle(), puzzle.calc_manhattan_distance, visited_nodes_set1, heap1, nodes_in_heap1
)
