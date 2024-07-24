import student, time, argparse, json
from blockworld import BlockWorld

parser = argparse.ArgumentParser(description='Evaluate the algorithm on a given problem from problems/.')
parser.add_argument('n', type=int, help='number of blocks')
parser.add_argument('pid', type=int, help="problem id")
args = parser.parse_args()

def load_problem(n, pid):
	with open(f"problems/{n}/{pid}", "r") as f:
		problem = json.load(f)

	return problem

problem = load_problem(args.n, args.pid)

astar = student.AStar()
start = student.BlockWorldHeuristic(state=problem['start'])
goal = BlockWorld(state=problem['goal'])

t_start = time.time()
path = astar.search(start, goal)
t_end = time.time()

path_len = None if path is None else len(path)
expanded = BlockWorld.expanded
t_elapsed = t_end - t_start

print(f"{args.n}/{args.pid}: {start} -> {goal}")
print(f"Reference | path length: {problem['path_length']}, expanded: {problem['expanded_nodes']}, time: {problem['time']:.2f}s")
print(f"Yours     | path length: {path_len}, expanded: {expanded}, time: {t_elapsed:.2f}s")
