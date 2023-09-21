import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        # if self.size() > 0:
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            return None

    def __str__(self):
        return_string = ""
        for item in self.stack:
            return_string += f'{item}, '
        return f'[{return_string}]'


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        # Maps IDs to User objects
        self.users = {}
        # Adjacency List
        # Maps user_ids to a list of other users (who are their friends)
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME
        # Add users
        for i in range(0, num_users):
            self.add_user(f'User {i + 1}')

        # Create friendships
        # Generate ALL possible friendships
        # Avoid duplicate friendships
        possible_friendships = []
        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):  # self.last_id+1 == len(self.users.keys())
                # user_id == friend_id cannot happen
                # If friendship between friend_id and user_id
                #     Don't add friendship between friend_id and user_id
                possible_friendships.append((user_id, friend_id))
        # Randomly select X friendships
        # X = num_users * avg_friendships // 2
        random.shuffle(possible_friendships)
        num_friendships = num_users * avg_friendships // 2
        for i in range(0, num_friendships):
            friendship = possible_friendships[i]
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # Create a queue
        queue = Queue()
        # Create a set of visited Vertives
        visited = {}
        # Add first user_id to the queue as a path
        queue.enqueue([user_id])

        # While the queue is not empty:
        while queue.size() > 0:
            # Dequeue a current path
            current_path = queue.dequeue()
            # Get the current vertex from end of path
            current_vertex = current_path[-1]
            # If current vertex NOT visited:
            if current_vertex not in visited:
                # Add vertex to visited set
                # Also add path that brought us to this vertex
                # i.e. add a key and value to the visited dictionary
                    # The key is the current vertex, and the value is the path
                visited[current_vertex] = current_path
                # Queue up all neighbors as paths
                for neighbor in self.friendships[current_vertex]:
                    new_path = current_path.copy()
                    new_path.append(neighbor)
                    queue.enqueue(new_path)

        return visited

    # def get_all_social_paths(self, user_id):
    #     """
    #     Takes a user's user_id as an argument
    #
    #     Returns a dictionary containing every user in that user's
    #     extended network with the shortest friendship path between them.
    #
    #     The key is the friend's ID and the value is the path.
    #     """
    #     visited = {
    #         # 2: [1, 2],
    #         # 3: [4, 5, 6, 2, 3]  #, etc, etc, ...
    #     }  # Note that this is a dictionary, not a set
    #     # !!!! IMPLEMENT ME
    #     # Temporary path for DFT
    #     path = []
    #     # Stack to keep next-ups
    #     stack = Stack()
    #
    #     # Add initial user to stack
    #     stack.push(user_id)
    #
    #     # Main lines, run until the stack is exhausted
    #     while len(stack.stack) > 0:
    #         # Set current_user to the top most user in the stack
    #         current_user = stack.pop()
    #         print(f'\n-while- on {current_user}')
    #
    #         # If we already visited this user, set the path to the current user's path
    #         if current_user in visited:
    #             path = visited[current_user]
    #             print(f"{current_user} has been visited, setting path to {current_user}'s path {path}")
    #         else:
    #             # Add the current user to the path
    #             path.append(current_user)
    #             print(f'{current_user} has NOT been visited... appending to path {path}')
    #
    #         # If the current_user hasn't been visited, make a visited entry for it and set its path to the current path
    #         if current_user not in visited:
    #             visited[current_user] = path
    #             print(f"{current_user} has NOT been visited, setting {current_user}'s path to {path}")
    #
    #             # For each neighbor that the current_user has, add to the top of stack, and add to path
    #             for neighbor in self.friendships[current_user]:
    #                 stack.push(neighbor)
    #                 # path.append(neighbor)
    #                 print(f"-for- on {neighbor}, pushing to stack {stack} and not appending to path {path}")
    #                 # new_path = list(path)
    #                 # new_path.append(neighbor)
    #
    #         # Automatically set it so no friends left (all friends already visited)
    #         friends_left = False
    #
    #         # Check each of the neighbors to see if they've been visited, if not, there are unvisited friends
    #         for neighbor in self.friendships[current_user]:
    #             print(f'-for- on {current_user} with friendships {self.friendships[current_user]}')
    #
    #             if neighbor not in visited:
    #                 print(f'neighbor {neighbor} is not in visited')
    #                 friends_left = True
    #
    #         print(f'friends_left is {friends_left}')
    #
    #         # If there are no friends left, take the current user off the path
    #         if friends_left == False:
    #             path.pop(len(path) - 1)
    #             print(f'popped')
    #
    #         print(f'new path is {path}')
    #     return visited


"""
        tracking_stack = Stack()
        tracking_stack.push({
            'current_vertex': starting_vertex,
            'path': [starting_vertex]
        })

        visited_set = set()

        while tracking_stack.size() > 0:
            current_obj = tracking_stack.pop()
            current_path = current_obj['path']
            current_vertex = current_obj['current_vertex']

            if current_vertex not in visited_set:

                visited_set.add(current_vertex)

                if current_vertex == destination_vertex:
                    return current_path

                for neighbor_vertex in self.get_neighbors(current_vertex):
                    new_path = list(current_path)
                    new_path.append(neighbor_vertex)

                    tracking_stack.push({
                        'current_vertex': neighbor_vertex,
                        'path': new_path
                    })
        return None"""

if __name__ == '__main__':
    sg = SocialGraph()
    # sg.populate_graph(5, 2)
    sg.add_user("1")
    sg.add_user("2")
    sg.add_user("3")
    sg.add_user("4")
    sg.add_user("5")
    sg.add_user("6")
    sg.add_friendship(1, 5)
    sg.add_friendship(1, 3)
    sg.add_friendship(2, 3)
    sg.add_friendship(3, 5)
    sg.add_friendship(4, 5)
    sg.add_friendship(2, 6)
    print(sg.friendships)
    connections = sg.get_all_social_paths(5)
    print(connections)
