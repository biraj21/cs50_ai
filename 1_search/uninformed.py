import sys
import maze
import maze.frontiers as frontiers

if len(sys.argv) != 2:
    sys.exit("Usage: python unformed.py maze.txt")

m = maze.Maze(sys.argv[1], frontiers.StackFrontier)
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("Solution:")
m.print()
print("States explored: ", m.num_explored)
m.output_image("uninformed.png", show_explored=True)

if m.solution != None:
    print("Path: ", m.solution["actions"])
