import puzzle

puzzle_with_31_steps_to_solve = [[8, 6, 7],
                                 [2, 5, 4],
                                 [3, 0, 1]]

puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_hamming, True)

# puzzle.init_solve_one_puzzle(puzzle.create_random_puzzle(), puzzle.calc_manhattan_distance, True)

list_of_100_solvable_puzzles = puzzle.creat_100_solvable_puzzles()

time_list_for_hamming = []
time_list_for_manhattan = []

#puzzle.solve_list_of_puzzles(list_of_100_solvable_puzzles, puzzle.calc_hamming, time_list_for_hamming)
#puzzle.solve_list_of_puzzles(list_of_100_solvable_puzzles, puzzle.calc_manhattan_distance, time_list_for_manhattan)
#print(time_list_for_manhattan)