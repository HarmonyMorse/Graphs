from room import Room
from player import Player
from world import World

from queue_and_stack import Queue
from queue_and_stack import Stack

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
player.current_room = world.starting_room

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = []
# trav_graph = {}


# trav_graph = {
#   0: {'n': '?', 's': 5, 'w': '?', 'e': '?'},
#   5: {'n': 0, 's': '?', 'e': '?'}
# }
"""
{0: {'n': 1, 'e': 3, 's': 5, 'w': 7}, 
5: {'n': 0, 's': 6}, 
7: {'e': 0, 'w': 8}, 
8: {'e': 7, 's': 9}, 
9: {'n': 8, 's': 10}, 
10: {'n': 9, 'e': 11}, 
11: {'e': 6, 'w': 10}, 
6: {'n': 5, 'w': 11}}
"""

#####
#                                        #
#                002                     #
#                 |                      #
#                 |                      #
#                001                     #
#                 |                      #
#                 |                      #
#      008--007--000--003--004           #
#       |         |                      #
#       |         |                      #
#      009       005                     #
#       |         |                      #
#       |         |                      #
#      010--011--006                     #
#                                        #
#####

trav_graph = {
    # Starting point
    0: {'n': '?', 'e': '?', 's': '?', 'w': '?'}

    # Various sets
    # 0: {'n': '?', 'e': '?', 's': 5, 'w': '?'},
    # 5: {'n': 0, 'e': '?', 's': '?'},

    # 0: {'n': 1, 'e': 3, 's': 5, 'w': 7},
    # 5: {'n': 0, 'e': '?', 's': '?'},
    # 7: {'e': 0, 'w': '?'}

    # After first dft
    # 0: {'n': 1, 'e': '?', 's': '?', 'w': '?'},
    # 1: {'n': 2, 's': 0},
    # 2: {'s': 1}

    # After doing 2 dft's
    # 0: {'n': 1, 'e': 3, 's': '?', 'w': '?'},
    # 1: {'n': 2, 's': 0},
    # 2: {'s': 1},
    # 3: {'e': 4, 'w': 0},
    # 4: {'w': 3}
}


def edit_trav_graph(room):
    if room.id not in trav_graph:  # If it's a brand-new room, set all its exits to '?' unless they are already in the graph then return True
        graph = {}
        for direction in room.get_exits():
            if room.get_room_in_direction(direction).id in trav_graph:
                graph[direction] = room.get_room_in_direction(direction).id

                if direction == 'n':
                    trav_graph[room.get_room_in_direction(direction).id]['s'] = room.id
                if direction == 'e':
                    trav_graph[room.get_room_in_direction(direction).id]['w'] = room.id
                if direction == 's':
                    trav_graph[room.get_room_in_direction(direction).id]['n'] = room.id
                if direction == 'w':
                    trav_graph[room.get_room_in_direction(direction).id]['e'] = room.id
            else:
                graph[direction] = '?'
        trav_graph[room.id] = graph
        return True
    else:  # It's already in the graph, so return False
        return False


# Go in a random direction (n, e, s, w) until you can't go in any to a '?' - DFT
# Use BFS to find the first room with an unexplored direction ('?') - look around without moving the player

# Returns the direction of the first unexplored room (n, s, w, e)
def check_for_unexplored(room):
    # if room.id == 7:
    #     print("7!")
    # print(f'check_for_unexplored: room: {room}')
    for exit_direction in room.get_exits():
        print(f'room: {room.id}, direction: {exit_direction}')
        if trav_graph[room.id][exit_direction] == '?':
            return exit_direction
    return None  # There are no unexplored rooms ('?') neighboring this room


# Returns the path to the first '?' without moving the player
def bfs(from_room):
    print(f'running bfs')
    queue = Queue()
    queue.enqueue({
        'path': [from_room.id],
        'room': from_room
    })
    while queue.size() > 0:
        # check each way for a '?' using player.current_room
        # return path to room in first direction (N->E->S->W) with a '?'
        current_obj = queue.dequeue()
        current_path = current_obj['path']
        current_room = current_obj['room']
        edit_trav_graph(current_room)
        first_unexplored = check_for_unexplored(current_room)
        if first_unexplored is not None:  # Found an unexplored room
            unexplored_room_id = current_room.get_room_in_direction(first_unexplored).id
            print(f'bfs found an unexplored room, path: {current_path.append(unexplored_room_id)}\ncurrent path{current_path}\nfirst unexplored: {unexplored_room_id} in direction {first_unexplored}')
            # return list(current_path).append(first_unexplored)
            return current_path[1:]
        else:  # No unexplored, keep looking
            for exit_direction in current_room.get_exits():
                # if current_room.get_room_in_direction(exit_direction).id not .,in trav_graph:
                new_path = list(current_path)
                new_path.append(current_room.get_room_in_direction(exit_direction).id)
                queue.enqueue({
                    'path': new_path,
                    'room': current_room.get_room_in_direction(exit_direction)
                })
    # print('bfs returned None')
    return None


def dft(from_room):
    current_room = from_room
    temp_path = []
    unexplored = check_for_unexplored(current_room)
    while unexplored is not None:
        # print(f'\ngraph: {trav_graph}')
        # print(f'room {current_room.id}, explored: {current_room.id in trav_graph}')
        next_room = current_room.get_room_in_direction(unexplored)
        # print(f'did_edit?: {edit_trav_graph(next_room)}; new graph: {trav_graph}')
        # print(f'current room: {current_room.id}; next room: {next_room.id}, explored? {next_room.id in trav_graph}')
        current_room = next_room
        edit_trav_graph(current_room)
        temp_path.append(current_room.id)
        # print(f'new path {temp_path}')
        if current_room in trav_graph:
            break
        # print(f'new graph: {trav_graph}')
        unexplored = check_for_unexplored(current_room)
    return temp_path


def traverse():
    trav_path = []
    current_room = player.current_room
    while True:  # len(trav_graph) != 12:
        # The path to the farthest possible room with no '?'s

        if current_room.id == 109:  # 480:
            print()

        print(f'--running dft with room {current_room.id}')
        depth = dft(current_room)

        if depth != []:
            # Add the path to trav_path
            trav_path.extend(depth)

            # Add the path to the farthest room with no '?'s
            # trav_path.extend(dft(current_room))

            current_room = world.rooms[depth[len(depth) - 1]]
            edit_trav_graph(current_room)

        # Testing break
        # if depth == [6, 11, 10, 9, 8, 7]:
        #     print("here")

        if len(trav_graph) == len(world.rooms):
            break

        # Set current_room to the last room in the path
        # current_room = world.rooms[trav_path[len(trav_path) - 1]]

        # Return a path to the nearest '?'
        breadth = bfs(current_room)

        # Add the path to the closest room with a '?'
        # trav_path.extend(bfs(current_room))

        # If there are no more rooms with '?'s, stop
        if breadth is None:  # len(breadth) == 0:
            break

        # Set current_room to the last room in the path
        # current_room = world.rooms[trav_path[len(trav_path) - 1]]
        current_room = world.rooms[breadth[len(breadth) - 1]]
        edit_trav_graph(current_room)

        # Add the path to trav_path
        trav_path.extend(breadth)

    return trav_path


def traverse1():
    path = []
    stack = Stack()

    # while len(path) < 500:
    #     for exit in player.current_room.get_exits():
    #         if True:
    #             pass
    #     # Check for '?' starting at north, adding each to the stack
    #     # Go to stack.pop()
    #     # UNLESS no '?' were found, THEN backtrack (previous path?)
    #     pass

    return ['n', 'n']


# MARK: - Running code
# print("\nPlayer's current room:")
# print(f'-{player.current_room}')
# print("ID:")
# print(f'-{player.current_room.id}')

# print("\nTesting bfs -> path_to_closest_'?'/None")
# print(f'-{bfs(player.current_room)}')

# print("\nPlayer's current room:")
# print(f'-{player.current_room}')
# print("ID:")
# print(f'-{player.current_room.id}')

# print("\nTesting dft -> path")
# print(f'-{dft(player.current_room)}')
# print(f'-{dft(world.rooms[3])}')

# print('Testing traverse()')
# print(f'---Final path:{traverse()}')

traversal_path = traverse()


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    visited_rooms.add(world.rooms[move])

    # player.travel(move)
    # visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
