import math

import puzzle

puzzle_with_31_steps_to_solve = [[8, 6, 7],
                                 [2, 5, 4],
                                 [3, 0, 1]]

# puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_hamming, True)

# puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_manhattan_distance, True)



# puzzle.solve_list_of_puzzles(list_of_100_solvable_puzzles, puzzle.calc_hamming, time_list_for_hamming_in_sec, memory_list_for_hamming_in_bytes)
# puzzle.solve_list_of_puzzles(list_of_100_solvable_puzzles, puzzle.calc_manhattan_distance, time_list_for_manhattan_in_sec, memory_list_for_manhattan_in_bytes)
# print(time_list_for_manhattan)
# print(memory_list_for_manhattan_in_bytes)
# print(memory_list_for_hamming_in_bytes)


list_of_100_solvable_puzzles = puzzle.creat_100_solvable_puzzles()

def format_number(num):
    return f"{num:,.6f}".replace(",", "X").replace(".", ",").replace("X", ".")

print("++++++++++*********************************************++++++++++")
print()
print("solve 100 Puzzles with manhattan")

time_list_for_manhattan_in_sec = []
memory_list_for_manhattan_in_bytes = []

puzzle.solve_list_of_puzzles(
    list_of_100_solvable_puzzles,
    puzzle.calc_manhattan_distance,
    time_list_for_manhattan_in_sec,
    memory_list_for_manhattan_in_bytes
)

manhattan_mean_time = puzzle.calc_mean(time_list_for_manhattan_in_sec)
print("mean time to solve: ", format_number(manhattan_mean_time), " sec")

manhattan_time_variance = puzzle.calc_variance(manhattan_mean_time, time_list_for_manhattan_in_sec)
print("variance time: ", format_number(manhattan_time_variance), " sec")
print("standard deviation of time: ", format_number(math.sqrt(manhattan_time_variance)), " bytes")

manhattan_mean_memory_of_heap = puzzle.calc_mean(memory_list_for_manhattan_in_bytes)
print("mean memory of heap: ", format_number(manhattan_mean_memory_of_heap), " bytes")

manhattan_memory_variance = puzzle.calc_variance(manhattan_mean_memory_of_heap, memory_list_for_manhattan_in_bytes)
print("variance of heap ", format_number(manhattan_memory_variance), " bytes")
print("standard deviation of heap: ", format_number(math.sqrt(manhattan_memory_variance)), " bytes")
print()
print("++++++++++*********************************************++++++++++")
print()

print("solve 100 Puzzles with hamming")

time_list_for_hamming_in_sec = []
memory_list_for_hamming_in_bytes = []

puzzle.solve_list_of_puzzles(
    list_of_100_solvable_puzzles,
    puzzle.calc_hamming,
    time_list_for_hamming_in_sec,
    memory_list_for_hamming_in_bytes
)

hamming_mean_time = puzzle.calc_mean(time_list_for_hamming_in_sec)
print("mean time to solve: ", format_number(hamming_mean_time), " sec")

hamming_time_variance = puzzle.calc_variance(hamming_mean_time, time_list_for_hamming_in_sec)
print("variance time: ", format_number(hamming_time_variance), " sec")
print("standard deviation of time: ", format_number(math.sqrt(hamming_time_variance)), " bytes")

hamming_mean_memory_of_heap = puzzle.calc_mean(memory_list_for_hamming_in_bytes)
print("mean memory of heap: ", format_number(hamming_mean_memory_of_heap), " bytes")

hamming_memory_variance = puzzle.calc_variance(hamming_mean_memory_of_heap, memory_list_for_hamming_in_bytes)
print("variance of heap ", format_number(hamming_memory_variance), " bytes")
print("standard deviation of heap: ", format_number(math.sqrt(hamming_memory_variance)), " bytes")
print()
print("++++++++++*********************************************++++++++++")

