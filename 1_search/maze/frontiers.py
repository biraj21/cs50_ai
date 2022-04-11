import math


class StackFrontier:
    """
        For Depth-First Search
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
        For Breadth-First Search. Always finds the shortest path.
    """

    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node


class ManhattenFrontier(StackFrontier):
    """
        For Greedy Best-First Search
    """

    @staticmethod
    def distance(x1, y1, x2, y2):
        return abs(x2 - x1) + abs(y2 - y1)

    def remove(self):
        if self.is_empty():
            raise Exception("empty frontier")
        else:
            # remove the node that is closest to the goal
            min = math.inf
            for i, node in enumerate(self.frontier):
                if node.state == self.goal:
                    self.frontier.remove(node)
                    return node
                else:
                    dist = self.__class__.distance(
                        node.state[0], node.state[1], self.goal[0], self.goal[1]
                    )
                    if dist < min:
                        min = dist
                        min_node = node

            self.frontier.remove(min_node)
            return min_node
