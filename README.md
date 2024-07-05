# Ant Colony Optimization (ACO) for the Traveling Salesman Problem (TSP)
======================================================================

This project implements the Ant Colony Optimization (ACO) algorithm to solve the Traveling Salesman Problem (TSP). The TSP is a classic optimization problem where the goal is to find the shortest possible route that visits a set of cities and returns to the origin city.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Parameters](#parameters)
  - [Example](#example)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Ant Colony Optimization (ACO) algorithm is inspired by the foraging behavior of ants. It utilizes a population of artificial ants to explore feasible solutions and find the optimal path. This algorithm is particularly effective for solving combinatorial optimization problems such as the TSP.

## Features

- Implementation of the ACO algorithm for the TSP.
- Adjustable parameters to control the behavior of the algorithm.
- Flexible distance matrix to define custom TSP instances.
- Outputs the shortest path and its distance.

## Installation

This project requires Python and the NumPy library. You can install NumPy using pip:

```bash
pip install numpy
```

## Usage

To use this project, you need to define the distances between cities in a matrix and set the parameters for the ACO algorithm. You can then run the algorithm to find the shortest path.

### Parameters

- `distances`: A 2D numpy array representing the distances between cities (adjacency matrix).
- `n_ants`: The number of ants in the colony.
- `n_iterations`: The number of iterations the algorithm will run.
- `alpha`: The relative importance of the pheromone trail.
- `beta`: The relative importance of the heuristic information (inverse of distance).
- `rho`: The rate of pheromone evaporation.
- `Q`: The pheromone deposit factor.
- `part`: The starting city (index).

### Example

Here's an example of how to use the ACO algorithm for TSP:

```python
import numpy as np

# Define the distances between the cities (adjacency matrix)
distances = np.array([
    [np.inf, 2, 3, 4, 5, 6, 7],
    [2, np.inf, 1, 3, 4, 5, 6],
    [3, 1, np.inf, 2, 3, 4, 5],
    [4, 3, 2, np.inf, 1, 2, 3],
    [5, 4, 3, 1, np.inf, 1, 2],
    [6, 5, 4, 2, 1, np.inf, 1],
    [7, 6, 5, 3, 2, 1, np.inf]
])

# Parameters
n_ants = 10
n_iterations = 100
alpha = 1
beta = 1
rho = 0.01
Q = 10

# Starting city defined by the user
part = int(input("Enter the starting city (0 to 6): "))

# Running the ACO algorithm
ant_colony = AntColony(distances, n_ants, n_iterations, alpha, beta, rho, Q, part)
shortest_path, shortest_path_distance = ant_colony.run()

# Print the shortest path and its distance
print(f"The shortest path found is: {shortest_path} with a distance of {shortest_path_distance}")
```
## Output

When you run the above script, you will be prompted to enter the starting city. The algorithm will then find the shortest path and print it along with the total distance.

## How It Works

1. **Initialization**: The algorithm initializes the pheromone levels on each edge of the graph.
2. **Path Construction**: Each ant constructs a path by moving from city to city based on a probabilistic rule that considers both the pheromone levels and the heuristic information (inverse of the distance).
3. **Pheromone Update**: After all ants have constructed their paths, the pheromone levels are updated. Pheromone evaporates over time, and new pheromone is deposited on the edges that were part of the shortest paths found by the ants.
4. **Iteration**: The process is repeated for a number of iterations or until a stopping criterion is met.

## Contributing

Contributions are welcome! If you have any improvements or bug fixes, please open an issue or submit a pull request. Here are some ways you can contribute:

- Reporting bugs and issues.
- Suggesting new features or enhancements.
- Improving documentation.
- Writing tests to ensure code quality.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
