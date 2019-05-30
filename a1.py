# a1.py

from search import *
import random # for shuffle the tuple
import time # for record the time
import math # for floor function
from itertools import permutations # for generate possbile permutations for Q3

# Question 1
def make_rand_8puzzle():
	init = list((0, 1, 2, 3, 4, 5, 6, 7, 8))
	solvable = False
	while not solvable:
		random.shuffle(init)
		new_puzzle = EightPuzzle(tuple(init))
		solvable = new_puzzle.check_solvability(new_puzzle.initial)
	return new_puzzle

def display(state):
	for x in range(0, 9):
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

def test_mispalced(puzzle, h):
	start_time = time.time()
	print(astar_search(puzzle, h))
	elapsed_time = time.time() - start_time
	return elapsed_time

def test_manhattan(puzzle, h):
	start_time = time.time()
	print(astar_search(puzzle, h))
	elapsed_time = time.time() - start_time
	return elapsed_time

def test_max_of_manhattan_misplaced(puzzle, h):
	start_time = time.time()
	print(astar_search(puzzle, h))
	elapsed_time = time.time() - start_time
	return elapsed_time

list_of_puzzle = []
f = open("Q2.txt", "w")
for i in range(0,15):
	st = "\nPuzzle"+str(i+1)+"\n"
	print(st)
	f.write(st)

	list_of_puzzle.append(make_rand_8puzzle())
	current_puzzle = list_of_puzzle[i]
	display(current_puzzle.initial)

	elapsed_time = test_mispalced(current_puzzle, current_puzzle.h)
	st = f'\nelapsed time (in seconds): {elapsed_time}'
	print(st)
	f.write(st)

	elapsed_time = test_manhattan(current_puzzle, h_manhattan)
	st = f'\nelapsed time (in seconds): {elapsed_time}'
	print(st)
	f.write(st)

	elapsed_time = test_max_of_manhattan_misplaced(current_puzzle, max_of_manhattan_misplaced)
	st = f'\nelapsed time (in seconds): {elapsed_time}'
	print(st)
	f.write(st)
f.close()

# Question 3
class YPuzzle(Problem):
	def __init__(self, initial, goal=(1, -1, 2, 3, 4, 5, 6, 7, 8, -1, 0, -1)):
		self.goal = goal
		Problem.__init__(self, initial, goal)

	def find_blank_square(self, state):
		return state.index(0)

	# cannot go to index 1, 9, 11
	# on index 0, 2, it can only go down
	# on index 4 can not go up
	# on index 6, 7 can not go down
	# on index 10 can only go up
	def actions(self, state):
		index_blank_square = self.find_blank_square(state)

		if index_blank_square == 0 or index_blank_square == 2:
			possible_actions = ['DOWN']
		elif index_blank_square == 10:
			possible_actions = ['UP']
		else:
			possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']

			if index_blank_square % 3 == 0:
				possible_actions.remove('LEFT')
			if index_blank_square < 3 or index_blank_square == 4:
				possible_actions.remove('UP')
			if index_blank_square % 3 == 2:
				possible_actions.remove('RIGHT')
			if index_blank_square == 6 or index_blank_square == 8:
				possible_actions.remove('DOWN')

		return possible_actions

	def result(self, state, action):
		blank = self.find_blank_square(state)
		new_state = list(state)

		delta = {'UP':-3, 'DOWN':3, 'LEFT':-1, 'RIGHT':1}
		neighbor = blank + delta[action]
		new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

		return tuple(new_state)

	def goal_test(self, state):
		return state == self.goal

	def check_inversion(self, state, goal):
		inversion = 0
		for i in range(3,9):
			for j in range(i+1, 9):
				if (state[i] > state[j]) and state[i] != 0 and state[j]!= 0:
					inversion += 1
		return inversion % 2 == 0

	def check_solvability(self, state):
		if state.index(1) == 0 and state.index(0) == 2 and state.index(7) == 10 and state.index(2) == 5:
			return self.check_inversion(state, self.goal)
		elif state.index(2) == 2 and state.index(0) == 0 and state.index(7) == 10 and state.index(1) == 3:
			return self.check_inversion(state, self.goal)
		if state.index(1) == 0 and state.index(2) == 2:
			if state.index(0) == 10:
				for i in range(3, 9):
					if state.index(i) != i:
						return False
				return True
			elif state.index(7) == 10:
				return self.check_inversion(state, self.goal)
			else:
				return False
		return False

def display_ypuzzle(state):
	for x in range(0, 12):
		if state[x] == 0:
			print("*", end = "  ")
		elif state[x] == -1:
			print("█", end = "  ")
		else:
			print(state[x], end = "  ")
		if x == 2 or x == 5 or x == 8 or x == 11:
			print("\n")

def make_rand_ypuzzle():
	solvable = False
	per = []
	s = 0
	for i in permutations((0, 1, 2, 3, 4, 5, 6, 7, 8)):
		i = list(i)
		i.insert(1, -1)
		i = list(i)
		i.insert(9, -1)
		i = list(i)
		i.insert(11 ,-1)

		temp_puzzle = YPuzzle(tuple(i))
		if temp_puzzle.check_solvability(temp_puzzle.initial):
			per.append(temp_puzzle)
	random.shuffle(per)

	# while not solvable:
	# 	version = random.randint(1,4)
	# 	if version == 1:
	# 		init = list((3, 4, 5, 6, 8))
	# 		random.shuffle(init)
	# 		init.insert(0, 1)
	# 		init.insert(1, -1)
	# 		init.insert(2, 0)
	# 		init.insert(5, 2)
	# 	elif version == 2:
	# 		init = list((3, 4, 5, 6, 8))
	# 		random.shuffle(init)
	# 		init.insert(0, 0)
	# 		init.insert(1, -1)
	# 		init.insert(2, 2)
	# 		init.insert(3, 1)
	# 	else:
	# 		init = list((0, 3, 4, 5, 6, 8))
	# 		random.shuffle(init)
	# 		init.insert(0, 1)
	# 		init.insert(1, -1)
	# 		init.insert(2, 2)
	# 	init.insert(9, -1)
	# 	init.insert(10, 7)
	# 	init.insert(11 ,-1)
	# 	new_puzzle = YPuzzle(tuple(init))
	# 	display_ypuzzle(init)
	# 	print("---------")
	# 	solvable = new_puzzle.check_solvability(new_puzzle.initial)
	return per[random.randint(0, len(per))]

def h_manhattan_ypuzzle(node):
	sum = 0
	goal = (1, -1, 2, 3, 4, 5, 6, 7, 8, -1, 0, -1)
	for i in range(1, 9):
		if goal.index(i) != node.state.index(i):
			if goal.index(i) <= 2:
				level_g = 1
			elif goal.index(i) >= 3 and goal.index(i) <= 5:
				level_g = 2
			elif goal.index(i) >= 6 and goal.index(i) <= 8:
				level_g = 3
			else:
				level_g = 4

			if node.state.index(i) <= 2:
				level_n = 1
			elif node.state.index(i) >= 3 and node.state.index(i) <= 5:
				level_n = 2
			elif node.state.index(i) >= 6 and node.state.index(i) <= 8:
				level_n = 3
			else:
				level_n = 4

			if level_n == level_g and (i == 1 or i == 2):
				moves = 4
			elif level_n == level_g and i > 2:
				moves = abs(goal.index(i) - node.state.index(i))
			elif level_n != level_g and (i == 1 or i == 2):
				moves = abs(goal.index(i) - (level_g-level_n)*3 - node.state.index(i))
			elif level_n != level_g and i > 2:
				moves = abs(abs(node.state.index(i) - goal.index(i)) - abs(level_g-level_n)*3 )

			distance = abs(level_g - level_n) + moves
			sum += distance % 3 + math.floor(distance / 3)
	return sum

# this function originally exists in search.py under EightPuzzle class
def h_misplaced_ypuzzle(node):
	goal = (1, -1, 2, 3, 4, 5, 6, 7, 8, -1, 0, -1)
	return sum(s != g for (s, g) in zip(node.state, goal))

def max_of_manhattan_misplaced_ypuzzle(node):
	value_manhattan = h_manhattan_ypuzzle(node)
	value_misplaced = h_misplaced_ypuzzle(node)
	return value_manhattan if value_manhattan > value_misplaced else value_misplaced

def test_mispalced_ypuzzle(puzzle, h):
	start_time = time.time()
	print(astar_search(puzzle, h))
	elapsed_time = time.time() - start_time
	return elapsed_time

def test_manhattan_ypuzzle(puzzle, h):
	start_time = time.time()
	print(astar_search(puzzle, h))
	elapsed_time = time.time() - start_time
	return elapsed_time

def test_max_of_manhattan_misplaced_ypuzzle(puzzle, h):
	start_time = time.time()
	print(astar_search(puzzle, h))
	elapsed_time = time.time() - start_time
	return elapsed_time

list_of_puzzle = []
f = open("Q3.txt", "w")
for i in range(0,15):
	st = "Puzzle"+str(i+1)+"\n"
	print(st)
	f.write(st)

	list_of_puzzle.append(make_rand_ypuzzle())
	current_puzzle = list_of_puzzle[i]
	display_ypuzzle(current_puzzle.initial)

	elapsed_time = test_mispalced_ypuzzle(current_puzzle, h_misplaced_ypuzzle)
	st = f'\nelapsed time (in seconds): {elapsed_time}'
	print(st)
	f.write(st)

	elapsed_time = test_manhattan_ypuzzle(current_puzzle, h_manhattan_ypuzzle)
	st = f'\nelapsed time (in seconds): {elapsed_time}'
	print(st)
	f.write(st)

	elapsed_time = test_max_of_manhattan_misplaced_ypuzzle(current_puzzle, max_of_manhattan_misplaced_ypuzzle)
	st = f'\nelapsed time (in seconds): {elapsed_time}'
	print(st)
	f.write(st)
f.close()



