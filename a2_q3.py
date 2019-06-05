''' Cmpt 310 assignment 2 question 3
	Created by Liam Ling
	Date: Sun Jun 2 2019'''

from csp import * # import csp module
from a2_q1 import * # import rand_graph function
from time import time # for tracking running time
from itertools import * # for calculating possible combinations of backtracking parameters

def run_q3():
	print("initializing...")
	variables = [i for i in range(30)]
	graphs = [rand_graph(30, 0.1), rand_graph(30, 0.2), rand_graph(30, 0.3),
          rand_graph(30, 0.4), rand_graph(30, 0.5)]

	# # for testing purpose
	# c = ["r","g","b","y","d"]
	# g = {0:[2,4], 1:[2,4], 2:[0,1,3], 3:[2,4], 4:[0,3]}

	for run in range(5):
		print("run ", run+1, ":")
		for index in range(len(graphs)):
			print("start solving graph [", index+1, "]", "...")
			colored_map = MapColoringCSP(variables, graphs[index])
			# print(colored_map.variables)
			# print(colored_map.domains)
			# print(colored_map.neighbors)
			# print(colored_map.constraints)
			
			variable_ordering = [first_unassigned_variable, mrv]
			value_ordering = [unordered_domain_values, lcv]
			inference = [no_inference, forward_checking, mac]

			backtracking_parameters = [combination] for combination in product(variable_ordering, value_ordering, inference)

			'''
			# solving process
			# default
			start_time = time()
			result1 = backtracking_search(colored_map)
			elapsed_time_default = time() - start_time
			elapsed_time_fun = elapsed_time_default

			assignment = colored_map.nassigns
			unassignment = len(result1) - colored_map.nassigns

			# The default variable order, The default value order, forward checking
			start_time = time()
			result2 = backtracking_search(colored_map, first_unassigned_variable, unordered_domain_values, forward_checking)
			elapsed_time_fuf = time() - start_time

			# The default variable order, The default value order, Maintain arc consistency
			start_time = time()
			result3 = backtracking_search(colored_map, first_unassigned_variable, unordered_domain_values, mac)
			elapsed_time_fum = time() - start_time
			
			# The default variable order, Least-constraining-values heuristic, no inference
			start_time = time()
			result4 = backtracking_search(colored_map, first_unassigned_variable, lcv, no_inference)
			elapsed_time_fln = time() - start_time

			# The default variable order, Least-constraining-values heuristic, forward checking
			start_time = time()
			result5 = backtracking_search(colored_map, first_unassigned_variable, lcv, forward_checking)
			elapsed_time_flf = time() - start_time

			# The default variable order, Least-constraining-values heuristic, Maintain arc consistency
			start_time = time()
			result6 = backtracking_search(colored_map, first_unassigned_variable, lcv, mac)
			elapsed_time_flm = time() - start_time

			# Minimum-remaining-values heuristic, Least-constraining-values heuristic, Maintain arc consistency
			start_time = time()
			result7 = backtracking_search(colored_map, mrv, lcv, mac)
			elapsed_time_mlm = time() - start_time

			number_of_teams = len(set(result1.values()))

			print("solution of graph [", index+1, "]: ", result1)
			print("number of teams: ", number_of_teams)
			print("running time of all default  : ", elapsed_time_fun)
			print("running time of fuv, udv, fc : ", elapsed_time_fuf)
			print("running time of fuv, udv, mac: ", elapsed_time_fum)
			print("running time of fuv, lcv, noi: ", elapsed_time_fln)
			print("running time of fuv, lcv, fc : ", elapsed_time_flf)
			print("running time of fuv, lcv, mac: ", elapsed_time_flm)
			print("count of assignment times: ", assignment)
			print("count of unassignment times: ", unassignment)
			print("\n")
			'''

run_q3()