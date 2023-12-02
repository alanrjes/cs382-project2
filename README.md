# Algorithms Project 2

Alan Jessup, 1 November 2023

### Distribution of work

As the only member of my group, I am responsible for all parts of the code & design document.

## Implementation

### Graph & Vertex objects

I chose to represent graphs through dictionaries (hash tables) in combination with `Vertex` class attributes that make a sort of linked-list.

Each `Graph` object has a dictionary of `{key : Vertex object}` containing all vertices in the graph. Each `Vertex` object has two dictionaries containing the keys of each neighboring vertex:

- `{key : edge weight}`, to track the edge weight between the `self` and `key` vertices.
- `{key : Vertex object}`, to form a linked-list of neighboring vertices.

I chose these data structures because a hash table is the most efficient way to access a large number of key-indexed `Vertex` objects by key for structural features like building/deleting, and a linked-list is the most efficient way to navigate between neighboring objects to traverse graph.

### Map objects

The `Map` class represents obstacles by removing the vertex at that location. Upon building, vertices are created and connected at all non-obstacle integer coordinates, and adding/removing vertices changes obstacles.

Importantly, all `Vertex` keys in a `Map` object are coordinate tuples in the form `(x, y)`, and are indexed as such in all dictionaries. All edge weights are default 1 and values are n/a.

### Map ASCII printing

The ASCII map for a map of size _n_ is initialized as a list of (_2n-1_)-size strings. The size is such that each vertex `(x, y)` is located at `[2y][2x]`, and edges can be drawn using odd-indexed characters positioned relative to a vertex.

Map printing is done simply by iterating through the vertices in a map from the top-left (0, 0) to the bottom-right and replacing the appropriate characters (`X` for a vertex, `—` or `|` for an edge) on each iteration.

### Single-source "Whatever-first" search

The `WFS` function is the foundation for my `BFS` and `dijkstra` implementations, adapted for my original implementation of BFS. The resulting `shortestPaths` data structure is a dictionary of all keys in a graph, structured as:

```
{ key (x, y) : { "d" : int distance of shortest path,
                 "p" : key of predecessor along shortest path } }
```

After initializing `shortestPaths`, it calls the recursive function `traverse` to visit each not-yet-visited vertex and fill in the `shortestPaths` dictionary.

The order in which paths are visited, which differentiates BFS from dijkstra's algorithm, or any other search, depends on the heuristic function `h` and the weight it returns. It takes the following arguments:

- `k` : key of the vertex being positioned in the queue.
- `v` : current vertex from which distance for dijkstra's is being measured.
- `m` : object of map (not needed for any of these implementations, but was suggested in the instructions to include)

### Breadth-first search

For BFS, `h` returns `1` for all vertices, since the order is arbitrary.

### Dijkstra's algorithm

For dijkstra's, `h` returns the weight of the edge leading to the vertex being sorted (represented by its key `k`, not its object), from the current-position vertex object `v`.

### Shortest-path search printing

`Map.print_search` is largely the same as the original `Map.pretty_print`, except:

- Instead of printing `X` for a vertex, the integer distance of the shortest path from the starting coordinate to that vertex is printed.
- Arrows are printed for edges instead of lines, to indicate the direction of the path.
- Instead of checking the vertex's neighbor data structure to determine whether to print an edge, it checks the predecessor field in the `shortestPaths` dictionary.

The same print function can be used for any variation of WFS, since the output is always structured the same.

### Single-pair shortest paths

Returns an ordered array of two-value dictionaries `{ "k" : key, "d" : distance }`, one for each vertex along the shortest path, ordered from start to end. Does so by simply backtracking along the path given by WFS, recursing on the predecessor to the end-vertex as the new end-vertex until the start vertex is reached.

### Single-pair search printing

Again, printing the result of a single-pair shortest path search with `Map.print_path` is done similarly to the other print functions. The main difference in this case is that the regular map is drawn first, with `.` in the place of vertices, and then the vertices specifically in the path are iterated over to draw the path.

## Demo

The functions `part_A_test`, `part_B_test`, and `part_C_test` include simple examples of the map functionalities included in each part, respectively. They print the following results when all run sequentially on the same map, with starting obstacles at (2, 2) and (0, 4):

### Part A

```
Map, printed prettily:
X — X — X — X — X
|   |   |   |   |
X — X — X — X — X
|   |       |   |
X — X       X — X
|   |       |   |
X — X — X — X — X
    |   |   |   |
    X — X — X — X

Is (0, 4) an obstacle? True

Remove (0, 4) as obstacle:
X — X — X — X — X
|   |   |   |   |
X — X — X — X — X
|   |       |   |
X — X       X — X
|   |       |   |
X — X — X — X — X
|   |   |   |   |
X — X — X — X — X

Is (0, 4) an obstacle? False

Add (3, 0) as obstacle:
X — X — X       X
|   |   |       |
X — X — X — X — X
|   |       |   |
X — X       X — X
|   |       |   |
X — X — X — X — X
|   |   |   |   |
X — X — X — X — X
```

### Part B

```
All shortest paths to (0, 0) using BFS:
0 ← 1 ← 2       6
↑               ↓
1 ← 2 ← 3 ← 4 ← 5
↑           ↑
2 ← 3       5 ← 6
↑
3 ← 4 ← 5 ← 6 ← 7
↑   ↑
4   5 ← 6 ← 7 ← 8

SPSP from (0, 0) to (4, 0) using BFS by default:
0   .   .       6
↓               ↑
1 → 2 → 3 → 4 → 5

.   .       .   .

.   .   .   .   .

.   .   .   .   .
```

### Part C

```
All shortest paths to (0, 0) using Dijkstra's:
6   5   4       2
↓   ↓   ↓       ↓
5 → 4 → 3 → 2   1
↑   ↑       ↓   ↓
6   5       1 → 0
            ↑   ↑
5 → 4 → 3 → 2   1
↑   ↑   ↑   ↑   ↑
6   5   4   3   2

SPSP from (4, 2) to (0, 3) using WFS Dijkstra's:
.   .   .       .

.   .   .   .   .

.   .       1 ← 0
            ↓
5 ← 4 ← 3 ← 2   .

.   .   .   .   .
```
