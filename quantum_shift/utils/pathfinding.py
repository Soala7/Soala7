# quantum_shift/utils/pathfinding.py
import pygame
import heapq
import math
from settings import *

class PathfindingNode:
    """Node for A* pathfinding"""
    def __init__(self, x, y, g=0, h=0, parent=None):
        self.x = x
        self.y = y
        self.g = g  # Distance from start
        self.h = h  # Heuristic (distance to goal)
        self.f = g + h  # Total cost
        self.parent = parent
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class Pathfinder:
    """A* pathfinding implementation"""
    def __init__(self):
        self.grid_size = 32  # Pathfinding grid resolution
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
    
    def heuristic(self, node1, node2):
        """Calculate heuristic distance between nodes"""
        return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
    
    def get_neighbors(self, node, grid):
        """Get valid neighboring nodes"""
        neighbors = []
        
        for dx, dy in self.directions:
            new_x = node.x + dx
            new_y = node.y + dy
            
            if (0 <= new_x < len(grid[0]) and 
                0 <= new_y < len(grid) and 
                grid[new_y][new_x] == 0):  # 0 = walkable
                
                neighbors.append(PathfindingNode(new_x, new_y))
        
        return neighbors
    
    def find_path(self, start_pos, goal_pos, obstacles=None):
        """Find path using A* algorithm"""
        # Convert world coordinates to grid coordinates
        start_grid = (int(start_pos[0] // self.grid_size), int(start_pos[1] // self.grid_size))
        goal_grid = (int(goal_pos[0] // self.grid_size), int(goal_pos[1] // self.grid_size))
        
        # Create simplified grid
        grid_width = SCREEN_WIDTH // self.grid_size
        grid_height = SCREEN_HEIGHT // self.grid_size
        grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        
        # Mark obstacles
        if obstacles:
            for obstacle in obstacles:
                obs_x = int(obstacle.x // self.grid_size)
                obs_y = int(obstacle.y // self.grid_size)
                obs_w = int(obstacle.width // self.grid_size) + 1
                obs_h = int(obstacle.height // self.grid_size) + 1
                
                for y in range(obs_y, min(obs_y + obs_h, grid_height)):
                    for x in range(obs_x, min(obs_x + obs_w, grid_width)):
                        if 0 <= x < grid_width and 0 <= y < grid_height:
                            grid[y][x] = 1  # 1 = blocked
        
        # Check bounds
        if (start_grid[0] < 0 or start_grid[0] >= grid_width or
            start_grid[1] < 0 or start_grid[1] >= grid_height or
            goal_grid[0] < 0 or goal_grid[0] >= grid_width or
            goal_grid[1] < 0 or goal_grid[1] >= grid_height):
            return []
        
        # Initialize nodes
        start_node = PathfindingNode(start_grid[0], start_grid[1])
        goal_node = PathfindingNode(goal_grid[0], goal_grid[1])
        
        # A* algorithm
        open_set = [start_node]
        closed_set = set()
        
        while open_set:
            current_node = heapq.heappop(open_set)
            
            if current_node == goal_node:
                # Reconstruct path
                path = []
                while current_node:
                    # Convert back to world coordinates
                    world_x = current_node.x * self.grid_size + self.grid_size // 2
                    world_y = current_node.y * self.grid_size + self.grid_size // 2
                    path.append((world_x, world_y))
                    current_node = current_node.parent
                return path[::-1]  # Reverse to get start-to-goal path
            
            closed_set.add(current_node)
            
            for neighbor in self.get_neighbors(current_node, grid):
                if neighbor in closed_set:
                    continue
                
                # Calculate distances
                g = current_node.g + self.heuristic(current_node, neighbor)
                h = self.heuristic(neighbor, goal_node)
                neighbor.g = g
                neighbor.h = h
                neighbor.f = g + h
                neighbor.parent = current_node
                
                # Check if this path to neighbor is better
                better_path = True
                for open_node in open_set:
                    if neighbor == open_node and neighbor.g >= open_node.g:
                        better_path = False
                        break
                
                if better_path:
                    heapq.heappush(open_set, neighbor)
        
        return []  # No path found
    
    def smooth_path(self, path):
        """Smooth the path by removing unnecessary waypoints"""
        if len(path) <= 2:
            return path
        
        smoothed = [path[0]]
        
        for i in range(1, len(path) - 1):
            # Check if we can skip this waypoint
            prev_point = smoothed[-1]
            next_point = path[i + 1]
            
            # Simple line-of-sight check
            if not self.line_of_sight(prev_point, next_point):
                smoothed.append(path[i])
        
        smoothed.append(path[-1])
        return smoothed
    
    def line_of_sight(self, start, end):
        """Check if there's a clear line of sight between two points"""
        # Simple implementation - just check if points are close enough
        distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        return distance < self.grid_size * 3

# =============================================================================

# quantum_shift/utils/pathfinding.py
import pygame
import heapq
import math
from settings import *