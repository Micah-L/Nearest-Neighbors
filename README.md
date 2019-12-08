# Nearest-Neighbors

This is a simple nearest neighbors algorithm, using a kdtree for fast lookup. It can take a list of nodes in space, and output which nodes are within a specified distance -- the search radius `r`.

## Usage
To run:

```
Nearest_Neighbors.py [input file]
```

## Input

The input file must be of the following form: The first `k` lines contain coordinates of each node, indexed by their ID (going from `1` to `k`) and separated by spaces. The last line is the search radius `r`. See the example input files.

## Output

The program outputs a list of each node, followed by the number of nodes nearby (nearby is defined as being within a distance `r` away), and the ID of each nearby node.

