''' 
Cmpt 310 assignment 3 question 1 
Created by Liam Ling
Date: Mon June 24 2019
'''

import subprocess # for exexcuting commands in terminal
from itertools import combinations # for generating combinations of a subset of clause candidates

def generate_clauses_set(num_of_queen):
	board_side = num_of_queen
	board_size = board_side**2
	candidates = [i] for i in range(1, board_size+1)
	clauses_set = []
	# horizontal
	for candidate in candidates[:board_side]:
		clauses_set.append(join' '.join(map(str, candidate) + " 0")
		clauses_set.append(' '.joing(i) for i in combinations(candidate, 2)))

def make_queen_sat(N):
	with open("sat-test.txt", "w") as sat_file:
		for 
			sat_file.write()
	sat_process = subprocess.Popen(["minisat",""], stdout=subprocess.PIPE)
	output = sat_process.communicate()[0]
	sat_file.close()

def draw_queen_sat_sol(sol):
