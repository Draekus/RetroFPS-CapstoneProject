from collections import deque
from functools import lru_cache


class PathFinding:
    """Pathfinding class for finding the shortest path between two points"""

    def __init__(self, game):
        """Initialize pathfinding class"""
        self.game = game
        self.map = game.map.mini_map
        self.ways = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        self.graph = {}
        self.get_graph()

    @lru_cache  # cache the paths so they are only calculated once
    def get_path(self, start, goal):
        """Get path from start pos to end pos"""
        self.visited = self.bfs(start, goal, self.graph)
        path = [goal]
        step = self.visited.get(goal, start)

        # While there is a valid step & step is not the start
        while step and step != start:
            # Add step to path
            path.append(step)
            # Set step to the next step
            step = self.visited.get(step, start)
        # If step is the start, return the path
        return path[-1]

    def bfs(self, start, goal, graph):
        """Breadth-first search of graph of map grid"""
        # Create a queue of nodes to visit
        queue = deque([start])
        # Create a dictionary of visited nodes
        visited = {start: None}
        # While there are nodes to visit
        while queue:
            # Pop the first node
            cur_node = queue.popleft()
            # If the node is the goal, break
            if cur_node == goal:
                break
            # Get the next nodes
            next_nodes = graph[cur_node]
            # For each next node
            for next_node in next_nodes:
                # If the node has not been visited & isn't occupied by an npc
                if (
                    next_node not in visited
                    and next_node not in self.game.object_handler.npc_positions
                ):
                    # Add node to queue
                    queue.append(next_node)
                    # Add node to visited
                    visited[next_node] = cur_node
        # Return visited nodes (Path to goal)
        return visited

    def get_next_nodes(self, x, y):
        """Get next possible nodes"""
        return [
            # Calculate each possible move direction and filter nodes
            # that are not valid (walls, out of bounds, npc positions)
            (x + dx, y + dy)
            for dx, dy in self.ways
            if (x + dx, y + dy) not in self.game.map.world_map
        ]

    def get_graph(self):
        """Generate a graph of the world map"""
        for y, row in enumerate(self.map):
            for x, col in enumerate(row):
                # If current grid position is not a wall
                if not col:
                    # Add the position to the graph
                    self.graph[(x, y)] = self.graph.get(
                        (x, y), []
                    ) + self.get_next_nodes(x, y)
