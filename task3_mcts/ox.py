import numpy as np, itertools, copy

MARKS_AS_CHAR = {0: '.', 1: 'x', 2: 'o'}
PLAYER_TO_MARK = [1, 2]
MARK_TO_PLAYER = [None, 0, 1]

class Board():
	def __init__(self, size=10, row_to_win=5):
		self.size = size
		self.row_to_win = row_to_win
		self.board = np.zeros((size, size), dtype=np.byte)
		self.player = 0
		self.available_actions = set(range(size ** 2))
		self.history = []
		self.winner = None

		self.set_x = set()
		self.set_o = set()

	def apply_action(self, action):
		i = action // self.size
		j = action % self.size

		assert self.board[i,j] == 0
		assert not self.is_terminal()

		self.available_actions.remove(action)
		self.history.append(action)

		if self.player == 0:
			self.set_x.add(action)
		else:
			self.set_o.add(action)

		self.board[i,j] = PLAYER_TO_MARK[self.player]
		self.player = 1 if self.player == 0 else 0

		self.winner = self._check_winner((i,j))

		# invalidate the cache
		if hasattr(self, '_hash'):
			del self._hash

	def is_terminal(self):
		return (self.winner is not None) or (len(self.available_actions) == 0)

	def current_player(self):
		return self.player

	def get_rewards(self):
		if self.winner is None:
			return [0, 0]

		if self.winner == 0:
			return [1, -1]

		if self.winner == 1:
			return [-1, 1]

		print(self.winner)
		raise RuntimeError()

	def get_actions(self):
		return self.available_actions

	def clone(self):
		return copy.deepcopy(self)

	def _check_winner(self, last_action):
		i, j = last_action
		slices = [self.board[i, :], self.board[:, j], self.board.diagonal(j-i), self.board[:, ::-1].diagonal(self.size-1-j-i)]
		
		for slice in slices:
			for mark, group in itertools.groupby(slice):
				if mark == 0:	# free spot
					continue

				if len(list(group)) == self.row_to_win:
					return MARK_TO_PLAYER[mark]

		return None

	def _val(self):
		return (frozenset(self.set_x), frozenset(self.set_o))

	def __hash__(self):
		if hasattr(self, '_hash'):
			return self._hash

		hsh = hash(self._val())
		self._hash = hsh

		return hsh

	def __eq__(self, other):
		return (self._val()) == (other._val())

	def __repr__(self):
		rows = ["".join(MARKS_AS_CHAR[self.board[i, j]] for j in range(self.size)) for i in range(self.size)]
		return "\n".join(rows)
