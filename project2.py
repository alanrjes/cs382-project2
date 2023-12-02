# expanded & modified from starter code file
# chars for prints: ↑ ↓ → ← —
from math import inf

class Vertex:
    def __init__(self, key, value, neighbors):
        self.key = key
        self.value = value
        self.edges = {}
        self.neighbors = {}
        for vertex in neighbors:
            self.neighbors[vertex.key] = vertex
            self.edges[vertex.key] = 1  # default edge weight
            vertex.neighbors[self.key] = self
            vertex.edges[self.key] = 1
        # for use in BFS
        self.visited = False
    
    def delete_from_neighbors(self):
        for vertex in self.neighbors.values():
            del vertex.neighbors[self.key]
            del vertex.edges[self.key]

class Graph:
    # represents an undirected weighted graph
    def __init__(self, vertices=[]):
        self.vertices = {}
        for vertex in vertices:
            self.vertices[vertex.key] = vertex

    def get_weight(self, v1, v2):
        # returns the weight of edge between v1 and v2 if it exists (None otherwise)
        if v2.key in v1.edges:
            return v1.edges[v2.key]

    def add_vertex(self, k, v, neighbors=[]):
        # k, v: key and value for the new vertex
        # neighbors: the new vertex's neighbors, as a list of vertex objects
        self.vertices[k] = Vertex(k, v, neighbors)

    def delete_vertex(self, v): # v: vertex object to be deleted
        # delete from LL of neighboring vertices & corresponding edge
        # delete v from graph
        v.delete_from_neighbors()
        del self.vertices[v.key]

    def add_edge(self, v1, v2, w):
        # adds an edge with weight w between the vertices corresponding to keys v1, v2 (if it doesn't already exist)
        if v2.key not in v1.neighbors:
            v1.neighbors[v2.key] = v1
            v1.edges[v2.key] = w
            v2.neighbors[v1.key] = v2
            v2.edges[v1.key] = w

    def delete_edge(self, v1, v2):
        # deletes the edge between the vertices corresponding to keys v1, v2 (if it exists)
        if v2.key in v1.neighbors:
            del v1.neighbors[v2.key]
            del v1.edges[v2.key]
            del v2.neighbors[v1.key]
            del v2.edges[v1.key]


class Map(Graph):
    def __init__(self, n, obstacles=[]):
        # creates a map representing the squares of n by n grid
        # optional argument: list of (x,y) locations indicating obstacles (cannot pass through)
        super().__init__()
        # create & connect vertices
        for x in range(n):
            for y in range(n):
                if (x, y) not in obstacles:
                    neighbors = []
                    for k in [(x-1, y), (x, y-1)]:
                        if k in self.vertices:
                            neighbors.append(self.vertices[k])
                    self.add_vertex((x, y), None, neighbors)
        self.size = n
    
    def print_pretty(self):
        # prints a pretty ASCII picture of the map using different characters for "open" spaces and obstacles
        mapLen = self.size*2-1
        mapStr = [[" "]*mapLen for i in range(mapLen)]
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) in self.vertices:
                    mapStr[y*2][x*2] = "X"
                    if (x-1, y) in self.vertices:
                        mapStr[y*2][x*2-1] = "—"
                    if (x+1, y) in self.vertices:
                        mapStr[y*2][x*2+1] = "—"
                    if (x, y-1) in self.vertices:
                        mapStr[y*2-1][x*2] = "|"
                    if (x, y+1) in self.vertices:
                        mapStr[y*2+1][x*2] = "|"
        for row in mapStr:
            print(" ".join(row))

    def add_obstacle(self, x, y):
        # adds an obstacle at position (x, y) (if it doesn't already exist) by deleting that vertex
        self.delete_vertex(self.vertices[(x, y)])

    def remove_obstacle(self, x, y):
        # removes an obstacle at position (x,y) (if it exists) by creating a vertex there
        neighbors = []
        for k in [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]:
            if k in self.vertices:
                neighbors.append(self.vertices[k])
        self.add_vertex((x, y), None, neighbors)

    def is_obstacle(self, x, y):
        return (x, y) not in self.vertices

    def WFS(self, start_key, h):
        # h takes parameters (k=key of vertex to be weighted, v=current vertex object, m=map object)
        # returns a dictionary of {key : {"d": distance of shortest path to node at key, "p": id of predecessor on shortest path}}
        shortestPaths = { k : {"d": inf, "p": None} for k in self.vertices}
        shortestPaths[start_key]["d"] = 0
        self.traverse(self.vertices[start_key], 0, shortestPaths, h)
        return shortestPaths
    
    def traverse(self, v, d, shortestPaths, h):
        # recursive helper for BFS
        if not v.visited:
            h_key = lambda k : h(k, v, self)
            Q = sorted(v.neighbors.keys(), key=h_key)
            for k in Q:
                kd = d + v.edges[k]
                if shortestPaths[k]["d"] > kd:
                    shortestPaths[k]["d"] = kd
                    shortestPaths[k]["p"] = v.key
                    self.traverse(v.neighbors[k], kd, shortestPaths, h)

    def BFS(self, start_key):
        h = lambda k, v, m : 1  # arbitrary/unsorted
        return self.WFS(start_key, h)
    
    def dijkstra(self, start_key):
        h = lambda k, v, m : v.edges[k]  # sorted by weight of edge from current vertex
        return self.WFS(start_key, h)

    def print_search(self, shortestPaths):
        mapLen = self.size*2-1
        mapStr = [[" "]*mapLen for i in range(mapLen)]
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) in self.vertices:
                    mapStr[y*2][x*2] = str(shortestPaths[(x, y)]["d"])
                    if (x-1, y) == shortestPaths[(x, y)]["p"]:
                        mapStr[y*2][x*2-1] = "←"
                    if (x+1, y) == shortestPaths[(x, y)]["p"]:
                        mapStr[y*2][x*2+1] = "→"
                    if (x, y-1) == shortestPaths[(x, y)]["p"]:
                        mapStr[y*2-1][x*2] = "↑"
                    if (x, y+1) == shortestPaths[(x, y)]["p"]:
                        mapStr[y*2+1][x*2] = "↓"
        for row in mapStr:
            print(" ".join(row))

    def SPSP(self, start, end, h=lambda k, v, m : 1, shortestPaths=None):
        # h has same criteria as for WFS, but default BFS
        # calculate shortestPaths only on first occurrence:
        if not shortestPaths:
            shortestPaths = self.WFS(start, h)
        # returns an array of {"k":key, "d":distance} for each vertex passed in the shortest path, in order from start -> end
        if start == end:
            return [{"k":start, "d":0}]  # base case
        path = shortestPaths[end]
        return self.SPSP(start, path["p"], h, shortestPaths) + [{"k": end, "d": path["d"]}]

    def print_path(self, path):
        mapLen = self.size*2-1
        mapStr = [[" "]*mapLen for i in range(mapLen)]
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) in self.vertices:
                    mapStr[y*2][x*2] = "."
        # draw path after overall map is drawn, easier this way for ordered array
        for i in range(len(path)):
            (x, y) = path[i]["k"]
            d = path[i]["d"]
            mapStr[y*2][x*2] = str(d)
            if i < len(path)-1:
                if path[i+1]["k"] == (x-1, y):
                    mapStr[y*2][x*2-1] = "←"
                if path[i+1]["k"] == (x+1, y):
                    mapStr[y*2][x*2+1] = "→"
                if path[i+1]["k"] == (x, y-1):
                    mapStr[y*2-1][x*2] = "↑"
                if path[i+1]["k"] == (x, y+1):
                    mapStr[y*2+1][x*2] = "↓"
        for row in mapStr:
            print(" ".join(row))


myMap = Map(5, obstacles = [(2, 2), (0, 4)])

def part_A_test():  # Example for part A -->
    print("Map, printed prettily:")
    myMap.print_pretty()
    print()
    print("Is (0, 4) an obstacle?", myMap.is_obstacle(0, 4))
    print()
    print("Remove (0, 4) as obstacle:")
    myMap.remove_obstacle(0, 4)
    myMap.print_pretty()
    print()
    print("Is (0, 4) an obstacle?", myMap.is_obstacle(0, 4))
    print()
    print("Add (3, 0) as obstacle:")
    myMap.add_obstacle(3, 0)
    myMap.print_pretty()
    print()

def part_B_test():  # Example for part B -->
    ps = myMap.BFS((0, 0))
    print("All shortest paths to (0, 0) using BFS:")
    myMap.print_search(ps)
    print()
    print("SPSP from (0, 0) to (4, 0) using BFS by default:")
    p = myMap.SPSP((0, 0), (4, 0))
    myMap.print_path(p)
    print()

def part_C_test():  # Example for part C -->
    ps = myMap.dijkstra((4, 2))
    print("All shortest paths to (0, 0) using Dijkstra's:")
    myMap.print_search(ps)
    print()
    print("SPSP from (0, 0) to (4, 1) using WFS Dijkstra's:")
    p = myMap.SPSP((4, 2), (0, 3), h=lambda k, v, m : v.edges[k])
    myMap.print_path(p)

part_A_test()
part_B_test()
part_C_test()
