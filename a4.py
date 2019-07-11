''' 
Cmpt 310 assignment 4 question 1 
Created by Liam Ling
Date: Sun July 8 2019
References: https://int8.io/monte-carlo-tree-search-beginners-guide/
		   https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/
'''

from random import randrange
import numpy # for construct game board and state
import sys
import re # for checking move input pattern
import time # for sleep function

class tic_tac_toe_game:
	"""docstring for game_state"""
	player_0 = 1 # as AI
	player_1 = -1 # as Human
	draw = 0
	def __init__(self, state, size = None, player = None):
		if type(player) != int:
			raise TypeError('player must be represented in int')
		if len(state.shape) != 2:
			raise ValueError('board must be in 2-dimension')
		if state.shape[0] != state.shape[1]:
			raise ValueError('board must has the same size row and column')
		self.__size = size
		self.__state = state
		self.__current_player = player

	@property
	def state(self):
		return self.__state

	@state.setter
	def state(self, value):
		self.__state = value

	@property
	def size(self):
		if self.__size != self.state.shape[0]:
			raise ValueError('state has diffierent value with size')
		return self.__size

	@size.setter
	def size(self, value):
		self.__size = value
	
	@property
	def current_player(self):
		return self.__current_player

	@current_player.setter
	def current_player(self, value):
		if self.__current_player == value:
			raise ValueError('unable to set the same player to current_player')
		self.__current_player = value

	@property
	def row_sum(self):
		return numpy.sum(self.state, axis = 1)
	
	@property
	def column_sum(self):
		return numpy.sum(self.state, axis = 0)

	@property
	def diagnal_sum(self):
		return [self.state.trace(), self.state[::-1].trace()]

	@property
	def result(self):
		if (self.size in self.row_sum) or (self.size in self.column_sum) or (self.size in self.diagnal_sum):
			return self.player_1 # player_1 wins
		elif (-self.size in self.row_sum ) or (-self.size in self.column_sum) or (-self.size in self.diagnal_sum):
			return self.player_0 # player_0 wins
		elif numpy.all(self.state != 0):
			return self.draw # draw

	@property
	def next_player(self):
		if self.current_player == self.player_0:
			return self.player_1
		elif self.current_player == self.player_1:
			return self.player_0

	def print_game_state(self):
		row_index = 0
		print('\n')
		for row in self.state:
			print('\t'+str(row_index) + '   ', end = '')
			for col in row:
				if col == 0:
					print('-   ', end = '')
				elif col == self.player_0:
					print('x   ', end = '')
				elif col == self.player_1:
					print('o   ', end = '')
			row_index += 1
			print('\n')
			if row_index == self.size:
				print('\t    ', end = '')
				for col_index in range(row_index):
					print(str(col_index) + '   ', end = '')
				print('\n')
		
	def game_over(self):
		return self.result != None
	
	def possible_moves(self):
		empty_slots = numpy.where(self.state == 0)
		return [[index[0], index[1]]for index in zip(empty_slots[0], empty_slots[1])]

	def legal_move(self, move):
		if move[0] > self.size and move[0] < 0 or move[1] > self.size and move[1] < 0:
			return False
		if self.state.take(move[0], 0).take(move[1], 0) != 0:
			return False
		return True

	def move(self, move):
		if not self.legal_move(move):
			raise ValueError(str(move) + ' is not legal')
		new_state = numpy.copy(self.state)
		new_state[move[0], move[1]] = self.next_player
		return tic_tac_toe_game(new_state, new_state.shape[0], self.next_player)

class monte_carlo_tree_node:
	"""docstring for node"""
	def __init__(self, state: tic_tac_toe_game, parent = None, move = None):
		self.__state = state
		self.__move = move
		self.__parent = parent
		self.__children = []
		self.__number_wins = 0
		self.__number_visits = 0;
		self.__unexplored_children = state.possible_moves()

	@property
	def state(self):
		return self.__state

	@state.setter
	def state(self, value):
		self.__state = value

	@property
	def move(self):
		return self.__move

	@move.setter
	def move(self, value):
		self.__move = value

	@property
	def parent(self):
		return self.__parent

	@parent.setter
	def parent(self, value):
		self.__parent = value

	@property
	def children(self):
		return self.__children

	@children.setter
	def children(self, value):
		self.__children = value

	@property
	def number_wins(self):
		return self.__number_wins

	@number_wins.setter
	def number_wins(self, value):
		self.__number_wins = value

	@property
	def number_visits(self):
		return self.__number_visits

	@number_visits.setter
	def number_visits(self, value):
		self.__number_visits = value

	@property
	def unexplored_children(self):
		return self.__unexplored_children

	@unexplored_children.setter
	def unexplored_children(self, value):
		if type(value) != list:
			raise TypeError('unexplored_children must be a list of nodes')
		self.__unexplored_children = value
	
	def fully_expanded(self):
		return self.__unexplored_children == []

	def children_exist(self):
		return self.children != []

	def terminal_node(self):
		return self.state.game_over()

	def expansion_policy(self, possible_moves):
		return randrange(len(possible_moves))

	def rollout_policy(self, possible_moves):
		return randrange(len(possible_moves))

	def select(self, c_parm = 1.): # Upper Confidence Bound applied to trees
		UCT = lambda x: x.number_wins / x.number_visits + c_parm * numpy.sqrt(2.0 * numpy.log(self.number_visits) / x.number_visits)
		return sorted(self.children, key = UCT)[-1]

	def expand(self):
		next_move = self.unexplored_children.pop(self.expansion_policy(self.unexplored_children))
		next_state = self.state.move(next_move)
		child = monte_carlo_tree_node(next_state, parent = self, move = next_move)
		self.children.append(child)
		return child

	def rollout(self):
		current_state = self.state
		while not current_state.game_over():
			possible_moves = current_state.possible_moves()
			move = possible_moves[self.rollout_policy(possible_moves)]
			current_state = current_state.move(move)
			#current_state.print_game_state()
		return current_state.result

	def update(self, game_result):
		self.number_visits += 1
		if game_result == 1:
			self.number_wins += 1

class monte_carlo_tree_search:
	"""docstring for monte_carlo_tree_search"""
	def __init__(self, tree_node: monte_carlo_tree_node):
		self.__root = tree_node

	@property
	def root(self):
		return self.__root

	@root.setter
	def root(self, value):
		self.__root = value

	def win_rate(self):
		win_rate_lambda = lambda x: x.number_wins / x.number_visits
		win_rate_sorted = list(zip(sorted(self.root.children, key = win_rate_lambda)[::-1], sorted(list(map(win_rate_lambda, self.root.children)))[::-1]))

		print('Win rate statistic from AI:')
		for item in win_rate_sorted:
			print('Move: ', item[0].move, '  Win rate: ', item[1]*100, '%')
		return win_rate_sorted

	def simulation_policy(self, possible_moves):
		return randrange(len(possible_moves))

	def simulating(self, simulation_times):
		while simulation_times > 0:
			current_node = self.root
			# selection phase
			while current_node.fully_expanded() and current_node.children_exist():
				current_node = current_node.select()
			# expansion phase
			if not current_node.fully_expanded() and not current_node.terminal_node():
				current_node = current_node.expand()
				if current_node == None:
					raise TypeError('current_node is not fully expanded')
			# rollout phase
			result = current_node.rollout()
			# propagation phase
			while current_node != None:
				current_node.update(result)
				current_node = current_node.parent

			simulation_times -= 1
		children_dict = self.win_rate()
		return children_dict[0][0], children_dict[0][0].move # return child node and best move

def get_keyboard_input(input_type, board:tic_tac_toe_game = None):
	while True:
		if input_type is 'size':
			try:
				keyboard_input = int(input('Please enter the size of the board: '))
				if keyboard_input < 1 or keyboard_input > 10:
					raise ValueError
				return keyboard_input
			except KeyboardInterrupt:
				print('\n')
				sys.exit(0)
			except ValueError:
				print('Size must be an positive integer which smaller or equal to 10')
		elif input_type is 'move':
			try:
				keyboard_input = input('Please enter your move (using "," to seperate the x and y coordinate): ')
				pattern = re.compile('^[0-9]+,[0-9]')
				if not pattern.match(keyboard_input):
					raise ValueError
				else:
					coordinate = [int(keyboard_input.split(',')[0]), int(keyboard_input.split(',')[1])]
				if not board.legal_move(coordinate):
					print(keyboard_input, end=': ')
					raise ValueError
				return coordinate
			except KeyboardInterrupt:
				print('\n')
				sys.exit(0)
			except ValueError:
				print('Invalid move, please try again.')

def play_a_new_game():
	print('---------- Tic Tac Toe ----------\nPress Ctrl+C to exit the program\nTo initialize game board, ', end = '')
	simulation_times = 1000
	players = {'AI':1, 'Human':-1}
	fisrt_player = 'Human'
	while True:
		board_size = get_keyboard_input('size')
		simulation_times = board_size * board_size * 1000
		game_board = tic_tac_toe_game(numpy.zeros((board_size, board_size)), board_size, players.get(fisrt_player))
		root_node = monte_carlo_tree_node(game_board)
		game_core = monte_carlo_tree_search(root_node)
		game_board.print_game_state()

		print(fisrt_player + ' play first =>')
		while True:
			root_node = monte_carlo_tree_node(game_board)
			game_core = monte_carlo_tree_search(root_node)
			if game_board.current_player == players.get('AI'):
				print('AI\' turn ...')
				root_node, move = game_core.simulating(simulation_times)
				print('AI choose move: ', move)
			else:
				move = get_keyboard_input('move', game_board)
			game_board = game_board.move(move)
			game_board.print_game_state()
			if game_board.game_over():
				if game_board.result == 1:
					print('AI won')
				elif game_board.result == -1:
					print('Human won')
				else:
					print('draw')
				if fisrt_player == 'AI':
					fisrt_player = 'Human'
				else:
					fisrt_player = 'AI'
				break

if __name__ == '__main__':
	play_a_new_game()
	
