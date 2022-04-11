import sys
import maze

if len(sys.argv) != 2:
    sys.exit("Usage: python a_star.py maze.txt")

m = maze.Maze(sys.argv[1], maze.ManhattanCostFrontier)
print("Maze:")
m.print()
print("Solving...\n")
m.solve()
print("Solution:")
m.print()
print("States explored: ", m.num_explored)
m.output_image("images/a_star.png", show_explored=True)

if m.solution != None:
    print("Path: ", m.solution["actions"])
