import math
from PIL import Image, ImageDraw


class Node:
    def __init__(self, state, parent, action, cost=0):
        self.state = state  # state of this node
        self.parent = parent  # reference to parent node
        self.action = action  # action taken to reach this state
        self.cost = cost  # cost incurred to reach this state


class StackFrontier:
    """
        For Depth-First Search algorithm.
    """

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def is_empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):
    """
        For Breadth-First Search algorithm. Always finds the shortest path.
    """

    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


def manhattan_distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


class ManhattanFrontier(StackFrontier):
    """
        For Greedy Best-First Search algorithm.
    """

    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            # remove the node that is estimated to be the closest to the goal
            min = math.inf
            for node in self.frontier:
                if node.state == self.goal:
                    self.frontier.remove(node)
                    return node
                else:
                    dist = manhattan_distance(
                        node.state[0], node.state[1], self.goal[0], self.goal[1]
                    )
                    if dist < min:
                        min = dist
                        min_node = node

            self.frontier.remove(min_node)
            return min_node


class ManhattanCostFrontier(StackFrontier):
    """
        For A* Search algorithm.
    """

    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            # remove the node that is estimated to be the closest to the goal
            min = math.inf
            for node in self.frontier:
                if node.state == self.goal:
                    self.frontier.remove(node)
                    return node
                else:
                    dist = node.cost + manhattan_distance(
                        node.state[0], node.state[1], self.goal[0], self.goal[1]
                    )
                    if dist < min:
                        min = dist
                        min_node = node

            self.frontier.remove(min_node)
            return min_node


class Maze:
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    def __init__(self, filename, frontier):
        with open(filename) as file:
            contents = file.read()

        # validation of starting and goal positions
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one starting point")
        elif contents.count("B") != 1:
            raise Exception("maze muse have exactly one goal")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        self.frontier = frontier
        self.solution = None

        self.walls = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                try:
                    if contents[y][x] == "A":
                        self.start = (x, y)
                        row.append(False)
                    elif contents[y][x] == "B":
                        self.goal = (x, y)
                        row.append(False)
                    elif contents[y][x] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)

            self.walls.append(row)

    def print(self):
        for y, row in enumerate(self.walls):
            for x, is_wall in enumerate(row):
                if is_wall:
                    print("█", end="")
                elif (x, y) == self.start:
                    print("A", end="")
                elif (x, y) == self.goal:
                    print("B", end="")
                elif self.solution != None and (x, y) in self.solution["path"]:
                    print("+", end="")
                else:
                    print(" ", end="")

            print()

        print()

    def routes(self, state):
        x, y = state
        coords = [
            (Maze.UP, (x, y - 1)),
            (Maze.DOWN, (x, y + 1)),
            (Maze.LEFT, (x - 1, y)),
            (Maze.RIGHT, (x + 1, y)),
        ]

        actions = []
        for action, (x, y) in coords:
            if 0 <= x < self.width and 0 <= y < self.height and not self.walls[y][x]:
                actions.append((action, (x, y)))

        return actions

    def solve(self):
        # number of states explored
        self.num_explored = 0

        # initial state
        start = Node(state=self.start, parent=None, action=None)
        frontier = self.frontier()
        frontier.goal = self.goal
        frontier.add(start)

        # states that have been explored
        self.explored = set()

        while True:
            # if frontier is empty, no solution
            if frontier.is_empty():
                print("no solution")
                return

            # choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            if node.state == self.goal:
                actions = []
                path = []

                while node.parent != None:
                    actions.append(node.action)
                    path.append(node.state)
                    node = node.parent

                actions.reverse()
                path.reverse()
                self.solution = {"actions": actions, "path": path}
                return

            # mark this node's state as explored
            self.explored.add(node.state)

            # add next routes to the frontier
            for action, state in self.routes(node.state):
                if state not in self.explored and not frontier.contains_state(state):
                    new_node = Node(state=state, parent=node,
                                    action=action, cost=node.cost + 1)
                    frontier.add(new_node)

    def output_image(self, filename, show_solution=True, show_explored=False):
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution["path"] if self.solution != None else None

        for y, row in enumerate(self.walls):
            for x, is_wall in enumerate(row):
                # for walls
                if is_wall:
                    fill = (40, 40, 40)
                # for starting position
                elif (x, y) == self.start:
                    fill = (255, 0, 0)
                # for goal position
                elif (x, y) == self.goal:
                    fill = (0, 171, 28)
                # for solution path
                elif show_solution and solution != None and (x, y) in solution:
                    fill = (220, 235, 113)
                # for explored nodes
                elif show_explored and solution != None and (x, y) in self.explored:
                    fill = (212, 97, 85)
                else:  # for empty cells
                    fill = (237, 240, 252)

                # Draw cell
                draw.rectangle(
                    ([(x * cell_size + cell_border, y * cell_size + cell_border),
                      ((x + 1) * cell_size - cell_border, (y + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)
