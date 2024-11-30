import heapq
import random
import time
from pympler import asizeof

# goal_state is the goal configuration of the puzzle
goal_state = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]


# Function to create a random puzzle
def create_random_puzzle():
    """
    Generates a random puzzle by shuffling numbers from 0 to 8.

    Output:
        - A 3x3 array (list of lists) representing the puzzle, where each number is
          placed randomly, and 0 represents the empty space.
    """
    numbers = list(range(9))  # List of numbers from 0 to 8
    random.shuffle(numbers)  # Shuffle the numbers to create a random puzzle
    array = [numbers[i:i + 3] for i in range(0, 9, 3)]  # Convert to a 3x3 list of lists
    return array  # Output: A 3x3 list of lists representing the puzzle


# Function to make a copy of the puzzle
def copy_puzzle(puzzle):
    """
    Makes a deep copy of the puzzle to avoid modifying the original one.

    Input:
        - puzzle: A 3x3 array (list of lists) representing the current puzzle state.

    Output:
        - A deep copy of the input puzzle as a 3x3 array.
    """
    return [row[:] for row in puzzle]  # Output: A new copy of the puzzle (deep copy)


# Function to check if the puzzle is solvable
def check_if_solvable(puzzle):
    """
    Checks if a given puzzle configuration is solvable based on the number of inversions.

    Input:
        - puzzle: A 3x3 array (list of lists) representing the puzzle state.

    Output:
        - True if the puzzle is solvable, False otherwise.
    """
    inversion = 0  # Variable to count the inversions
    line_array = []  # List to store puzzle values in a single line
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            line_array.append(puzzle[i][j])

    line_array.remove(0)  # Remove 0, since it's the empty space and doesn't count towards inversions

    # Count the number of inversions (pairs of tiles where the larger number comes before the smaller one)
    for i in range(len(line_array) - 1):
        for j in range(i + 1, len(line_array)):
            if line_array[i] > line_array[j]:
                inversion += 1

    return inversion % 2 == 0  # Output: True if solvable, False otherwise


# Function to calculate the Hamming distance (number of misplaced tiles)
def calc_hamming(puzzle):
    """
    Calculates the Hamming distance of the puzzle. It counts how many tiles are
    out of place compared to the goal state.

    Input:
        - puzzle: A 3x3 array (list of lists) representing the puzzle state.

    Output:
        - The number of misplaced tiles (Hamming distance).
    """
    if puzzle is None:
        return None

    out_of_place = 0  # Counter for out-of-place tiles
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] != 0 and puzzle[i][j] != goal_state[i][j]:
                out_of_place += 1  # Increment if the tile is out of place

    return out_of_place  # Output: Number of misplaced tiles


# Function to get the position of a tile in the puzzle
def pos_in_puzzle(target, puzzle):
    """
    Finds the position of a specific tile in the puzzle.

    Input:
        - target: The value of the tile to search for.
        - puzzle: A 3x3 array (list of lists) representing the puzzle state.

    Output:
        - A tuple (row_index, col_index) representing the position of the tile in the puzzle.
    """
    for row_index, row in enumerate(puzzle):
        for col_index, value in enumerate(row):
            if value == target:
                return row_index, col_index  # Output: (row_index, col_index) of the target tile
    return None


# Function to calculate the Manhattan distance (sum of the distances each tile is from its goal position)
def calc_manhattan_distance(puzzle):
    """
    Calculates the Manhattan distance for the puzzle. It computes the sum of the
    distances each tile is from its goal position.

    Input:
        - puzzle: A 3x3 array (list of lists) representing the puzzle state.

    Output:
        - The total Manhattan distance of the puzzle.
    """
    if puzzle is None:
        return None

    # Dictionary to store the goal positions of each tile in goal_state
    goal_positions = {value: (i, j) for i, row in enumerate(goal_state) for j, value in enumerate(row)}

    sum_manhattan_distance = 0  # Variable to store the total Manhattan distance

    for i, row in enumerate(puzzle):
        for j, value in enumerate(row):
            if value != 0:
                goal_i, goal_j = goal_positions[value]  # Get the goal position of the tile
                sum_manhattan_distance += abs(i - goal_i) + abs(j - goal_j)  # Add the distance to the total

    return sum_manhattan_distance  # Output: Total Manhattan distance


# Node class to represent a state in the search tree
class Node:
    def __init__(self, puzzle, level, function_for_heuristic, parent):
        """
        Initializes a new node in the search tree.

        Input:
            - puzzle: A 3x3 array (list of lists) representing the current state of the puzzle.
            - level: The depth level of the node in the search tree.
            - function_for_heuristic: A heuristic function (e.g., Hamming or Manhattan) to calculate the heuristic.
            - parent: The parent node from which this node was created.

        Output:
            - A Node object that stores the puzzle, level, heuristic value, and parent.
        """
        self.puzzle = puzzle
        self.level = level  # Depth of the node in the search tree
        self.function_for_heuristic = function_for_heuristic
        self.parent_node = parent

        if function_for_heuristic is not None and puzzle is not None:
            self.heuristic_value_of_the_puzzle = function_for_heuristic(puzzle)
        else:
            self.heuristic_value_of_the_puzzle = None

        if self.level is not None and self.heuristic_value_of_the_puzzle is not None:
            self.f = self.level + self.heuristic_value_of_the_puzzle  # f = g + h (f-value)
        else:
            self.f = None

    def __lt__(self, other):
        """Comparing f-values of two nodes to be used by heapq (priority queue)"""
        return self.f < other.f

    def to_hashable(self):
        """Converts the puzzle into a hashable tuple of tuples for easier comparison"""
        return tuple(tuple(row) for row in self.puzzle)


# SolutionNode class that extends Node to store additional information after reaching the solution
class SolutionNode(Node):
    def __init__(self, node, time_to_solve, heapq_memory_usage, number_of_expanded_nodes):
        """
        Extends Node to store additional information after solving the puzzle.

        Input:
            - node: The Node object that contains the puzzle state, level, and heuristic value.
            - time_to_solve: The time taken to solve the puzzle.
            - heapq_memory_usage: The memory usage of the heapq during the search.
            - number_of_expanded_nodes: The number of nodes that were expanded during the search.

        Output:
            - A SolutionNode object containing the puzzle solution and additional statistics.
        """
        super().__init__(node.puzzle, node.level, node.function_for_heuristic, node.parent_node)
        self.time_to_solve_till_goal_node = time_to_solve
        self.heapq_memory_usage = heapq_memory_usage
        self.number_of_expanded_nodes = number_of_expanded_nodes


# Function to create child nodes from a parent node (possible next states)
def create_child_nodes(parent_node):
    """
    Generates child nodes by making valid moves (up, down, left, right) from the current state.

    Input:
        - parent_node: The current Node object that contains the puzzle state.

    Output:
        - A list of Node objects representing all possible next states.
    """
    child_nodes_list = []  # List to store child nodes
    temp_puzzle_list = []  # Temporary list to store generated puzzles
    row_pos_empty_field, col_pos_empty_field = pos_in_puzzle(0, parent_node.puzzle)  # Find empty space (0)

    # Check the possible moves (up, down, left, right) and generate the child nodes
    if row_pos_empty_field > 0:
        temp_puzzle = copy_puzzle(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field - 1][col_pos_empty_field] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field - 1][
            col_pos_empty_field]
        child_nodes_list.append(
            Node(temp_puzzle, parent_node.level + 1, parent_node.function_for_heuristic, parent_node))

    if row_pos_empty_field < 2:
        temp_puzzle = copy_puzzle(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field + 1][col_pos_empty_field] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field + 1][
            col_pos_empty_field]
        child_nodes_list.append(
            Node(temp_puzzle, parent_node.level + 1, parent_node.function_for_heuristic, parent_node))

    if col_pos_empty_field > 0:
        temp_puzzle = copy_puzzle(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field][col_pos_empty_field - 1] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field][
            col_pos_empty_field - 1]
        child_nodes_list.append(
            Node(temp_puzzle, parent_node.level + 1, parent_node.function_for_heuristic, parent_node))

    if col_pos_empty_field < 2:
        temp_puzzle = copy_puzzle(parent_node.puzzle)
        temp_puzzle[row_pos_empty_field][col_pos_empty_field + 1] = 0
        temp_puzzle[row_pos_empty_field][col_pos_empty_field] = parent_node.puzzle[row_pos_empty_field][
            col_pos_empty_field + 1]
        child_nodes_list.append(
            Node(temp_puzzle, parent_node.level + 1, parent_node.function_for_heuristic, parent_node))

    return child_nodes_list  # Output: List of child nodes


def pretty_print(puzzle):
    """
    Prints the puzzle in a human-readable format.

    Input:
        - puzzle (2D list): The puzzle to print, represented as a 2D list of integers.

    Output:
        - Prints the puzzle to the console row by row.
    """
    if puzzle is None:
        print("pretty_print not possible because puzzle is none")
        return

    for row in puzzle:
        print(row)  # Prints each row of the puzzle


def solve_puzzle(puzzle_as_node, visited_nodes_set, heapq_for_unvisited, is_in_heapq_set):
    """
    Solves the puzzle using the A* algorithm (best-first search).

    Input:
        - puzzle_as_node (Node): The starting node that contains the current puzzle state.
        - visited_nodes_set (set): A set of already visited nodes to avoid revisiting.
        - heapq_for_unvisited (heapq): A priority queue used to store the unvisited nodes.
        - is_in_heapq_set (set): A set used to check if a node is already in the heap (prevents duplicates).

    Output:
        - solution (SolutionNode): A SolutionNode containing the solution to the puzzle, time taken to solve, memory usage, and number of expanded nodes.
    """
    start_time = time.time()
    current_node = puzzle_as_node
    expanded_node_count = 0

    while current_node.heuristic_value_of_the_puzzle != 0:  # Until the goal state is reached
        visited_nodes_set.add(current_node.to_hashable())  # Mark the current node as visited

        temp_child_nodes = create_child_nodes(current_node)  # Generate child nodes from the current node

        for child_node in temp_child_nodes:
            hashed_child_node = child_node.to_hashable()  # Create a hashable version of the child node
            # If the child node hasn't been visited or is not in the heap, add it to the heap
            if hashed_child_node not in visited_nodes_set and hashed_child_node not in is_in_heapq_set:
                heapq.heappush(heapq_for_unvisited, child_node)
                is_in_heapq_set.add(hashed_child_node)
                expanded_node_count += 1  # Increment the expanded nodes counter

        current_node = heapq.heappop(heapq_for_unvisited)  # Pop the node with the lowest f value from the heap

    time_to_solve = time.time() - start_time  # Calculate the time it took to solve the puzzle
    solution = SolutionNode(current_node, time_to_solve, None,
                            expanded_node_count)  # Create a SolutionNode with statistics
    return solution


def init_solve_one_puzzle(puzzle, heuristic_function, with_console_output, with_heapq_memory):
    """
    Initializes the solution process for a single puzzle.

    Input:
        - puzzle (2D list): The starting puzzle state.
        - heuristic_function (function): The heuristic function to be used (e.g., Manhattan or Hamming).
        - with_console_output (bool): Whether to print the solution process to the console.
        - with_heapq_memory (bool): Whether to track and print memory usage of the heapq.

    Output:
        - solution_node (SolutionNode): The node containing the solution, including time taken, memory usage, and expanded nodes.
    """
    puzzle_as_node = Node(puzzle, 0, heuristic_function, None)  # Convert the puzzle into a Node object
    if with_console_output:
        print("!!!!!!!!!!!!!START!!!!!!!!!!!!!!")
        print(puzzle_as_node.function_for_heuristic)  # Print the heuristic function used
        pretty_print_puzzle_node(puzzle_as_node)  # Print the starting puzzle state

    if not check_if_solvable(puzzle_as_node.puzzle):  # Check if the puzzle is solvable
        print("not solvable")
        return

    heapq_for_nodes = []  # Initialize an empty priority queue (heap)
    visited_nodes_set = set()  # Set to track visited nodes
    set_is_in_heapq = set()  # Set to track nodes in the heap

    solution_node = solve_puzzle(puzzle_as_node, visited_nodes_set, heapq_for_nodes,
                                 set_is_in_heapq)  # Solve the puzzle
    if with_heapq_memory:
        heapq_memory_usage = asizeof.asizeof(heapq_for_nodes)  # Measure the memory usage of the heapq
        solution_node.heapq_memory_usage = heapq_memory_usage  # Store the memory usage in the solution node

    if with_console_output:
        print("**********************************************************************")
        print_solution(solution_node)  # Print the solution
        print(f"Time: {solution_node.time_to_solve_till_goal_node:.6f} seconds")  # Print the time to solve
        if with_heapq_memory:
            print(f"heapq memory usage: {heapq_memory_usage} Bytes")  # Print the memory usage

    return solution_node


def pretty_print_puzzle_node(puzzle_as_a_node):
    """
    Prints a puzzle node with additional information.

    Input:
        - puzzle_as_a_node (Node): The node containing the puzzle state, heuristic value, and other attributes.

    Output:
        - Prints the puzzle and node attributes such as level, heuristic value, and f value.
    """
    print("----------------")
    pretty_print(puzzle_as_a_node.puzzle)  # Print the puzzle
    print("level: ", puzzle_as_a_node.level)  # Print the level of the node (number of moves)
    print("heuristic value: ", puzzle_as_a_node.heuristic_value_of_the_puzzle)  # Print the heuristic value
    print("f: ", puzzle_as_a_node.f)  # Print the f value (sum of level and heuristic value)
    print("---------------")


def print_solution(solution_as_a_node):
    """
    Recursively prints the solution path from the goal to the start.

    Input:
        - solution_as_a_node (SolutionNode): The solution node, containing the path to the solution.

    Output:
        - Prints the solution path from the goal node to the start node.
    """
    pretty_print_puzzle_node(solution_as_a_node)  # Print the current node in the solution

    if solution_as_a_node.parent_node is None:  # If there is no parent, we've reached the start
        return

    print_solution(solution_as_a_node.parent_node)  # Recursively print the parent node (previous step in the solution)


def creat_100_solvable_puzzles():
    """
    Generates a list of 100 solvable puzzles.

    Output:
        - list_of_100_puzzles (list): A list containing 100 solvable 2D puzzles.
    """
    list_of_100_puzzles = []

    while len(list_of_100_puzzles) != 100:
        temp_puzzle = create_random_puzzle()  # Generate a random puzzle
        if check_if_solvable(temp_puzzle):  # Check if it is solvable
            list_of_100_puzzles.append(temp_puzzle)  # Add to the list if solvable

    return list_of_100_puzzles


def solve_list_of_puzzles(solvable_puzzle_list, heuristic_function, list_of_times_for_each_puzzle_in_sec,
                          list_of_memory_for_each_puzzle_in_bytes, list_of_expanded_nodes_for_each_puzzle,
                          with_heapq_memory):
    """
    Solves a list of puzzles and stores statistics for each one.

    Input:
        - solvable_puzzle_list (list): A list of solvable puzzles (2D lists).
        - heuristic_function (function): The heuristic function to be used.
        - list_of_times_for_each_puzzle_in_sec (list): List to store time taken for each puzzle.
        - list_of_memory_for_each_puzzle_in_bytes (list): List to store memory usage for each puzzle.
        - list_of_expanded_nodes_for_each_puzzle (list): List to store the number of expanded nodes for each puzzle.
        - with_heapq_memory (bool): Whether to track memory usage of the heapq during solving.

    Output:
        - Adds statistics for each puzzle to the respective lists.
    """
    total_start_time = time.time()  # Start timing the total process

    for current_puzzle in solvable_puzzle_list:
        current_solution_node = init_solve_one_puzzle(current_puzzle, heuristic_function, False,
                                                      with_heapq_memory)  # Solve each puzzle
        current_heapq_memory = current_solution_node.heapq_memory_usage  # Get memory usage for the heap
        current_solution_time = current_solution_node.time_to_solve_till_goal_node  # Get the time taken to solve the puzzle
        current_expanded_nodes = current_solution_node.number_of_expanded_nodes  # Get the number of expanded nodes

        list_of_memory_for_each_puzzle_in_bytes.append(current_heapq_memory)  # Add memory usage to list
        list_of_times_for_each_puzzle_in_sec.append(current_solution_time)  # Add time to list
        list_of_expanded_nodes_for_each_puzzle.append(current_expanded_nodes)  # Add expanded nodes count to list

    print("Total time: ", time.time() - total_start_time, " sec")  # Print total time taken to solve all puzzles


def calc_mean(list_of_numbers):
    """
    Calculates the mean (average) of a list of numbers.

    Input:
        - list_of_numbers (list): A list of numerical values (e.g., times, memory usage).

    Output:
        - mean (float): The mean value of the numbers in the list, calculated as the sum of all numbers divided by the count of numbers.
    """
    return sum(list_of_numbers) / len(
        list_of_numbers)  # Calculate the mean by dividing the sum by the number of elements


def calc_variance(mean, list_of_numbers):
    """
    Calculates the variance of a list of numbers based on the provided mean.

    Input:
        - mean (float): The mean (average) value of the numbers, used to calculate the variance.
        - list_of_numbers (list): A list of numerical values (e.g., times, memory usage).

    Output:
        - variance (float): The variance, which measures the spread or dispersion of the numbers around the mean.
                             It is calculated by averaging the squared differences between each number and the mean.
    """
    return sum((x - mean) ** 2 for x in list_of_numbers) / len(list_of_numbers)  # Calculate variance using the formula
