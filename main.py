import math
import puzzle

puzzle_with_31_steps_to_solve = [[8, 6, 7],
                                 [2, 5, 4],
                                 [3, 0, 1]]

puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_hamming, True)

puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_manhattan_distance, True)

list_of_100_solvable_puzzles = puzzle.creat_100_solvable_puzzles()


def format_number(num):
    return f"{num:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")


def print_centered(text, width=60):
    print(text.center(width).upper())


print("++++++++++*********************************************++++++++++")
print()
print_centered("solve 100 puzzles with manhattan")
print()

time_list_for_manhattan_in_sec = []
memory_list_for_manhattan_in_bytes = []

puzzle.solve_list_of_puzzles(
    list_of_100_solvable_puzzles,
    puzzle.calc_manhattan_distance,
    time_list_for_manhattan_in_sec,
    memory_list_for_manhattan_in_bytes
)

manhattan_mean_time = puzzle.calc_mean(time_list_for_manhattan_in_sec)
manhattan_time_variance = puzzle.calc_variance(manhattan_mean_time, time_list_for_manhattan_in_sec)
manhattan_std_time = math.sqrt(manhattan_time_variance)

manhattan_mean_memory_of_heap = puzzle.calc_mean(memory_list_for_manhattan_in_bytes)
manhattan_memory_variance = puzzle.calc_variance(manhattan_mean_memory_of_heap, memory_list_for_manhattan_in_bytes)
manhattan_std_memory = math.sqrt(manhattan_memory_variance)
print()
print(f"Average time to solve puzzle:         {format_number(manhattan_mean_time)} sec")
print(f"Variance in solving times:            {format_number(manhattan_time_variance)} sec²")
print(f"Standard deviation of solving times:  {format_number(manhattan_std_time)} sec")
print(f"Average heap memory usage:            {format_number(manhattan_mean_memory_of_heap)} bytes")
print(f"Variance in heap memory usage:        {format_number(manhattan_memory_variance)} bytes²")
print(f"Standard deviation of heap memory:    {format_number(manhattan_std_memory)} bytes")
print()
print("++++++++++*********************************************++++++++++")
print()

print_centered("solve 100 puzzles with hamming")
print()

time_list_for_hamming_in_sec = []
memory_list_for_hamming_in_bytes = []

puzzle.solve_list_of_puzzles(
    list_of_100_solvable_puzzles,
    puzzle.calc_hamming,
    time_list_for_hamming_in_sec,
    memory_list_for_hamming_in_bytes
)

hamming_mean_time = puzzle.calc_mean(time_list_for_hamming_in_sec)
hamming_time_variance = puzzle.calc_variance(hamming_mean_time, time_list_for_hamming_in_sec)
hamming_std_time = math.sqrt(hamming_time_variance)

hamming_mean_memory_of_heap = puzzle.calc_mean(memory_list_for_hamming_in_bytes)
hamming_memory_variance = puzzle.calc_variance(hamming_mean_memory_of_heap, memory_list_for_hamming_in_bytes)
hamming_std_memory = math.sqrt(hamming_memory_variance)
print()
print(f"Average time to solve puzzle:         {format_number(hamming_mean_time)} sec")
print(f"Variance in solving times:            {format_number(hamming_time_variance)} sec²")
print(f"Standard deviation of solving times:  {format_number(hamming_std_time)} sec")
print(f"Average heap memory usage:            {format_number(hamming_mean_memory_of_heap)} bytes")
print(f"Variance in heap memory usage:        {format_number(hamming_memory_variance)} bytes²")
print(f"Standard deviation of heap memory:    {format_number(hamming_std_memory)} bytes")
print()
print("++++++++++*********************************************++++++++++")
