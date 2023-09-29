"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""

    def __init__(self):  # space(?): O(v) + O(e)
        self.vertices = {}

    def add_vertex(self, vertex_id):  # runtime: O(1)
        """
        Add a vertex to the graph.
        """
        # Create a new key with the vertex ID, and set the value to an empty set (meaning no edges yet)
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):  # runtime: O(1)
        """
        Add a directed edge to the graph.
        """
        # Find vertex V1 in our vertices, and add V2 to the set of edges
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)

    def get_neighbors(self, vertex_id):  # runtime: O(1)
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # Create an empty queue and enqueue the starting_vertex
        # Create an empty set to track visited vertices
        tracking_queue = Queue()
        tracking_queue.enqueue(starting_vertex)

        visited_set = set()

        # While the queue is not empty:
        #     Get current vertex (dequeue from queue)
        #     Check if the current vertex has not been visited
        #       Print the current vertex
        #       Mark the current vertex as visited
        #           Add the current vertex to a visited_set
        #       Queue up all the current vertex's neighbors (so we can visit them next)
        while tracking_queue.size() > 0:
            cur = tracking_queue.dequeue()
            if cur not in visited_set:
                print(f"current vertex: {cur}")
                visited_set.add(cur)
                for vertex in self.vertices[cur]:
                    tracking_queue.enqueue(vertex)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        pass  # TODO

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        #



        pass  # TODO

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        print(f'Running BFS on {starting_vertex} -> {destination_vertex}')
        # Create an empty queue and enqueue the path to starting_vertex
        # Create an empty set to track visited vertices
        tracking_queue = Queue()
        tracking_queue.enqueue({
            'current_vertex': starting_vertex,
            'path': [starting_vertex]
        })

        visited_set = set()

        # While the queue is not empty:
        #     Get current vertex path (dequeue from queue)
        #     Set the current vertex to the last element of the path
        #     Check if the current vertex has not been visited
        #       Check if current vertex is destination
        #           If it is, stop and return
        #       Mark the current vertex as visited
        #           Add the current vertex to a visited_set
        #       Queue up new paths with each neighbor:
        #           Take the current path
        #           Append the neighbor to it
        #           Queue up new path

        while tracking_queue.size() > 0:
            current_obj = tracking_queue.dequeue()
            current_path = current_obj['path']
            current_vertex = current_obj['current_vertex']

            if current_vertex not in visited_set:

                visited_set.add(current_vertex)

                if current_vertex == destination_vertex:
                    return current_path

                for neighbor_vertex in self.get_neighbors(current_vertex):
                    new_path = list(current_path)
                    new_path.append(neighbor_vertex)

                    tracking_queue.enqueue({
                        'current_vertex': neighbor_vertex,
                        'path': new_path
                    })
        return None


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        print(f'Running DFS on {starting_vertex} -> {destination_vertex}')
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
        return None


    def dfs_recursive(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        pass  # TODO


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/BloomInstituteOfTechnology/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    # graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # graph.dft(1)
    # graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    # print(graph.dfs_recursive(1, 6))
