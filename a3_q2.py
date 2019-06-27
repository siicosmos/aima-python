''' 
Cmpt 310 assignment 3 question 1 
Created by Liam Ling
Date: Mon June 24 2019
'''

from itertools import combinations # for generating combinations of a subset of clause candidates
import math # for ceil function
import random # for testing probability
import subprocess # for exexcuting commands in terminal
import csv # for saving data
import io # for writing data

CNF_file_name = 'sat-ice.txt'
SAT_output_file_name = 'out-ice.txt'
DATA_file = 'data-ice.csv'
n = 12 # define the number of nodes in friendship graph
p = 0.0
run = 10

# following code is from assignment 2
def rand_graph(n, p):
	print('Generating friendship graph ('+str(n)+', '+str(p)+')')
	edges = []
	graph = {i:[] for i in range(1, n+1)} # create the defalut graph
	for i in range(1, n+1):
		for j in range(1, i): 
			if random.random() < p: # with probability p append edges to edges
				edges.append((i, j))

	for (i, j) in edges:
		if j not in graph[i]: # check if the edge already exist
			graph[i].append(j)
		if i not in graph[j]: # check if the edge already exist
			graph[j].append(i)
	print('Complete')
	return graph

#rand_graph(5, 0.5)

# this function generate a dictionary that maps a variable to a number
def creat_variable_dic(variables):
	return {variables[i-1]:str(i) for i in range(1, len(variables)+1)}

def make_ice_breaker_sat(graph, k):
	print('Generating friendship graph SAT string with ' + str(k) + ' colors')
	nodes = [i for i in range(1, n+1)]
	colors = [c for c in range(k)]
	constrains = []
	variables = []
	clauses_string = ''
	number_of_clauses = 0
	with io.open(CNF_file_name, 'w') as sat_file:
		# get all the constrains (edges)
		for node, neighbors in graph.items():
			for neighbor in neighbors:
				constrain = []
				constrain.append(node)
				constrain.append(neighbor)
				constrain.sort()
				if constrain not in constrains:
					constrains.append(constrain)
		#print(constrains)
		# get all the possible sat variables and create a dict maps numbers to all variables
		for node in nodes:
			for color in colors:
				variables.append((node, color))
		variable_dic = creat_variable_dic(variables)
		#print(variables, '\n')
		#print(variable_dic, '\n')

		# create a string of clauses
		# type 1 clause: adjacent clauses cannot have the same color
		for constrain in constrains:
			for color in colors:
				clauses_string += '-' + variable_dic.get((constrain[0], color)) + ' -' + variable_dic.get((constrain[1], color)) + ' 0\n'
				number_of_clauses += 1

		# type 2 clause: a node must not be left uncolored
		for node in nodes:
			for color in colors:
				clauses_string += variable_dic.get((node, color))
				if len(colors) != 1 and color != colors[-1]:
					clauses_string += ' '
			clauses_string += ' 0\n'
			number_of_clauses += 1
			if k > 2:
				for combination in combinations(colors, 2):
					clauses_string += '-' + variable_dic.get((node, list(combination)[0])) + ' -' + variable_dic.get((node, list(combination)[1])) + ' 0\n'
					number_of_clauses += 1

		# type 3 clause: a node cannot have more than 1 color
		if k > 2:
			for node in nodes:
				for combination in combinations(colors, 2):
					clauses_string += '-' + variable_dic.get((node, list(combination)[0])) + ' -' + variable_dic.get((node, list(combination)[1])) + ' 0\n'
					number_of_clauses += 1
		elif k == 1:
			for node in nodes:
				clauses_string += '-' + variable_dic.get((node, colors[0])) + ' 0\n'
				number_of_clauses += 1
		else:
			for node in nodes:
				clauses_string += '-' + variable_dic.get((node, colors[0])) + ' -' + variable_dic.get((node, colors[1])) + ' 0\n'
				number_of_clauses += 1
		#print(clauses_string)

		comment = 'c ice breaker problem graph(' + str(n) +', ' + str(p) + ') (sat)\n'
		sat_solver_parameters = 'p cnf ' + str(n*k) + ' ' + str(number_of_clauses) + '\n'
		sat_file.write(comment)
		sat_file.write(sat_solver_parameters)
		sat_file.write(clauses_string)
	sat_file.close()
	print('Complete')

def find_min_teams(graph):
	# run a external script 'minisat [CNF fi0le] [output file]'

	for k in range(1, n+1, 1):
		make_ice_breaker_sat(graph, k)
		sat_process = subprocess.Popen(['minisat', CNF_file_name, SAT_output_file_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		stdout, stderr = sat_process.communicate()
		
		cpu_time = [string for string in (stdout.decode().split('\n')) if 'CPU' in string][0]
		satisfiability = [string for string in (stdout.decode().split('\n')) if 'SAT' in string][0]
		if satisfiability == 'SATISFIABLE':
			print(satisfiability, cpu_time, '\n')
			print('MINISAT find the minimum number of teams needed:', k)
			#print(stdout.decode())
			break
		else:
			print('UNSATISFIABLE')
	with io.open(DATA_file, 'a') as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow([p, k, cpu_time, satisfiability])
	csv_file.close()

def main():
	with io.open(DATA_file, 'w') as csv_file:
		field_names = ['Probability', 'Minimum Number of Teams', 'CPU Time', 'Satisfiability']
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(field_names)
	csv_file.close()
	
	for i in range(1,10):
		for j in range(run):
			probability = i/10
			global p
			p = probability
			graph = rand_graph(n, probability)
			find_min_teams(graph)
	return 0

main()
