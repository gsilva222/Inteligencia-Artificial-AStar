import csv
import heapq

class Graph:
    def __init__(self, adjacency_list, heuristics, cost_weights=(1, 1, 1)):
        self.adjacency_list = adjacency_list
        self.H = heuristics  # Heurísticas fixas fornecidas
        self.cost_weights = cost_weights  # Tupla de pesos para os custos (km, litros, minutos)
    
    def get_neighbors(self, v):
        return self.adjacency_list.get(v, [])

    def a_star(self, start_node, stop_node):
        g = {node: float('inf') for node in self.adjacency_list}  # Custo do caminho g(n)
        f = {node: float('inf') for node in self.adjacency_list}  # Função f(n) = g(n) + h(n)
        g[start_node] = 0  # Inicializa o custo do nó de partida
        f[start_node] = self.H.get(start_node, 0)  # Inicializa f(n)

        open_list = []
        heapq.heappush(open_list, (f[start_node], start_node))  # Prioridade é f(n)
        came_from = {}  # Para reconstruir o caminho
        
        while open_list:
            _, current = heapq.heappop(open_list)  # Nós com menor f(n) são explorados primeiro
            
            if current == stop_node:
                return self.reconstruct_path(came_from, current)
            
            neighbors = self.get_neighbors(current)
            for neighbor, costs in neighbors:
                # Calcula g(n) como o custo acumulado até o nó vizinho
                tentative_g = g[current] + sum(cost * weight for cost, weight in zip(costs, self.cost_weights))
                
                if tentative_g < g[neighbor]:
                    came_from[neighbor] = current
                    g[neighbor] = tentative_g
                    f[neighbor] = g[neighbor] + self.H.get(neighbor, 0)  # f(n) = g(n) + h(n)
                    
                    if neighbor not in [n[1] for n in open_list]:  # Se o vizinho não está na open_list
                        heapq.heappush(open_list, (f[neighbor], neighbor))
        
        return None  # Se não encontrar um caminho

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()  # Reverte para o caminho correto
        return path

def load_graph_from_csv(filename):
    adjacency_list = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pula o cabeçalho
        for row in reader:
            origem, destino = row[0], row[1]
            custos = tuple(map(int, row[2:]))  # Converte os custos para inteiros
            
            if origem not in adjacency_list:
                adjacency_list[origem] = []
            if destino not in adjacency_list:
                adjacency_list[destino] = []
                
            adjacency_list[origem].append((destino, custos))
            adjacency_list[destino].append((origem, custos))  # Grafo bidirecional
    
    return adjacency_list

filename = "CSVinventado.csv"
adjacency_list = load_graph_from_csv(filename)

# Definindo heurísticas fixas para os nós (h(n)) - Exemplo: as heurísticas podem ser baseadas na distância ao destino
heuristics = {
    'A': 10,  # Exemplo de heurísticas (estimativa de custo até o destino)
    'B': 8,
    'C': 6,
    'D': 4,
    'E': 2,
    'F': 1,
    'G': 0,  # Destino
}

# Definindo pesos para os custos: (km, litros, minutos)
graph1 = Graph(adjacency_list, heuristics, cost_weights=(1, 1, 1))

path = graph1.a_star('A', 'G')

print(f"Path found (Considerar melhor trajeto):", path)
