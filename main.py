import math
import puzzle

# Keep the rest of your puzzle-related code here (e.g., puzzle creation, initialization)

# Define the list of solvable puzzles
list_of_100_solvable_puzzles = puzzle.creat_100_solvable_puzzles()


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
        puzzle_function,
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


def select_heuristic():
    print("Select a heuristic:")
    print("1. Manhattan Distance")
    print("2. Hamming Distance")
    print("3. Both")
    choice = input("Enter your choice (1/2/3): ").strip()
    if choice == "1":
        return puzzle.calc_manhattan_distance
    elif choice == "2":
        return puzzle.calc_hamming
    elif choice == "3":
        return None  # Will run both heuristics
    else:
        print("Invalid choice, defaulting to Manhattan Distance.")
        return puzzle.calc_manhattan_distance


def select_number_of_puzzles():
    print("Select number of puzzles:")
    print("1. Solve 1 puzzle")
    print("2. Solve 100 puzzles")
    choice = input("Enter your choice (1/2): ").strip()
    return 1 if choice == "1" else 100


def run_program():
    # Ask user for puzzle settings
    heuristic_function = select_heuristic()
    num_puzzles = select_number_of_puzzles()

    if heuristic_function == None:
        # If both heuristics are selected, run both
        print("Solving puzzles with Manhattan Distance:")
        solve_and_print_results(
            puzzle_function=list_of_100_solvable_puzzles[:num_puzzles],
            with_heapq_memory=False,
            heuristic_function=puzzle.calc_manhattan_distance,
            title="solve puzzles with Manhattan"
        )

        print("Solving puzzles with Hamming Distance:")
        solve_and_print_results(
            puzzle_function=list_of_100_solvable_puzzles[:num_puzzles],
            with_heapq_memory=False,
            heuristic_function=puzzle.calc_hamming,
            title="solve puzzles with Hamming"
        )
    else:
        # If only one heuristic is selected
        solve_and_print_results(
            puzzle_function=list_of_100_solvable_puzzles[:num_puzzles],
            with_heapq_memory=False,
            heuristic_function=heuristic_function,
            title=f"solve {num_puzzles} puzzles with selected heuristic"
        )


def ask_to_run_again():
    print("Do you want to run the program again?")
    print("1. Yes")
    print("2. No")
    choice = input("Enter your choice (1/2): ").strip()
    return choice == "1"


def main():
    # Main loop to allow the user to restart or exit
    while True:
        run_program()

        if not ask_to_run_again():
            print("Thank you for using the program. Exiting...")
            break


if __name__ == "__main__":
    main()
