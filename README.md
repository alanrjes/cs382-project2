# Algorithms Project 2

Alan Jessup, 22 November 2023

## Project Logistics

### Timeline

So far, I've drafted the code for part 1, but not yet tested/debugged.

The plan is to test/debug and complete part 2 of this project before the due date, December 4.

### Distribution of work

As the only member of my group, I will do all parts of the code & design document writing.

## Implementation

### Graphs & Vertices

I chose to represent graphs through dictionaries (hash tables) in combination with `Vertex` class attributes that make a sort of linked-list.

Each `Graph` object has a dictionary of `{key : Vertex object}` containing all vertices in the graph. Each `Vertex` object has two dictionaries containing the keys of each neighboring vertex:

- `{key : edge weight}`, to track the edge weight between the `self` and `key` vertices.
- `{key : Vertex object}`, to form a linked-list of neighboring vertices.

I chose these data structures because a hash table is the most efficient way to access a large number of key-indexed `Vertex` objects by key for structural features like building/deleting, and a linked-list is the most efficient way to navigate between neighboring objects to traverse graph.

### Maps

The `Map` class represents obstacles by removing the vertex at that location. Upon building, vertices are created and connected at all non-obstacle integer coordinates, and adding/removing vertices changes obstacles.

Importantly, all `Vertex` keys in a `Map` object are coordinate tuples in the form `(x, y)`, and are indexed as such in all dictionaries. All edge weights are default 1 and values are n/a.

ASCII display to-be-coded.
