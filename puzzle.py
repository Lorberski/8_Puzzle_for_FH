import copy
import heapq
import random
from typing import List

# goal_state = [[0, 1, 2],
#               [3, 4, 5],
#               [6, 7, 8]]

goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]


def create_random_puzzle():
    numbers = list(range(9))
    random.shuffle(numbers)
    array = [numbers[i:i + 3] for i in range(0, 9, 3)]
    return array


def check_if_solvable(puzzle):
    inversion = 0
    line_array = []
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            line_array.append(puzzle[i][j])

    line_array.remove(0)

    for i in range(len(line_array) - 1):
        for j in range(i + 1, len(line_array)):
            if line_array[i] > line_array[j]:
                inversion += 1

    return inversion % 2 == 0


def calc_hamming(puzzle):
    if puzzle is None:
        return None

    out_of_place = 0
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != 0 and puzzle[i][j] != goal_state[i][j]:
                out_of_place += 1

    return out_of_place


def pos_in_puzzle(target, puzzle):
    for row_index, row in enumerate(puzzle):
        for col_index, value in enumerate(row):
            if value == target:
                return row_index, col_index
    return None


def calc_manhattan_distance(puzzle):
    if puzzle is None:
        return None

    # Zielpositionen aus goal_state berechnen
    goal_positions = {value: (i, j) for i, row in enumerate(goal_state) for j, value in enumerate(row)}

    sum_manhattan_distance = 0

    for i, row in enumerate(puzzle):
        for j, value in enumerate(row):
            if value != 0:
                goal_i, goal_j = goal_positions[value]  #
                sum_manhattan_distance += abs(i - goal_i) + abs(j - goal_j)

    return sum_manhattan_distance


class Node:
    def __init__(self, puzzle, level, function_for_heuristic, parent):
        self.puzzle = puzzle
        self.level = level
        self.function_for_heuristic = function_for_heuristic
        self.parent_node = parent

        if function_for_heuristic is not None and puzzle is not None:
            self.heuristic_value_of_the_puzzle = function_for_heuristic(puzzle)
        else:
            self.heuristic_value_of_the_puzzle = None

        if self.level is not None and self.heuristic_value_of_the_puzzle is not None:
            self.f = self.level + self.heuristic_value_of_the_puzzle
        else:
            self.f = None

    def __lt__(self, other):
        """compares f value, is used by the heap"""
        return self.f < other.f

    def to_hashable(self):
        """Converts the puzzle into a hashable tuple of tuples."""
        return tuple(tuple(row) for row in self.puzzle)


def create_child_nodes(parent_node):
    child_nodes_list: list[Node] = []
    temp_puzzle_list = []
    row_pos_empty_field, col_pos_empty_field = pos_in_puzzle(0, parent_node.puzzle)

    if row_pos_empty_field > 0:
        temp_puzzle = copy.deepcopy(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field - 1][col_pos_empty_field] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field - 1][
            col_pos_empty_field]
        temp_puzzle_list.append(temp_puzzle)

    if row_pos_empty_field < 2:
        temp_puzzle = copy.deepcopy(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field + 1][col_pos_empty_field] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field + 1][
            col_pos_empty_field]
        temp_puzzle_list.append(temp_puzzle)

    if col_pos_empty_field > 0:
        temp_puzzle = copy.deepcopy(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field][col_pos_empty_field - 1] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field][
            col_pos_empty_field - 1]
        temp_puzzle_list.append(temp_puzzle)

    if col_pos_empty_field < 2:
        temp_puzzle = copy.deepcopy(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field][col_pos_empty_field + 1] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field][
            col_pos_empty_field + 1]
        temp_puzzle_list.append(temp_puzzle)

    for puzzle in temp_puzzle_list:
        temp_node = Node(puzzle, parent_node.level + 1, parent_node.function_for_heuristic, parent_node)
        child_nodes_list.append(temp_node)

    return child_nodes_list


def pretty_print(puzzle):
    if puzzle is None:
        print("pretty_print not possible because puzzle is none")
        return

    for row in puzzle:
        print(row)


def is_in_heap(node, heap):
    return any(existing_node.to_hashable() == node.to_hashable() for existing_node in heap)


def solve_puzzle(puzzle_as_node, visited_nodes_set, heap):
    current_node = puzzle_as_node

    while current_node.heuristic_value_of_the_puzzle != 0:

        visited_nodes_set.add(current_node.to_hashable())

        temp_child_nodes = create_child_nodes(current_node)

        for child_node in temp_child_nodes:
            if child_node.to_hashable() not in visited_nodes_set and not is_in_heap(child_node, heap):
                # print("child node:")
                # pretty_print_puzzle_node(child_node)
                heapq.heappush(heap, child_node)

        current_node = heapq.heappop(heap)

    return current_node


def pretty_print_puzzle_node(puzzle_as_a_node):
    print("----------------")
    pretty_print(puzzle_as_a_node.puzzle)
    print("level: ", puzzle_as_a_node.level)
    print("heuristic value: ", puzzle_as_a_node.heuristic_value_of_the_puzzle)
    print("f: ", puzzle_as_a_node.f)
    print("---------------")


def print_solution(solution_as_a_node):
    pretty_print_puzzle_node(solution_as_a_node)

    if solution_as_a_node.parent_node is None:
        return

    print_solution(solution_as_a_node.parent_node)


def init_solve_puzzle(puzzle, heuristic_function, visited_nodes_set, heap, set_is_in_heap):
    print("START:")
    puzzle_as_node = Node(puzzle, 0, heuristic_function, None)
    print(puzzle_as_node.function_for_heuristic)
    pretty_print_puzzle_node(puzzle_as_node)

    if not check_if_solvable(puzzle_as_node.puzzle):
        print("not solvable")
        return

    solution = solve_puzzle(puzzle_as_node, visited_nodes_set, heap)
    print("**********************************************************************")

    print_solution(solution)
