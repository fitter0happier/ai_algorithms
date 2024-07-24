###
# This file is not part of the submission. Do not change it!
# You can play with the environment by directly running `python blockworld.py`.
##

import random, copy, numpy as np, ast

def _get_random_state(num_obj):
	stacks = []
	obj = np.arange(1, num_obj + 1)

	while len(obj) > 0:
		stack_len = np.random.randint(1, len(obj)+1)
		stack = np.random.choice(obj, stack_len, replace=False)

		stacks.append(stack)
		obj = np.setdiff1d(obj, stack)

	return stacks

def _find_stack(stacks, item):
	for stack_id, stack in enumerate(stacks):
		if stack[0] == item:
			return stack, stack_id

	return None, None

class BlockWorld():
	expanded = 0

	def __init__(self, num_blocks=5, state=None):
		if state is None:	# create a random state
			self.state = _get_random_state(num_blocks)
			self.conf = frozenset(tuple(o) for o in self.state)
			
		else:	# load the given state
			stacks = []
			for s in ast.literal_eval(state):
				stacks.append(np.array(s))

			self.state = stacks
			self.conf = frozenset(tuple(o) for o in self.state)

	def apply(self, action):
		what, where = action

		# print(f"{what}->{where}")
		if what == where:
			print("!invalid action what==where")
			return

		stack_from, stack_from_id = _find_stack(self.state, what)
		if stack_from is None:	 # invalid action
			print("!invalid action cannot move what")
			return

		if where == 0: 			 # to the ground, create a new stack
			stack_to = np.empty(0, dtype=int)
			self.state.append(stack_to)
			stack_to_id = len(self.state) - 1
		else: 					 
			stack_to, stack_to_id = _find_stack(self.state, where)

		if stack_to is None:	 # invalid action
			print("!invalid action cannot move to where")
			return

		# move the item
		self.state[stack_from_id] = np.delete(stack_from, 0)
		self.state[stack_to_id]   = np.insert(stack_to, 0, what)

		# delete a potentially empty stack
		if len(self.state[stack_from_id]) == 0:
			del self.state[stack_from_id]

		self.conf = frozenset(tuple(o) for o in self.state)

	def get_actions(self):
		BlockWorld.expanded += 1

		actions = []
		for s_from in self.state:
			a = s_from[0]

			if len(s_from) > 1:
				actions.append((a, 0)) # to ground

			for s_to in self.state:
				b = s_to[0]

				if a != b:
					actions.append((a, b))

		return actions

	def get_neighbors(self):
		neighbors = []

		for a in self.get_actions():
			n = self.clone()
			n.apply(a)

			neighbors.append( (a, n) )

		return neighbors

	def get_state(self):
		return self.conf

	def __str__(self):
		return str([list(o) for o in self.state])

	def __repr__(self):
		return str(self)

	def __eq__(self, other):
		return self.conf == other.conf

	def __hash__(self):
		return hash(self.conf)

	def __lt__(self, other):
		return 0

	def clone(self):
		blocks_ = type(self)(0)
		blocks_.state = copy.deepcopy(self.state)

		return blocks_

if __name__ == '__main__':
	blocks = BlockWorld(4)

	while True:
		print(f"state = {blocks}")
		print(f"actions = {blocks.get_actions()}")
		print("<from> <to>: ", end="")

		n_from, n_to = [int(x) for x in input().split()]
		blocks.apply((n_from, n_to))


