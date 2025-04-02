import csv
from math import inf
from collections import defaultdict, deque
import heapq

class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list
        self.km = 0
        self.heuristic = {}
        self.g_values = {}
        self.rhs_values = {}
        self.open_list = []
        self.open_list_hash = set()
    
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
    
    def calculate_key(self, node):
        """Calcula a chave de prioridade para o D*"""
        g = self.g_values.get(node, inf)
        rhs = self.rhs_values.get(node, inf)
        min_g_rhs = min(g, rhs)
        heuristic = self.heuristic.get(node, 0)
        return (min_g_rhs + heuristic, min_g_rhs)
    
    def update_vertex(self, u):
        """Atualiza um vértice no algoritmo D*"""
        if u != self.goal:
            min_rhs = inf
            for (v, costs) in self.get_neighbors(u):
                current_cost = costs[2] + self.g_values.get(v, inf)
                if current_cost < min_rhs:
                    min_rhs = current_cost
            self.rhs_values[u] = min_rhs
        
        # Verifica se o nó está na open_list_hash antes de remover
        if u in self.open_list_hash:
            self.open_list_hash.remove(u)
            # Remove da open_list
            self.open_list = [(k, n) for (k, n) in self.open_list if n != u]
            heapq.heapify(self.open_list)
        
        if self.g_values.get(u, inf) != self.rhs_values.get(u, inf):
            key = self.calculate_key(u)
            heapq.heappush(self.open_list, (key, u))
            self.open_list_hash.add(u)
    
    def compute_shortest_path(self):
        """Computa o caminho mais curto usando D*"""
        while self.open_list and (
            self.open_list[0][0] < self.calculate_key(self.start) or 
            self.rhs_values.get(self.start, inf) != self.g_values.get(self.start, inf)
        ):
            _, u = heapq.heappop(self.open_list)
            if u in self.open_list_hash:  # Verificação adicional de segurança
                self.open_list_hash.remove(u)
            
            if self.g_values.get(u, inf) > self.rhs_values.get(u, inf):
                self.g_values[u] = self.rhs_values.get(u, inf)
                for (v, _) in self.get_neighbors(u):
                    self.update_vertex(v)
            else:
                self.g_values[u] = inf
                self.update_vertex(u)
                for (v, _) in self.get_neighbors(u):
                    self.update_vertex(v)
    
    def d_star(self, start, goal):
        """Implementação do algoritmo D*"""
        self.start = start
        self.goal = goal
        self.km = 0
        
        # Inicialização
        self.g_values = {node: inf for node in self.adjacency_list}
        self.rhs_values = {node: inf for node in self.adjacency_list}
        self.rhs_values[goal] = 0
        
        self.open_list = []
        self.open_list_hash = set()
        heapq.heappush(self.open_list, (self.calculate_key(goal), goal))
        self.open_list_hash.add(goal)
        
        self.compute_shortest_path()
        
        # Reconstruir o caminho
        path = []
        current = start
        toll = fuel = distance = 0
        
        while current != goal:
            path.append(current)
            
            min_cost = inf
            next_node = None
            selected_costs = None
            
            for neighbor, costs in self.get_neighbors(current):
                if neighbor not in self.g_values:  # Verificação de segurança
                    continue
                total_cost = costs[2] + self.g_values.get(neighbor, inf)
                if total_cost < min_cost:
                    min_cost = total_cost
                    next_node = neighbor
                    selected_costs = costs
            
            if next_node is None:
                return (None, None, None, None)
            
            toll += selected_costs[0]
            fuel += selected_costs[1]
            distance += selected_costs[2]
            current = next_node
        
        path.append(goal)
        return (path, toll, fuel, distance)
    
    def find_top_paths(self, start, goal, num_paths=5, max_attempts=30):
        """Versão adaptada para encontrar os melhores caminhos com D*"""
        paths = []
        attempts = 0
        
        while len(paths) < num_paths and attempts < max_attempts:
            attempts += 1
            path, toll, fuel, dist = self.d_star(start, goal)
            
            if path:
                path_tuple = tuple(path)
                if not any(path_tuple == tuple(existing_path[0]) for existing_path in paths):
                    heapq.heappush(paths, (path, toll, fuel, dist))
                    if len(paths) > num_paths:
                        heapq.heappop(paths)
        
        # Ordena por distância, portagem e combustível
        paths_sorted = sorted(paths, key=lambda x: (x[3], x[1], x[2]))
        return paths_sorted

def load_graph_from_csv(filename):
    """Carrega o grafo do CSV com tratamento robusto de erros"""
    adjacency_list = defaultdict(list)
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
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


#def main():
#    filename = "cities_nodes_special.csv"
#    graph_data = load_graph_from_csv(filename)
    
#    if not graph_data:
#        return
    
#    graph = Graph(graph_data)
    
#    print("Sistema de Planeamento de Rotas com Dynamic A* (D*)")
#    print("Valores exatos do CSV serão usados\n")
    
#    start = input("Cidade de origem: ").strip()
#    end = input("Cidade de destino: ").strip()
    
#    if start not in graph_data or end not in graph_data:
#        print("Erro: Uma ou ambas as cidades não existem no grafo.")
#        return
    
#    print(f"\nCalculando os melhores caminhos de {start} para {end}...")
    
#    paths = graph.find_top_paths(start, end)
    
#    if not paths:
#        print("Nenhum caminho encontrado.")
#        return
    
#    print("\nTop melhores caminhos encontrados:")
#    for i, (path, toll, fuel, dist) in enumerate(paths, 1):
#        print(f"\n--- Caminho #{i} ---")
#        print(" → ".join(path))
#        print(f"Distância total: {dist:.2f} km")
#        print(f"Portagem total: €{toll:.2f}")
#        print(f"Combustível total: {fuel:.2f} litros")

#if __name__ == "__main__":
#    main()
