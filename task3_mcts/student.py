import random, time
import numpy as np

import ox

class MCTSBot:
	visited = {}
	chosen = {}
	q_dict = {}
	c = 2

	def __init__(self, play_as: int, time_limit: float):
		self.play_as = play_as
		self.time_limit = time_limit * 0.9

	# we look at each child, if all of them have visited = 0, we send this node to expand, otherwise, we calc the best child using UCB1 and switch to it
	def select(self, board):
		leaf_node = False

		while not board.is_terminal():
			next_states = []
			for action in board.available_actions:
				board_next = board.clone()
				board_next.apply_action(action)

				if board_next in self.visited.keys():
					leaf_node = False
					
				a_from_s_chosen = self.chosen.get((board, action), 0)
				
				if a_from_s_chosen == 0:
					UCB = np.inf
				else:
					q_sa = self.q_dict.get((board, action), 0)
					s_visited = np.log(self.visited.get(board, 0))
					UCB = q_sa + 2 * self.c * np.sqrt((2 * s_visited) / a_from_s_chosen)

				next_states.append((board_next, action, UCB))

			if board.is_terminal() or leaf_node:
				break
			else:
				board_next = max(next_states, key=lambda x: x[2])[0]
				board = board_next

		return board

	# if chosen(board, action) = 0, we simulate from here, else we create random child and simulate from there
	def expand(self, board):
		if not board.is_terminal() or self.visited.get(board, 0) != 0:
			actions = list(board.available_actions)
			action = random.choice(actions)
			new_board = board.clone()
			new_board.apply_action(action)
			board = new_board
		
		return board

	def simulate(self, board):
		visited_boards = []
		while not board.is_terminal():
			actions = list(board.available_actions)
			action = random.choice(actions)
			visited_boards.append((board, action))
			board.apply_action(action)

		visited_boards.append((board, -1))
		return visited_boards

	def backpropagate(self, visited_boards):
		reward = visited_boards[-1][0].get_rewards()[self.play_as]
		count = 0

		for state, action in visited_boards[:-1]:
			if state in self.visited.keys():
				self.visited[state] += 1
			else:
				self.visited[state] = 1

			if (state, action) in self.chosen.keys():
				self.chosen[(state, action)] += 1
			else:
				self.chosen[(state, action)] = 1

			self.q_dict[(state, action)] = (self.q_dict.get((state, action), 0) + reward) / self.chosen[(state, action)] * ((-1 * count))
			count = count + 1



	def play_action(self, board):
		# TODO: implement MCTS bot

		start_time = time.time()
		while (time.time() - start_time) < self.time_limit:
			child = self.select(board)
			exp_child = self.expand(child)
			simulation = self.simulate(exp_child)
			self.backpropagate(simulation)

		q_values_for_this_state = []
		for action in board.available_actions:
			q_value = self.q_dict.get((board, action), 0)
			q_values_for_this_state.append((action, q_value))
		
		a = max(q_values_for_this_state, key=lambda x: x[1])[0]
		return a

if __name__ == '__main__':
	board = ox.Board(8)  # 8x8
	bots = [MCTSBot(0, 1.0), MCTSBot(1, 1.0)]

	# try your bot against itself
	while not board.is_terminal():
		current_player = board.current_player()
		current_player_mark = ox.MARKS_AS_CHAR[ ox.PLAYER_TO_MARK[current_player] ]

		current_bot = bots[current_player]
		a = current_bot.play_action(board)
		board.apply_action(a)

	print(f"{current_player_mark}: {a} -> \n{board}\n")

