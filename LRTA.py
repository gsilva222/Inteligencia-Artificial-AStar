import csv
from math import inf
from collections import defaultdict, deque
import random
import heapq

class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.heuristic = {}
    
    def get_neighbors(self, node):
        return self.adjacency_list.get(node, [])
    
    def initialize_heuristic(self, goal):
        """Inicialização robusta da heurística usando BFS"""
        self.heuristic = {node: inf for node in self.adjacency_list}
        self.heuristic[goal] = 0
        
        queue = deque([goal])
        while queue:
            current = queue.popleft()
            for neighbor, costs in self.get_neighbors(current):
                if self.heuristic[neighbor] > self.heuristic[current] + costs[2]:
                    self.heuristic[neighbor] = self.heuristic[current] + costs[2]
                    queue.append(neighbor)
    
    def lrta_star(self, start, goal, exploration=0.2):
        """Implementação correta do LRTA* com fator de exploração"""
        current = start
        path = [current]
        toll = fuel = distance = 0
        visited = set()
        
        while current != goal:
            visited.add(current)
            neighbors = []
            
            for neighbor, costs in self.get_neighbors(current):
                if neighbor not in visited or neighbor == goal:
                    total_cost = costs[2] + self.heuristic.get(neighbor, 0)
                    neighbors.append((
                        total_cost,
                        random.uniform(0, exploration),  # Fator de exploração
                        neighbor,
                        costs
                    ))
            
            if not neighbors:
                break
            
            neighbors.sort()
            _, _, next_node, costs = neighbors[0]
            
            # Atualização LRTA* clássica
            self.heuristic[current] = costs[2] + self.heuristic.get(next_node, 0)
            
            path.append(next_node)
            toll += costs[0]
            fuel += costs[1]
            distance += costs[2]
            current = next_node
            
            if len(path) > 50:  # Prevenção contra loops
                break
        
        return (path, toll, fuel, distance) if current == goal else (None, None, None, None)
    
    def find_top_paths(self, start, goal, num_paths=5, max_attempts=30):
        """Versão otimizada para encontrar os melhores caminhos"""
        paths = []
        attempts = 0
        
        while len(paths) < num_paths and attempts < max_attempts:
            attempts += 1
            self.initialize_heuristic(goal)
            path, toll, fuel, dist = self.lrta_star(start, goal)
            
            if path:
                path_tuple = tuple(path)
                # Verifica se o caminho é novo e válido
                if not any(path_tuple == tuple(p[1]) for p in paths):
                    # Usa heap para manter os melhores (ordenado por distância)
                    heapq.heappush(paths, (dist, path, toll, fuel))
                    if len(paths) > num_paths:
                        heapq.heappop(paths)
        
        # Ordena por distância, portagem e combustível
        paths_sorted = sorted(paths, key=lambda x: (x[0], x[2], x[3]))
        return [(p[1], p[2], p[3], p[0]) for p in paths_sorted]

def load_graph_from_csv(filename):
    """Carrega o grafo do CSV com tratamento robusto de erros"""
    adjacency_list = defaultdict(list)
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Pula cabeçalho
            for row in reader:
                if len(row) < 5:
                    continue
                origem, destino, custo, combustivel, distancia = row
                try:
                    custos = (float(custo), float(combustivel), float(distancia))
                except ValueError:
                    continue
                adjacency_list[origem].append((destino, custos))
                adjacency_list[destino].append((origem, custos))
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado.")
        return None
    return adjacency_list

def main():
    filename = "cities_nodes_special.csv"
    graph_data = load_graph_from_csv(filename)
    
    if not graph_data:
        return
    
    graph = Graph(graph_data)
    
    print("Sistema de Planeamento de Rotas com LRTA*")
    print("Valores exatos do CSV serão usados\n")
    
    start = input("Cidade de origem: ").strip()
    end = input("Cidade de destino: ").strip()
    
    if start not in graph_data or end not in graph_data:
        print("Erro: Uma ou ambas as cidades não existem no grafo.")
        return
    
    print(f"\nCalculando os melhores caminhos de {start} para {end}...")
    
    paths = graph.find_top_paths(start, end)  # Agora usando find_top_paths
    
    if not paths:
        print("Nenhum caminho encontrado.")
        return
    
    print("\nTop melhores caminhos encontrados:")
    for i, (path, toll, fuel, dist) in enumerate(paths, 1):
        print(f"\n--- Caminho #{i} ---")
        print(" → ".join(path))
        print(f"Distância total: {dist:.2f} km")
        print(f"Portagem total: €{toll:.2f}")
        print(f"Combustível total: {fuel:.2f} litros")

if __name__ == "__main__":
    main()