# a1.py

from search import *
import random # for shuffle the tuple
import time # for record the time

# Question 1
def make_rand_8puzzle():
	init = list((0,1,2,3,4,5,6,7,8))
	solvable = False
	while not solvable:
		random.shuffle(init)
		new_puzzle = EightPuzzle(tuple(init))
		solvable = new_puzzle.check_solvability(new_puzzle.initial)
	return new_puzzle

def display(state):
	for x in range(0,9):
		if state[x] == 0:
			print("*", end = "  ")
		else:
			print(state[x], end = "  ")
		if x == 2 or x == 5 or x == 8:
			print("\n")

# Question 2
list_of_puzzle = []
for i in range(0,1):
	print("Puzzle", i+1, "\n")
	list_of_puzzle.append(make_rand_8puzzle())
	current_puzzle = list_of_puzzle[i]
	display(current_puzzle.initial)

	current_node = Node(current_puzzle.initial)
	current_state = current_puzzle.initial
	current_level = []

	start_time = time.time()
	astar_search(current_puzzle, current_puzzle.h)
	elapsed_time = time.time() - start_time()
	print('elapsed time (in seconds): {elapsed_time}')

