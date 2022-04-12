import sys
import maze

if len(sys.argv) != 2:
    sys.exit("Usage: python bfs.py maze.txt")

m = maze.Maze(sys.argv[1], maze.QueueFrontier)
print("Maze:")
m.print()
print("Solving...\n")
m.solve()
print("Solution:")
m.print()
print("States explored:", m.num_explored)
print("Path:", m.solution["actions"])
m.output_image("images/bfs.png", show_explored=True)
