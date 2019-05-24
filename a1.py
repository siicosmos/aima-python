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
for i in range(0,20):
	print("Puzzle", i+1, "\n")
	list_of_puzzle.append(make_rand_8puzzle())
	current_puzzle = list_of_puzzle[i]
	display(current_puzzle.initial)

	start_time = time.time()
	print(astar_search(current_puzzle, current_puzzle.h))
	elapsed_time = time.time() - start_time
	print(f'elapsed time (in seconds): {elapsed_time}')

	start_time = time.time()
	print(astar_search(current_puzzle, h_manhattan))
	elapsed_time = time.time() - start_time
	print(f'elapsed time (in seconds): {elapsed_time}')

	start_time = time.time()
	print(astar_search(current_puzzle, max_of_manhattan_misplaced))
	elapsed_time = time.time() - start_time
	print(f'elapsed time (in seconds): {elapsed_time}')

# Question 3
class YPuzzle(Problem):
	def __init__(self, initial, goal=(1,2,3,4,5,6,7,8,0)):
		self.goal = goal
		Problem.__init__(self, initial, goal)

	def find_blank_square(self, state):
		return state.index(0)

	# index 0 and index 1 can only go up
	# index 3 can not go down
	# index 8 can only go down
	def actions(self, state):
		index_blank_square = self.find_blank_square(state)
		if index_blank_square == 0 or index_blank_square == 1:
			possible_actions = ['UP']
		elif index_blank_square == 8:
			possible_actions = ['DOWN']
		else:
			possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

			if index_blank_square == 3:
				possible_actions.remove('DOWN')
			if index_blank_square % 3 == 0:
				possible_actions.remove('LEFT')
			if index_blank_square < 3:
				possible_actions.remove('UP')
			if index_blank_square % 3 == 2:
				possible_actions.remove('RIGHT')
			if index_blank_square > 5:
				possible_actions.remove('DOWN')
		return possible_actions


