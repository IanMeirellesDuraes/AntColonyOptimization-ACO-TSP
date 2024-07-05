import numpy as np

class AntColony:
    def __init__(self, distances, n_ants, n_iterations, alpha, beta, rho, Q, part):
        self.distances = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.part = part
        self.all_inds = range(len(distances))
        self.shortest_path = None
        self.shortest_path_distance = np.inf

    def run(self):
        for _ in range(self.n_iterations):
            part = self.part
            all_paths = self.construct_all_paths(part)
            self.update_pheromone(all_paths)
            shortest_path, shortest_path_distance = min(all_paths, key=lambda x: x[1])
            if shortest_path_distance < self.shortest_path_distance:
                self.shortest_path = shortest_path
                self.shortest_path_distance = shortest_path_distance
        return self.shortest_path, self.shortest_path_distance

    def construct_all_paths(self, part):
        all_paths = []
        for _ in range(self.n_ants):
            path = self.construct_path(part)
            all_paths.append((path, self.path_distance(path)))
        return all_paths

    def construct_path(self, start):
        path = [start]
        visited = set(path)
        prev = start
        for _ in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append(move)
            visited.add(move)
            prev = move
        path.append(start)
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone)
        pheromone[list(visited)] = 0
        probabilities = (pheromone ** self.alpha) * ((1.0 / dist) ** self.beta)
        probabilities /= probabilities.sum()
        move = np.random.choice(self.all_inds, p=probabilities)
        return move

    def path_distance(self, path):
        total_distance = 0
        for i in range(len(path) - 1):
            total_distance += self.distances[path[i]][path[i + 1]]
        return total_distance

    def update_pheromone(self, all_paths):
        self.pheromone *= (1 - self.rho)
        for path, dist in all_paths:
            for move in zip(path[:-1], path[1:]):
                self.pheromone[move] += self.Q / dist

# Definindo as distâncias entre as cidades (matriz de adjacência) 7x7
distances = np.array([[np.inf, 2, 3, 4, 5, 6, 7],
                      [2, np.inf, 1, 3, 4, 5, 6],
                      [3, 1, np.inf, 2, 3, 4, 5],
                      [4, 3, 2, np.inf, 1, 2, 3],
                      [5, 4, 3, 1, np.inf, 1, 2],
                      [6, 5, 4, 2, 1, np.inf, 1],
                      [7, 6, 5, 3, 2, 1, np.inf]])

# Parâmetros
n_ants = 10
n_iterations = 100
alpha = 1
beta = 1
rho = 0.01
Q = 10

# Ponto de partida definido pelo usuário
part = int(input("Digite o ponto de partida (0 a 6): "))

# Executando o objeto colocando seus parâmetros
ant_colony = AntColony(distances, n_ants, n_iterations, alpha, beta, rho, Q, part)
shortest_path, shortest_path_distance = ant_colony.run()

# Imprimindo o menor caminho e a distância do menor caminho
print(f"O caminho mais curto encontrado é: {shortest_path} com uma distância de {shortest_path_distance}")
