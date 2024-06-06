import numpy as np

class AntColony:
    def __init__(self, distances, n_ants, n_iterations, alpha, beta, rho, Q):
        self.distances = distances
        #inicializando a matriz copiada de distances, porém divido pelo numero de elementos da matriz(5), resultando no valor de feromônio
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.all_inds = range(len(distances))
        self.shortest_path = None
        self.shortest_path_distance = np.inf

    def run(self):
        for _ in range(self.n_iterations):
            all_paths = self.construct_all_paths()
            self.update_pheromone(all_paths)
            shortest_path, shortest_path_distance = min(all_paths, key=lambda x: x[1])
            if shortest_path_distance < self.shortest_path_distance:
                self.shortest_path = shortest_path
                self.shortest_path_distance = shortest_path_distance
        return self.shortest_path, self.shortest_path_distance

    def construct_all_paths(self):
        all_paths = []
        #for rodando de acordo com a quantidade de formigas desejadas
        for _ in range(self.n_ants):
            #alocando a lista dos caminhos e distâncias de cada formiga
            path = self.construct_path(0)
            #usando a lista de dos caminhos como parâmetro para calcular a distância total do caminho
            all_paths.append((path, self.path_distance(path)))
        return all_paths

    def construct_path(self, start):
        #lista com somente o ponto inicial
        path = [start]
        #criando um conjunto com o ponto inicial, para evitar que ele seja visitado novamente
        visited = set(path)
        prev = start
        #for rodando 4 vezes, pois temos 5 cidades. Path.append(move) adiciona o próximo ponto á lista, que também adiciona o ponto ao conjunto visited(faz com que ele não seja visitado novamente)
        for _ in range(len(self.distances) - 1):
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            path.append(move)
            visited.add(move)
            prev = move
        # Voltar ao ponto inicial
        path.append(start)
        return path

    def pick_move(self, pheromone, dist, visited):
        #criando uma cópia do array de feromônios
        pheromone = np.copy(pheromone)
        #zerando o valor dos pontos visitados
        pheromone[list(visited)] = 0
        #calculo da probabilidade de cada caminho a ser escolhido
        probabilities = (pheromone ** self.alpha) * ((1.0 / dist) ** self.beta)
        #normalizando as probabilidades, dividindo todos os valores pela soma deles?
        probabilities /= probabilities.sum()
        #escolhendo um caminho de acordo com as probabilidades calculadas
        move = np.random.choice(self.all_inds, p=probabilities)
        return move

    def path_distance(self, path):
        total_distance = 0
        #for rodando 5 vezes para calcular a distância total do caminho
        for i in range(len(path) - 1):
            total_distance += self.distances[path[i]][path[i + 1]]
        return total_distance

    def update_pheromone(self, all_paths):
        self.pheromone *= (1 - self.rho)
        for path, dist in all_paths:
            for move in zip(path[:-1], path[1:]):
                self.pheromone[move] += self.Q / dist

# Definindo as distâncias entre as cidades (matriz de adjacência)
distances = np.array([[np.inf, 2, 2, 5, 7],
                      [2, np.inf, 4, 8, 2],
                      [2, 4, np.inf, 1, 3],
                      [5, 8, 1, np.inf, 2],
                      [7, 2, 3, 2, np.inf]])

# Parâmetros
n_ants = 10
n_iterations = 100
alpha = 1
beta = 1
rho = 0.01
Q = 10

# Executando o algoritmo
ant_colony = AntColony(distances, n_ants, n_iterations, alpha, beta, rho, Q)
shortest_path, shortest_path_distance = ant_colony.run()
print(f'O caminho mais curto encontrado é: {shortest_path} com uma distância de {shortest_path_distance}')