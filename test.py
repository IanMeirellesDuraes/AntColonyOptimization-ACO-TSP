import numpy as np

class AntColony:
    def __init__(self, distances, n_ants, n_iterations, alpha, beta, rho, Q, part):
        self.distances = distances
        #inicializando a matriz copiada de distances, porém divido pelo numero de elementos da matriz(5), resultando no valor de feromônio
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
        #np.inf é um valor infinito, para que qualquer valor de distância seja menor que ele
        self.shortest_path_distance = np.inf

    def run(self):
        #for rodando de acordo com o número de iterações desejadas(100)
        for _ in range(self.n_iterations):
            #alocando todos os caminhos e distancias de cada formiga em all_paths
            part = self.part
            all_paths = self.construct_all_paths(part)
            #atualizando a matriz de feromônio de acordo com os caminhos e distâncias de cada formiga por iteração
            self.update_pheromone(all_paths)
            #usando a função min para encontrar a menor distância entre as tuplas de all_paths, usando key=lambda x: x[1] para especificar para a função min que o critério de comparação é o segundo elemento da tupla que no caso será sempre a distância
            shortest_path, shortest_path_distance = min(all_paths, key=lambda x: x[1])
            #verificando se a atual distância é menor que a menor distância ja armazenada, e a primeira verificação sempre será verdadeira pois a menor distância inicial é np.inf(um valor infinito)
            if shortest_path_distance < self.shortest_path_distance:
                #atualizando a menor distância e o caminho mais curto
                self.shortest_path = shortest_path
                self.shortest_path_distance = shortest_path_distance
        return self.shortest_path, self.shortest_path_distance

    def construct_all_paths(self, part):
        all_paths = []
        #for rodando de acordo com a quantidade de formigas desejadas
        for _ in range(self.n_ants):
            #alocando a lista dos caminhos e distâncias de cada formiga
            path = self.construct_path(part)
            #alocando em all_paths a o trajeto da formiga, e a distância total do trajeto com a função path_distance, usando como parametro o trajeto da formiga(path)
            all_paths.append((path, self.path_distance(path)))
        return all_paths

    def construct_path(self, start):
        #lista com somente o ponto inicial
        path = [start]
        #criando um conjunto com o ponto inicial, para evitar que ele seja visitado novamente
        visited = set(path)
        prev = start
        #for rodando 4 vezes, pois temos 5 cidades e a inicial ja está inclusa. path.append(move) adiciona o próximo ponto á lista, que também adiciona o ponto ao conjunto visited(faz com que ele não seja visitado novamente)
        for _ in range(len(self.distances) - 1):
            #leva para a função pick_move a linha da matriz de feromônios correspondente ao ponto prev, a linha da matriz de distâncias correspondente ao ponto prev e o conjunto de pontos visitados sempre atualizado de acordo com o for
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited)
            #adiciona o ponto escolhido ao caminho
            path.append(move)
            #adiciona o ponto escolhido ao conjunto de pontos visitados
            visited.add(move)
            #atualiza o ponto prev para o ponto para qual a formiga se moveu
            prev = move
        #finalizando o caminho com o ponto inicial
        path.append(start)
        return path

    def pick_move(self, pheromone, dist, visited):
        #criando uma cópia do array de feromônios, copiada da linha correspondente ao ponto prev
        pheromone = np.copy(pheromone)
        #zerando o valor de pheromone para os pontos já visitados que estiverem no set visited que foi transformado para uma lista, para que as formigas não escolham passar por um local ja visitado
        pheromone[list(visited)] = 0
        #calculo da probabilidade de cada caminho a ser escolhido baseado na influência do feromônio e da distância(alpha e beta)
        probabilities = (pheromone ** self.alpha) * ((1.0 / dist) ** self.beta)
        #normalizando as probabilidades, dividindo todos os valores pela soma deles, pois para usar um processo de seleção aleátoria é preciso que a soma de todos os valores seja igual a 1, o que é feito dividindo todos os valores pela soma deles
        probabilities /= probabilities.sum()
        #escolhendo um próximo passo de acordo com as probabilidades calculadas anteriormente. Sendo all_inds a lista de todos os pontos possíveis mas agora com a probabilidade de escolha de cada alocada em cada ponto
        move = np.random.choice(self.all_inds, p=probabilities)
        return move

    def path_distance(self, path):
        total_distance = 0
        #for roda 5 vezes pois temos 6 elementos em path, mas o último elemento é o mesmo que o primeiro
        for i in range(len(path) - 1):
            #calculando a distância total do caminho pela array distances
            total_distance += self.distances[path[i]][path[i + 1]]
        return total_distance

    def update_pheromone(self, all_paths):
        #atualizando a matriz de pheromone simulando a taxa de evaporação do mesmo, para que cada vez mais o sistema seja acertivo com a quantidade de pheromone depositado no caminho ideal
        self.pheromone *= (1 - self.rho)
        #separando o trajeto e a distância do trajeto de cada formiga
        for path, dist in all_paths:
            #move é uma tupla dupla que sempre sera um ponto inicial de um dos trajetos das formigas ate o ponto seguinte indo ate o ultimo ponto do trajeto, formando duplas, ignorando o ponto de chegada([:-1] e [1:])
            for move in zip(path[:-1], path[1:]):
                #usando a dupla de caminhos como posição na matriz pheromone e adicionando a quantidade de feromônio depositado por formiga(Q) dividido pela distância total do trajeto, para que quanto menor o trajeto mais feroômnio seja depositado
                self.pheromone[move] += self.Q / dist

#definindo as distâncias entre as cidades (matriz de adjacência)
distances = np.array([[np.inf, 2, 3, 4, 5, 6, 7],
                      [2, np.inf, 1, 3, 4, 5, 6],
                      [3, 1, np.inf, 2, 3, 4, 5],
                      [4, 3, 2, np.inf, 1, 2, 3],
                      [5, 4, 3, 1, np.inf, 1, 2],
                      [6, 5, 4, 2, 1, np.inf, 1],
                      [7, 6, 5, 3, 2, 1, np.inf]])


#PARAMETROS PRE DEFINIDOS
#número de formigas
n_ants = 10
#número de iterações
n_iterations = 100
#alpha é um parametro que controla a influência do feromônio na escolha do caminho pela formiga
alpha = 1
#beta é um parametro que controla a influência da distância na escolha do caminho pela formiga
beta = 1
#rho é a taxa de evaporação do feromônio
rho = 0.01
#Q é a quantidade de feromônio depositada por formiga
Q = 10

#part é o ponto de partida definido pelo usuário	
part = int(input("Digite o ponto de partida(0, 6): "))
#executando o objeto colocando seus parâmetros
ant_colony = AntColony(distances, n_ants, n_iterations, alpha, beta, rho, Q, part)
#rodando o algoritmo
shortest_path, shortest_path_distance = ant_colony.run()
#imprimindo o menor caminho e a distância do menor caminho
print(f"O caminho mais curto encontrado é: {shortest_path} com uma distância de {shortest_path_distance}")