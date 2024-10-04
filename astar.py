import time
import random
import sys

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    #Track nodes created
    nodes_created = 0

    # Add the start node
    open_list.append(start_node)

    #Track time
    start_time = time.time()

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            total_cost = 0
            while current is not None:
                path.append(current.position)
                if current != start_node:
                    total_cost += maze[current.position[0]][current.position[1]]
                current = current.parent
            end_time = time.time()
            runtime = (end_time - start_time) * 1000 # milliseconds
            print(f"Path Cost: {total_cost}")
            print(f"Path: {path[:: -1]}")
            print(f"Nodes Created: {nodes_created}")
            print(f"Runtime: {runtime:.2f} ms")
            return
        
        # Generate childrenexit
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Modified to use only up down left and right

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] < 0 or node_position[0] >= len(maze) or node_position[1] < 0 or node_position[1] >= len(maze[0]):
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)
            nodes_created += 1

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

           # Create g, h, and f values
            child.g = current_node.g + maze[child.position[0]][child.position[1]]
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])  # Manhattan distance
            child.f = child.g + child.h

           # Child is already in the open list with a higher g (cost)
            if len([open_node for open_node in open_list if child == open_node and child.g >= open_node.g]) > 0:
                continue

            # Add the child to the open list
            open_list.append(child)
    
    #If no path is found
    end_time = time.time()
    runtime = (end_time - start_time) * 1000
    print("Path cost: -1")
    print("Path: NULL")
    print(f"Nodes Created: {nodes_created}")
    print(f"Runtime: {runtime:.2f} ms")

def get_maze(maze_number):

    mazes = {
        1: [[2, 4, 2, 1, 4, 5, 2],
             [0, 1, 2, 3, 5, 3, 1],
             [2, 0, 4, 4, 1, 2, 4],
             [2, 5, 5, 3, 2, 0, 1],
             [4, 3, 3, 2, 1, 0, 1]
        ],
        2: [[1, 3, 2, 5, 1, 4, 3],
             [2, 1, 3, 1, 3, 2, 5],
             [3, 0, 5, 0, 1, 2, 2],
             [5, 3, 2, 1, 5, 0, 3],
             [2, 4, 1, 0, 0, 2, 0],
             [4, 0, 2, 1, 5, 3, 4],
             [1, 5, 1, 0, 2, 4, 1]
        ],
        3: [[2, 0, 2, 0, 2, 0, 0, 2, 2, 0],
             [1, 2, 3, 5, 2, 1, 2, 5, 1, 2],
             [2, 0, 2, 2, 1, 2, 1, 2, 4, 2],
             [2, 0, 1, 0, 1, 1, 1, 0, 0, 1],
             [1, 1, 0, 0, 5, 0, 3, 2, 2, 2],
             [2, 2, 2, 2, 1, 0, 1, 2, 1, 0],
             [1, 0, 2, 1, 3, 1, 4, 3, 0, 1],
             [2, 0, 5, 1, 5, 2, 1, 2, 4, 1],
             [1, 2, 2, 2, 0, 2, 0, 1, 1, 0],
             [5, 1, 2, 1, 1, 1, 2, 0, 1, 2]
        ],
        4: [[1, 1, 0, 2, 3, 4, 5, 0, 1, 2],
             [1, 2, 0, 0, 0, 3, 1, 2, 0, 3],
             [3, 1, 5, 1, 0, 1, 2, 0, 4, 1],
             [0, 0, 1, 2, 3, 1, 1, 5, 1, 1],
             [2, 1, 1, 0, 2, 0, 2, 1, 1, 3],
             [1, 5, 0, 2, 0, 3, 4, 2, 1, 0],
             [2, 0, 2, 0, 0, 1, 0, 1, 2, 5],
             [3, 1, 1, 0, 4, 1, 5, 1, 0, 1],
             [1, 1, 0, 2, 1, 3, 1, 1, 1, 0],
             [5, 1, 1, 0, 1, 1, 1, 0, 2, 1]
        ],
        5: [[1, 1, 0, 2, 3, 4, 5, 0, 1, 2, 1, 3 ,0, 3],
             [1, 2, 0, 0, 0, 3, 1, 2, 0, 3, 1, 0, 0, 2],
             [3, 1, 5, 1, 0, 1, 2, 0, 4, 1, 1, 3, 0, 2],
             [4, 0, 1, 2, 3, 1, 0, 5, 1, 1, 5, 1, 1, 0],
             [2, 1, 1, 0, 2, 5, 2, 1, 1, 3, 2, 2, 3, 1],
             [1, 5, 0, 2, 0, 3, 4, 2, 1, 0, 3, 0, 2, 1],
             [2, 0, 2, 2, 1, 1, 0, 1, 2, 5, 0, 2, 1, 2],
             [3, 1, 1, 0, 4, 1, 5, 1, 0, 1, 1, 2, 1, 0],
             [1, 1, 0, 2, 1, 3, 1, 1, 1, 0, 4, 2, 1, 1],
             [5, 1, 1, 0, 1, 1, 1, 0, 2, 1, 3, 2, 1, 2],
             [2, 0, 2, 0, 0, 1, 0, 1, 2, 5, 0, 2, 1, 2],
             [3, 1, 1, 1, 4, 1, 5, 1, 0, 1, 1, 2, 1, 0],
             [1, 1, 0, 2, 1, 0, 1, 1, 1, 0, 4, 2, 1, 1],
             [5, 1, 1, 0, 1, 1, 1, 0, 2, 1, 3, 2, 1, 1]
        ]
    }

    return mazes.get(maze_number)

def heuristic_h1(node, goal):
    return 0

def heurstic_h2(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

def heuristic_h3(node, goal):
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1]) * 1.5  # For example, adding a penalty for vertical movement

def heuristic_h4(node, goal):
    manhattan_distance = abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    error = random.choice([-3, -2, -1, 1, 2, 3])
    return max(0, manhattan_distance + error)  # Ensuring the heuristic is non-negative

def main():

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (7, 6)

    path = astar(maze, start, end)
    print(path)
    print("\n" + "="*30 + "\n")

    # Test case 1
    maze1 = get_maze(1)
    start1 = (1, 2)
    end1 = (4, 3)
    print("Test Case 1")
    astar(maze1, start1, end1)
    print("\n" + "="*30 + "\n")
    
    # Test case 2
    maze2 = get_maze(2)
    start2 = (3, 6)
    end2 = (5, 1)
    print("Test Case 2")
    astar(maze2, start2, end2)
    print("\n" + "="*30 + "\n")
    
    # Test case 3
    maze3 = get_maze(3)
    start3 = (1, 2)
    end3 = (8, 8)
    print("Test Case 3")
    astar(maze3, start3, end3)
    print("\n" + "="*30 + "\n")

    # Test case 4
    maze4 = get_maze(4)
    start4 = (0, 0)
    end4 = (9, 9)
    print("Test Case 4")
    astar(maze4, start4, end4)
    print("\n" + "="*30 + "\n")

    # Test case 5
    maze5 = get_maze(5)
    start5 = (0, 0)
    end5 = (13, 13)
    print("Test Case 5")
    astar(maze5, start5, end5)
    print("\n" + "="*30 + "\n")

if __name__ == '__main__':
    main()
