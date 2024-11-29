import heapq
import random
import time
from pympler import asizeof

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


def copy_puzzle(puzzle):
    return [row[:] for row in puzzle]


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

    # dict vor goal positions in goal_state
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

        self.time_to_solve_till_goal_node = None

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
        temp_puzzle = copy_puzzle(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field - 1][col_pos_empty_field] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field - 1][
            col_pos_empty_field]
        temp_puzzle_list.append(temp_puzzle)

    if row_pos_empty_field < 2:
        temp_puzzle = copy_puzzle(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field + 1][col_pos_empty_field] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field + 1][
            col_pos_empty_field]
        temp_puzzle_list.append(temp_puzzle)

    if col_pos_empty_field > 0:
        temp_puzzle = copy_puzzle(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field][col_pos_empty_field - 1] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field][
            col_pos_empty_field - 1]
        temp_puzzle_list.append(temp_puzzle)

    if col_pos_empty_field < 2:
        temp_puzzle = copy_puzzle(parent_node.puzzle)
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


def solve_puzzle(puzzle_as_node, visited_nodes_set, heap, set_is_in_heap):
    start_time = time.time()
    current_node = puzzle_as_node

    while current_node.heuristic_value_of_the_puzzle != 0:

        visited_nodes_set.add(current_node.to_hashable())

        temp_child_nodes = create_child_nodes(current_node)

        for child_node in temp_child_nodes:
            if child_node.to_hashable() not in visited_nodes_set and child_node.to_hashable() not in set_is_in_heap:
                heapq.heappush(heap, child_node)
                set_is_in_heap.add(child_node.to_hashable())

        current_node = heapq.heappop(heap)
        current_node.time_to_solve_till_goal_node = time.time() - start_time

    return current_node


def init_solve_one_puzzle(puzzle, heuristic_function, with_console_output):
    puzzle_as_node = Node(puzzle, 0, heuristic_function, None)
    if with_console_output:
        print("START:")
        print(puzzle_as_node.function_for_heuristic)
        pretty_print_puzzle_node(puzzle_as_node)

    start_time = time.time()

    if not check_if_solvable(puzzle_as_node.puzzle):
        print("not solvable")
        return

    heap = []
    visited_nodes_set = set()
    set_is_in_heap = set()

    solution = solve_puzzle(puzzle_as_node, visited_nodes_set, heap, set_is_in_heap)

    if with_console_output:
        print("**********************************************************************")

        print_solution(solution)
        time_needed = time.time() - start_time
        print(f"Time: {time_needed:.6f} seconds")
        print(f"total memory from heap: {asizeof.asizeof(heap)} Bytes")

    return asizeof.asizeof(heap), solution.time_to_solve_till_goal_node


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


def creat_100_solvable_puzzles():
    list_of_100_puzzles = []

    while len(list_of_100_puzzles) != 100:
        temp_puzzle = create_random_puzzle()
        if check_if_solvable(temp_puzzle):
            list_of_100_puzzles.append(temp_puzzle)

    return list_of_100_puzzles


def solve_list_of_puzzles(solvable_puzzle_list, heuristic_function, list_of_times_for_each_puzzle_in_sec,
                          list_of_memory_for_each_puzzle_in_bytes):
    total_start_time = time.time()

    for current_puzzle in solvable_puzzle_list:
        heap_memory, solution_time = init_solve_one_puzzle(current_puzzle, heuristic_function, False)
        list_of_memory_for_each_puzzle_in_bytes.append(heap_memory)
        list_of_times_for_each_puzzle_in_sec.append(solution_time)

    print("Total time: ", time.time() - total_start_time, " sec")


def calc_mean(list_of_numbers):
    return sum(list_of_numbers) / len(list_of_numbers)


def calc_variance(mean, list_of_numbers):
    return sum((x - mean) ** 2 for x in list_of_numbers) / len(list_of_numbers)
