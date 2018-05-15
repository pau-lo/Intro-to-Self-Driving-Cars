'''
Inspired by:

https://en.wikipedia.org/wiki/A*_search_algorithm

and

https://www.redblobgames.com/pathfinding/a-star/implementation.html

'''


from queue import PriorityQueue
import math

# Using the Greedy and Best-First Search (a heuristic function)
# Returns eucludian distance between given two nodes


def get_heuristic(start, goal):
    '''Returns ecludian distance between given two points/nodes'''
    return math.sqrt((start[0] - goal[0])**2 + (start[1] - goal[1])**2)

#  A* uses both the heuristic and the ordering from Dijkstra’s Algorithm.
# creating the A * algorithm

def shortest_path(M, start, goal):
    # creating priority queue
    open_nodes = PriorityQueue()
    open_nodes.put(start, 0)

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually
    # contain the most efficient previous step.
    came_from = {}
    cost_so_far = {}
    came_from = {start: None}  # start, None
    # For each node, the cost of getting from the start node to the next node
    cost_so_far = {start: 0}  # start, 0

    while not open_nodes.empty():  
        current = open_nodes.get()  # select path with lowest cost

        if current == goal:
            # if current equals goal reconstruct path and keep on going
            # do not need to break: keep on going
            reconstruct_path(came_from, start, goal)

        for i in M.roads[current]:  # loop through nodes
            # calculate cost from start to next node
            new_cost = cost_so_far[current] + \
                get_heuristic(M.intersections[current], M.intersections[i])
            # if node has not been seen or new cost is less than cost_so_far
            # calculate new cost
            if i not in cost_so_far or new_cost < cost_so_far[i]:
                cost_so_far[i] = new_cost
                new_score = new_cost + \
                    get_heuristic(
                        M.intersections[current], M.intersections[i])
                # put path into priority queue and new score
                open_nodes.put(i, new_score)
                came_from[i] = current

    return reconstruct_path(came_from, start, goal)


def reconstruct_path(came_from, start, goal):  # came_from , start, goal
    current = goal
    return_path = [current]
    while current != start:
        current = came_from[current]
        return_path.append(current)
    return_path.reverse()
    return return_path
