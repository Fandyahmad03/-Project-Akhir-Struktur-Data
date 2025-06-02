class Node:
    def __init__(self, key):
        self.key = key
        self.children = []

class Graph:
    def __init__(self):
        self.nodes = {}
    
    def add_node(self, key):
        if key not in self.nodes:
            self.nodes[key] = Node(key)
    
    def add_edge(self, from_key, to_key):
        self.add_node(from_key)
        self.add_node(to_key)
        self.nodes[from_key].children.append(self.nodes[to_key])
    
    def get_graph(self):
        result = {}
        for key, node in self.nodes.items():
            result[key] = [child.key for child in node.children]
        return result

class PriorityQueue:
    def __init__(self):
        self.queue = []
    
    def push(self, priority, item):
        self.queue.append((priority, item))
        self.queue.sort(key=lambda x: x[0], reverse=True)
    
    def pop(self):
        if self.queue:
            return self.queue.pop(0)[1]
        return None
    
    def peek(self):
        if self.queue:
            return self.queue[0][1]
        return None
    
    def is_empty(self):
        return len(self.queue) == 0

class HashMap:
    def __init__(self):
        self.size = 1000
        self.map = [[] for _ in range(self.size)]
    
    def _get_hash(self, key):
        return hash(key) % self.size
    
    def set(self, key, value):
        key_hash = self._get_hash(key)
        key_exists = False
        bucket = self.map[key_hash]
        for i, kv in enumerate(bucket):
            k, v = kv
            if k == key:
                bucket[i] = (key, value)
                key_exists = True
                break
        if not key_exists:
            bucket.append((key, value))
    
    def get(self, key):
        key_hash = self._get_hash(key)
        bucket = self.map[key_hash]
        for k, v in bucket:
            if k == key:
                return v
        return None
    
    def delete(self, key):
        key_hash = self._get_hash(key)
        bucket = self.map[key_hash]
        for i, kv in enumerate(bucket):
            k, v = kv
            if k == key:
                del bucket[i]
                return True
        return False

class Queue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, item):
        self.queue.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None
    
    def is_empty(self):
        return len(self.queue) == 0

class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, item):
        self.stack.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def is_empty(self):
        return len(self.stack) == 0
