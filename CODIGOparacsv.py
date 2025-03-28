import csv
import heapq

class Graph:
    def __init__(self, adjacency_list, heuristics):
        self.adjacency_list = adjacency_list
        self.H = heuristics  # Heurísticas fornecidas
    
    def get_neighbors(self, v):
        return self.adjacency_list.get(v, [])

    def a_star(self, start_node, stop_node, cost_weights):
        g = {node: float('inf') for node in self.adjacency_list}
        f = {node: float('inf') for node in self.adjacency_list}
        g[start_node] = 0
        f[start_node] = self.H.get(start_node, 0)

        open_list = []
        heapq.heappush(open_list, (f[start_node], start_node))
        came_from = {}
        
        while open_list:
            _, current = heapq.heappop(open_list)
            
            if current == stop_node:
                return self.reconstruct_path(came_from, current), self.calculate_path_cost(came_from, stop_node)
            
            for neighbor, costs in self.get_neighbors(current):
                tentative_g = g[current] + sum(cost * weight for cost, weight in zip(costs, cost_weights))
                
                if tentative_g < g[neighbor]:
                    came_from[neighbor] = (current, costs)
                    g[neighbor] = tentative_g
                    f[neighbor] = g[neighbor] + self.H.get(neighbor, 0)
                    heapq.heappush(open_list, (f[neighbor], neighbor))
        
        return None, None

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current][0]
            path.append(current)
        path.reverse()
        return path
    
    def calculate_path_cost(self, came_from, destination):
        total_costs = {"toll": 0, "fuel": 0, "distance": 0}
        current = destination
        while current in came_from:
            prev, costs = came_from[current]
            total_costs["toll"] += costs[0]
            total_costs["fuel"] += costs[1]
            total_costs["distance"] += costs[2]
            current = prev
        return total_costs

def load_graph_from_csv(filename):
    adjacency_list = {}
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                origem, destino = row[0], row[1]
                custos = tuple(map(float, row[2:]))
                
                if origem not in adjacency_list:
                    adjacency_list[origem] = []
                if destino not in adjacency_list:
                    adjacency_list[destino] = []
                
                adjacency_list[origem].append((destino, custos))
                adjacency_list[destino].append((origem, custos))
    except FileNotFoundError:
        return None
    return adjacency_list

# Carregar o grafo do CSV
filename = "cities_nodes_special.csv"
adjacency_list = load_graph_from_csv(filename)

if adjacency_list:
    heuristics = {node: 1 for node in adjacency_list}
    graph = Graph(adjacency_list, heuristics)
    
    # Pedir ao utilizador as cidades de origem e destino
    start_city = input("Digite a cidade de origem: ")
    destination_city = input("Digite a cidade de destino: ")

    # Executar A* para diferentes critérios
    path_cheapest, costs_cheapest = graph.a_star(start_city, destination_city, cost_weights=(1, 0, 0))
    path_fastest, costs_fastest = graph.a_star(start_city, destination_city, cost_weights=(0, 0, 1))
    path_most_economic, costs_economic = graph.a_star(start_city, destination_city, cost_weights=(0, 1, 0))

    # Exibir os resultados
    def print_result(title, path, costs):
        print(f"\n{title}:")
        if path:
            print(" -> ".join(path))
            print(f"Total Portagem (€): {costs['toll']:.2f} | Combustível (L): {costs['fuel']:.2f} | Distância (km): {costs['distance']:.2f}")
        else:
            print("Nenhum caminho encontrado.")

    print_result("Caminho mais barato (Menor custo de portagem)", path_cheapest, costs_cheapest)
    print_result("Caminho mais rápido (Menor distância)", path_fastest, costs_fastest)
    print_result("Caminho mais econômico (Menor combustível gasto)", path_most_economic, costs_economic)