import sys
import maze

if len(sys.argv) != 2:
    sys.exit("Usage: python gbf.py maze.txt")

m = maze.Maze(sys.argv[1], maze.ManhattanFrontier)
print("Maze:")
m.print()
print("Solving...\n")
m.solve()
print("Solution:")
m.print()
print("States explored: ", m.num_explored)
m.output_image("images/gbf.png", show_explored=True)

if m.solution != None:
    print("Path: ", m.solution["actions"])
