import csv
from math import inf
from collections import defaultdict, deque
import heapq

class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.heuristic = {}
    
    def get_neighbors(self, node):
        return self.adjacency_list.get(node, [])
    
    def initialize_heuristic(self, goal):
        """Inicialização da heurística usando BFS"""
        self.heuristic = {node: inf for node in self.adjacency_list}
        self.heuristic[goal] = 0
        
        queue = deque([goal])
        while queue:
            current = queue.popleft()
            for neighbor, costs in self.get_neighbors(current):
                if self.heuristic[neighbor] > self.heuristic[current] + costs[2]:
                    self.heuristic[neighbor] = self.heuristic[current] + costs[2]
                    queue.append(neighbor)
    
    def a_star(self, start, goal):
        """Implementação do algoritmo A*"""
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        
        g_score = {node: inf for node in self.adjacency_list}
        g_score[start] = 0
        
        f_score = {node: inf for node in self.adjacency_list}
        f_score[start] = self.heuristic[start]
        
        toll_values = {node: 0 for node in self.adjacency_list}
        fuel_values = {node: 0 for node in self.adjacency_list}
        distance_values = {node: 0 for node in self.adjacency_list}
        
        while open_set:
            _, current = heapq.heappop(open_set)
            
            if current == goal:
                # Reconstruir o caminho
                path = []
                total_toll = toll_values[current]
                total_fuel = fuel_values[current]
                total_distance = distance_values[current]
                
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                
                return (path, total_toll, total_fuel, total_distance)
            
            for neighbor, costs in self.get_neighbors(current):
                tentative_g_score = g_score[current] + costs[2]
                
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic[neighbor]
                    toll_values[neighbor] = toll_values[current] + costs[0]
                    fuel_values[neighbor] = fuel_values[current] + costs[1]
                    distance_values[neighbor] = distance_values[current] + costs[2]
                    
                    if neighbor not in [node for (_, node) in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        return (None, None, None, None)
    
    def find_top_paths(self, start, goal, num_paths=5, max_attempts=30):
        """Versão otimizada para encontrar os melhores caminhos com A*"""
        paths = []
        attempts = 0
        
        self.initialize_heuristic(goal)
        
        while len(paths) < num_paths and attempts < max_attempts:
            attempts += 1
            path, toll, fuel, dist = self.a_star(start, goal)
            
            if path:
                path_tuple = tuple(path)
                if not any(path_tuple == tuple(p[1]) for p in paths):
                    heapq.heappush(paths, (dist, path, toll, fuel))
                    if len(paths) > num_paths:
                        heapq.heappop(paths)
        
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

# def main():
#     filename = "cities_nodes_special.csv"
#     graph_data = load_graph_from_csv(filename)
#     
#     if not graph_data:
#         return
#     
#     graph = Graph(graph_data)
#     
#     print("Sistema de Planeamento de Rotas com A*")
#     print("Valores exatos do CSV serão usados\n")
#     
#     start = input("Cidade de origem: ").strip()
#     end = input("Cidade de destino: ").strip()
#     
#     if start not in graph_data or end not in graph_data:
#         print("Erro: Uma ou ambas as cidades não existem no grafo.")
#         return
#     
#     print(f"\nCalculando os melhores caminhos de {start} para {end}...")
#     
#     paths = graph.find_top_paths(start, end)
#     
#     if not paths:
#         print("Nenhum caminho encontrado.")
#         return
#     
#     print("\nTop melhores caminhos encontrados:")
#     for i, (path, toll, fuel, dist) in enumerate(paths, 1):
#         print(f"\n--- Caminho #{i} ---")
#         print(" → ".join(path))
#         print(f"Distância total: {dist:.2f} km")
#         print(f"Portagem total: €{toll:.2f}")
#         print(f"Combustível total: {fuel:.2f} litros")
# 
# if __name__ == "__main__":
#     main()