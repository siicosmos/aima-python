''' 
Cmpt 310 assignment 3 question 1 
Created by Liam Ling
Date: Mon June 24 2019
'''

import subprocess # for exexcuting commands in terminal
from itertools import combinations, islice # for generating combinations of a subset of clause candidates
import math # for ceil, sqrt function
import csv # for saving data

CNF_file_name = 'sat-test.txt'
SAT_output_file_name = 'out.txt'
DATA_file = 'data.csv'
MAX_N = 70

def add_minus_sign(string):
	string = '-' + string
	return string

def chunk_list(sample_list, size):
	sample_list = iter(sample_list)
	return iter(lambda: tuple(islice(sample_list, size)), ())

def transpose_list(sample_list):
	return list(map(list, zip(*sample_list)))

def extend_clause_set(clauses, clause_set, tiled):
	for clause in clauses:
		if tiled == 0:
			clause_set.append(' '.join(map(str, clause)) + ' 0')
		for combination in combinations(clause, 2):
			clause_set.append(' '.join(map(add_minus_sign, map(str, list(combination)))) + ' 0')

# tile_direction == 1 for calculating right tile elements, otherwise, for calculating left tile elements
def extend_tile_clause(diagonal_clauses, element_set, board_side, tile_direction):
	for index in range(math.ceil(len(element_set)/2)):
		element1 = element_set[index]
		element2 = element_set[-index-1]
		if element1 != element2:
			if tile_direction == 1:
				diagonal_clauses.append([i for i in range(element1, (element1-1)*board_side+element1, board_side-1)])
				diagonal_clauses.append([i for i in range(element2, (element1-1)*board_side+element2, board_side-1)])
			else:
				diagonal_clauses.append([i for i in range(element1, (index+2)*board_side+1, board_side+1)])
				diagonal_clauses.append([i for i in range(element2, ((index+2)*board_side+1-element1)+element2, board_side+1)])
		else:
			if tile_direction == 1:
				diagonal_clauses.append([i for i in range(element1, (element1-1)*board_side+element1, board_side-1)])
			else:
				diagonal_clauses.append([i for i in range(element1, (index+2)*board_side+1, board_side+1)])

def generate_clause_set(num_of_queen):
	board_side = num_of_queen
	board_size = board_side**2
	candidates = [i for i in range(1, board_size+1)]
	clause_set = []
	# horizontal clauses
	horizontal_clauses = list(map(list, chunk_list(candidates, board_side)))
	extend_clause_set(horizontal_clauses, clause_set, 0)
	# vertical clauses
	vertical_clauses = transpose_list(horizontal_clauses)
	extend_clause_set(vertical_clauses, clause_set, 0)
	# diagonal clauses
	# calculate the first element in diagonally alignment which tiles left or right
	left_tile = [i for i in range(board_side-1, 0, -1)]
	right_tile = [i for i in range(2, board_side+1)]
	left_tile += [i for i in range(right_tile[-1]+1, board_size-board_side, board_side)]
	right_tile += [i for i in range(right_tile[-1]+board_side, board_size-1, board_side)]

	diagonal_clauses = []
	# right_tile
	extend_tile_clause(diagonal_clauses, right_tile, board_side, 1)
	# left_tile
	extend_tile_clause(diagonal_clauses, left_tile, board_side, 0)
	extend_clause_set(diagonal_clauses, clause_set, 1)
	return clause_set

def make_queen_sat(N):
	if N > MAX_N:
		print('The number of queen must be less than ', MAX_N)
	elif N < 2:
		print('The number of queen must be larger than 2')
	# create a txt file with N clauses with CNF form for feeding to minisat
	with open(CNF_file_name, 'w') as sat_file:
		clause_set = generate_clause_set(N)
		comment = 'c ' + str(N) + '-queens problem (sat)\n'
		sat_solver_parameters = 'p cnf ' + str(N**2) + ' ' + str(len(clause_set)) + '\n'
		sat_file.write(comment)
		sat_file.write(sat_solver_parameters)
		for clause in clause_set:
			sat_file.write(clause + '\n')
	# run a external script 'minisat [CNF fi0le] [output file]'
	sat_process = subprocess.Popen(['minisat', CNF_file_name, SAT_output_file_name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout, stderr = sat_process.communicate()

	nth_problem = str(N)+'-queens:'
	cpu_time = [string for string in (stdout.decode('utf-8').split('\n')) if 'CPU' in string][0]
	satisfiability = [string for string in (stdout.decode('utf-8').split('\n')) if 'SAT' in string][0]
	print(nth_problem)
	print(cpu_time)

	# save all the CPU time and satisfiability to a CVS file
	with open(DATA_file, 'a') as csv_file:
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow([nth_problem, cpu_time, satisfiability])
	'''if stderr != None:
		print(stderr)'''
	# save minisat output to output txt file
	with open(SAT_output_file_name, 'r') as output_file:
		result = output_file.read()
		# call draw_queen_sat_sol() to display the result
		draw_queen_sat_sol(result)

	sat_file.close()
	output_file.close()

def draw_queen_sat_sol(sol):
	if sol.split('\n')[0] == 'UNSAT':
		print('No solution\n')
	else:
		data = sol.split('\n')[1].split(' 0')[0].split(' ')
		side = int(math.sqrt(len(data)))
		for i in range(side):
			for j in range(side):
				print('. ', end = '') if '-' in data[i*side+j] else print('Q ', end = '')
			print()
		print()

def main():
	with open(DATA_file, 'w') as csv_file:
		field_names = ['N-queens Problem', 'CPU Time', 'Satisfiability']
		csv_writer = csv.writer(csv_file)
		csv_writer.writerow(field_names)
	csv_file.close()
	for i in range(2, MAX_N+1):
		make_queen_sat(i)

main()