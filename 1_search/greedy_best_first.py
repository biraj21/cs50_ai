import sys
import maze
import maze.frontiers as frontiers

m = maze.Maze(sys.argv[1], frontiers.ManhattenFrontier)
print("Maze:")
m.print()
print("Solving...")
m.solve()
print("Solution:")
m.print()
print("States explored: ", m.num_explored)
m.output_image(f"{__file__}.png", show_explored=True)

if m.solution != None:
    print("Path: ", m.solution["actions"])
