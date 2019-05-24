# a1.py

from search import *
import random # for shuffle the tuple
import time # for record the time
import math # for floor function

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
def h_manhattan(node):
	sum = 0
	goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
	for i in range(1, 9):
		distance = abs(node.state.index(i) - goal.index(i))
		sum += distance%3 + math.floor(distance/3)
	return sum

# this function originally exists in search.py under EightPuzzle class
def h_misplaced(node):
	goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    return sum(s != g for (s, g) in zip(node.state, goal))

def max_of_manhattan_misplaced(node):
	value_manhattan = h_manhattan(node)
	value_misplaced = h_misplaced(node)
	return value_manhattan if value_manhattan > value_misplaced else value_misplaced

list_of_puzzle = []
for i in range(0,1):
	print("Puzzle", i+1, "\n")
	list_of_puzzle.append(make_rand_8puzzle())
	current_puzzle = list_of_puzzle[i]
	display(current_puzzle.initial)

	start_time = time.time()
	print(astar_search(current_puzzle, current_puzzle.h))
	elapsed_time = time.time() - start_time()
	print(f'elapsed time (in seconds): {elapsed_time}')

	start_time = time.time()
	print(astar_search(current_puzzle, h_manhattan))
	elapsed_time = time.time() - start_time
	print(f'elapsed time (in seconds): {elapsed_time}')

	start_time = time.time()
	print(astar_search(current_puzzle, max_of_manhattan_misplaced))
	elapsed_time = time.time() - start_time
	print(f'elapsed time (in seconds): {elapsed_time}')



