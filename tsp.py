import itertools
import random

class TSP:
    def __init__(self, adjacency_matrix=None):
        self.adjacency_matrix = adjacency_matrix

    def generate_adjacency_matrix(self, num_vertices, edge_probability=1.0, max_weight=100):
        # Initialize an empty adjacency matrix with zeros
        self.adjacency_matrix = [[None for _ in range(num_vertices)] for _ in range(num_vertices)]

        # Iterate over each pair of vertices to potentially add an edge
        for i in range(num_vertices):
            self.adjacency_matrix[i][i] = 0
            for j in range(i + 1, num_vertices):
                if random.random() < edge_probability:
                    weight = random.randint(1, max_weight)
                    self.adjacency_matrix[i][j] = weight
                    self.adjacency_matrix[j][i] = weight

    def print(self):
        for row in self.adjacency_matrix:
            print(" ".join(map(str, row)))

    def __total_distance_permutation(self, permutation):
        total_distance = 0
        num_cities = len(permutation)

        for i in range(num_cities - 1):
            total_distance += self.adjacency_matrix[permutation[i]][permutation[i + 1]]

        return total_distance

    def brute_force(self):
        num_cities = len(self.adjacency_matrix)
        city_indices = list(range(num_cities))

        # Generate all permutations of city indices
        permutations = itertools.permutations(city_indices)

        # Initialize variables to keep track of the minimum distance and the best permutation
        min_distance = float('inf')
        best_permutation = None

        # Check every possible permutation of cities
        for permutation in permutations:
            p = list(permutation + (permutation[0],)) # add starting vertex to end
            current_distance = self.__total_distance_permutation(p)
            if current_distance < min_distance:
                min_distance = current_distance
                best_permutation = p

        return best_permutation, min_distance

    def nearest_neighbor(self):
        num_vertices = len(self.adjacency_matrix)
        visited = [False] * num_vertices
        tour = []
        current_city = 0
        total_distance = 0

        for _ in range(num_vertices):
            tour.append(current_city)
            visited[current_city] = True
            nearest_distance = float('inf')
            nearest_city = None
            for next_city in range(num_vertices):
                if visited[next_city]:
                    continue
                if 0 < self.adjacency_matrix[current_city][next_city] < nearest_distance:
                    nearest_distance = self.adjacency_matrix[current_city][next_city]
                    nearest_city = next_city
            if nearest_city is not None:
                total_distance += nearest_distance
                current_city = nearest_city

        # Return to the starting city
        total_distance += self.adjacency_matrix[current_city][tour[0]]
        tour.append(tour[0])

        return tour, total_distance
