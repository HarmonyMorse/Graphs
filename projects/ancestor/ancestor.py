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


def earliest_ancestor(ancestors, starting_node):
    tracking_queue = Queue()
    tracking_queue.enqueue(starting_node)
    cur = -1

    while tracking_queue.size() > 0:
        cur = tracking_queue.dequeue()
        adding = []
        for duo in ancestors:
            if duo[1] == cur:
                adding.append(duo[0])
        if len(adding) > 0:
            tracking_queue.enqueue(min([num for num in adding]))

    if cur == starting_node:
        cur = -1
    print(f'{starting_node} -> {cur}')
    return cur
