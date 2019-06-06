''' 
Cmpt 310 assignment 2 question 4
Created by Liam Ling
Date: Wed Jun 5 2019
Description: this function will auto-generate a CSV file containing all data
			 the same method is used to solve graph[100,0.1] ~ graph[100,0.5]
			 since there is no significant influence on the solving time, the method is unchanged
'''

from csp import * # import csp module
from a2_q1 import * # import rand_graph function
from a2_q2 import * # import check_teams function
from time import time # for tracking running time
from itertools import * # for calculating possible combinations of backtracking parameters
import csv # for generate CSV file

def run_q4():
	print("initializing...")
	variables = [i for i in range(100)]
	graphs = [rand_graph(100, 0.1), rand_graph(100, 0.2), rand_graph(100, 0.3), 
				rand_graph(100, 0.4), rand_graph(100, 0.5)]

	# get all possible combinations of backtracking parameters
	variable_ordering = [first_unassigned_variable, mrv]
	value_ordering = [unordered_domain_values, lcv]
	inference = [no_inference, forward_checking, mac]
	backtracking_parameter_combinations = list(product(variable_ordering, value_ordering, inference))
	backtracking_parameter_combinations_name = []

	# create a csv file for recording data
	csv_file = open("a2_q4.csv", "w")
	writer = csv.writer(csv_file)

	# # for testing purpose
	# c = ["r","g","b","y","d"]
	# g = {0:[2,4], 1:[2,4], 2:[0,1,3], 3:[2,4], 4:[0,3]}

	for run in range(5):
		run_str = "run " + str(run+1)
		print(run_str + ":")
		writer.writerow([run_str])

		run_data = [0.0] * len(backtracking_parameter_combinations) # for storinng average time for each backtracking parameter combination
		for index in range(len(graphs)):
			graph_str = "graph [100," + str((index+1)/10) + "]"
			print("start solving", graph_str, "...")
			writer.writerow([graph_str])
			# for storing solutions
			results = []
			colored_map = MapColoringCSP(variables, graphs[index])
			# print(colored_map.variables)
			# print(colored_map.domains)
			# print(colored_map.neighbors)
			# print(colored_map.constraints)

			# solving process
			for combination in backtracking_parameter_combinations:
				combination_index = backtracking_parameter_combinations.index(combination)

				start_time = time()
				result = backtracking_search(colored_map, combination[0], combination[1], combination[2])
				elapsed_time = time() - start_time

				number_of_teams = len(set(result.values()))
				assignment = colored_map.nassigns 
				unassignment = len(variables) - assignment
				colored_map.nassigns = 0
				correctness = check_teams(graphs[index], result)
				combination_name = ", ".join(func.__name__ for func in combination)

				results.append([combination_name, number_of_teams, elapsed_time, assignment, unassignment, result, correctness])
				run_data[combination_index] = run_data[combination_index] + elapsed_time
				if len(backtracking_parameter_combinations_name) != len(backtracking_parameter_combinations):
					backtracking_parameter_combinations_name.append(combination_name)

			total_time = 0.0
			minimum = ["", results[0][2]]
			maximum = ["", results[0][2]]
			print("number of teams: ", results[0][1])
			for combination in backtracking_parameter_combinations:
				idx = backtracking_parameter_combinations.index(combination)
				total_time = total_time + results[idx][2]
				minimum = [", ".join(func.__name__ for func in combination), results[idx][2]] if minimum[1] > results[idx][2] else minimum
				maximum = [", ".join(func.__name__ for func in combination), results[idx][2]] if maximum[1] < results[idx][2] else maximum
				print("running time of combination ", ", ".join(func.__name__ for func in combination), ":\n", results[idx][2])
			print("count of assignment times: ", results[0][3])
			print("count of unassignment times: ", results[0][4])
			print("solution of graph [", index+1, "]: ", results[0][5])
			print("solution is", "correct" if results[0][6] else "wrong")
			print("\n")

			# record data
			writer.writerow(["backtraing parameter combination", "number of teams", "elapsed time", "assignment times", "unassignment times", "result", "correctness"])
			writer.writerows(results)
			writer.writerow([run_str + " " + graph_str + " average time", "fastest combination", "fastest time", "slowest combination", "slowest time"])
			writer.writerow([total_time/len(backtracking_parameter_combinations), minimum[0], minimum[1], maximum[0], maximum[1]])
		writer.writerow([run_str + " combinations average time:"])
		writer.writerows(list(zip(backtracking_parameter_combinations_name, run_data)))
	csv_file.close()
	print("All data saving to the same path, file name: a2_q3.csv")

# uncomment to run
run_q4()