import math
import puzzle

puzzle_with_31_steps_to_solve = [[8, 6, 7],
                                 [2, 5, 4],
                                 [3, 0, 1]]

puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_hamming, True, False)

puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_manhattan_distance, True, False)


def format_number(num):
    return f"{num:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")


def print_centered(text, width=60):
    print(text.center(width).upper())


def solve_and_print_results(puzzle_function, with_heapq_memory, heuristic_function, title):
    print("++++++++++*********************************************++++++++++")
    print()
    print_centered(title)
    print()

    time_list = []
    memory_list = []
    expanded_nodes_list = []

    # Solve the puzzles
    puzzle.solve_list_of_puzzles(
        list_of_100_solvable_puzzles,
        heuristic_function,
        time_list,
        memory_list,
        expanded_nodes_list,
        with_heapq_memory
    )

    # Calculate statistics
    mean_time = puzzle.calc_mean(time_list)
    time_variance = puzzle.calc_variance(mean_time, time_list)
    std_time = math.sqrt(time_variance)

    mean_expanded_nodes = puzzle.calc_mean(expanded_nodes_list)
    expanded_nodes_variance = puzzle.calc_variance(mean_expanded_nodes, expanded_nodes_list)
    std_expanded_nodes = math.sqrt(expanded_nodes_variance)

    if with_heapq_memory:
        mean_memory = puzzle.calc_mean(memory_list)
        memory_variance = puzzle.calc_variance(mean_memory, memory_list)
        std_memory = math.sqrt(memory_variance)

    # Print results
    print(f"Average time to solve puzzle:         {format_number(mean_time)} sec")
    print(f"Variance in solving times:            {format_number(time_variance)} sec²")
    print(f"Standard deviation of solving times:  {format_number(std_time)} sec")

    print(f"Average expanded nodes:               {format_number(mean_expanded_nodes)} nodes")
    print(f"Variance in expanded nodes:           {format_number(expanded_nodes_variance)} nodes²")
    print(f"Standard deviation expanded nodes:    {format_number(std_expanded_nodes)} nodes")

    if with_heapq_memory:
        print(f"Average heapq memory usage:           {format_number(mean_memory)} bytes")
        print(f"Variance in heapq memory usage:       {format_number(memory_variance)} bytes²")
        print(f"Standard deviation of heapq memory:   {format_number(std_memory)} bytes")
    print()
    print("++++++++++*********************************************++++++++++")
    print()


# Define the list of solvable puzzles
list_of_100_solvable_puzzles = puzzle.creat_100_solvable_puzzles()

# Solve puzzles using Manhattan distance
solve_and_print_results(with_heapq_memory=False, puzzle_function=list_of_100_solvable_puzzles, heuristic_function=puzzle.calc_manhattan_distance,
                        title="solve 100 puzzles with manhattan")

# Solve puzzles using Hamming distance
solve_and_print_results(with_heapq_memory=False, puzzle_function=list_of_100_solvable_puzzles, heuristic_function=puzzle.calc_hamming,
                        title="solve 100 puzzles with hamming")
