''' Cmpt 310 assignment 2 question 3
	Created by Liam Ling
	Date: Sun Jun 2 2019'''

from csp import * # import csp module
from a2_q1 import * # import rand_graph function
from a2_q2 import * # import check_teams function
from time import time # for tracking running time
from itertools import * # for calculating possible combinations of backtracking parameters
import csv

def run_q3():
	print("initializing...")
	variables = [i for i in range(30)]
	graphs = [rand_graph(30, 0.1), rand_graph(30, 0.2), rand_graph(30, 0.3), 
				rand_graph(30, 0.4), rand_graph(30, 0.5)]

	# get all possible combinations of backtracking parameters
	variable_ordering = [first_unassigned_variable, mrv]
	value_ordering = [unordered_domain_values, lcv]
	inference = [no_inference, forward_checking, mac]
	backtraing_parameter_combinations = list(product(variable_ordering, value_ordering, inference))

	# create a csv file for recording data
	csv_file = open("a2_q3.csv", "wb")

	# # for testing purpose
	# c = ["r","g","b","y","d"]
	# g = {0:[2,4], 1:[2,4], 2:[0,1,3], 3:[2,4], 4:[0,3]}

	for run in range(5):
		print("run ", run+1, ":")
		for index in range(len(graphs)):
			print("start solving graph [", index+1, "]", "...")
			# for storing solutions
			results = []
			colored_map = MapColoringCSP(variables, graphs[index])
			# print(colored_map.variables)
			# print(colored_map.domains)
			# print(colored_map.neighbors)
			# print(colored_map.constraints)

			# solving process
			for combination in backtraing_parameter_combinations:
				start_time = time()
				result = backtracking_search(colored_map, combination[0], combination[1], combination[2])
				elapsed_time = time() - start_time
				number_of_teams = len(set(result.values()))
				assignment = colored_map.nassigns 
				unassignment = len(variables) - assignment
				colored_map.nassigns = 0
				correctness = check_teams(graphs[index], result)

				results.append([number_of_teams, elapsed_time, assignment, unassignment, result, correctness])

			print("number of teams: ", results[0][0])
			for combination in backtraing_parameter_combinations:
				idx = backtraing_parameter_combinations.index(combination)
				print("running time of combination ", ", ".join(func.__name__ for func in combination), ":\n", results[idx][1])
			print("count of assignment times: ", results[0][2])
			print("count of unassignment times: ", results[0][3])
			print("solution of graph [", index+1, "]: ", results[0][4])
			print("solution is", "correct" if results[0][5] else "wrong")
			print("\n")

			# record data
			writer = csv.writer(csv_file)
			writer = wrirerow(["number_of_teams", "elapsed_time", "assignment", "unassignment", "result", "correctness"])
			writer = wrirerows(results)

run_q3()