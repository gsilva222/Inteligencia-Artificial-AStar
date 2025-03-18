import csv
import heapq

class Graph:
    def __init__(self, adjacency_list, heuristics):
        self.adjacency_list = adjacency_list
        self.H = heuristics  # Heurísticas fixas fornecidas
    
    def get_neighbors(self, v):
        return self.adjacency_list.get(v, [])

    def a_star(self, start_node, stop_node, cost_weights):
        """Executa o A* com diferentes pesos para cada critério."""
        g = {node: float('inf') for node in self.adjacency_list}  # Custo acumulado g(n)
        f = {node: float('inf') for node in self.adjacency_list}  # f(n) = g(n) + h(n)
        g[start_node] = 0  # Inicializa o custo do nó de partida
        f[start_node] = self.H.get(start_node, 0)  # Inicializa f(n)

        open_list = []
        heapq.heappush(open_list, (f[start_node], start_node))  # Prioridade é f(n)
        came_from = {}  # Para reconstruir o caminho
        total_toll, total_fuel, total_distance = 0, 0, 0  # Acumuladores de custos

        while open_list:
            _, current = heapq.heappop(open_list)  # Nós com menor f(n) são explorados primeiro
            
            if current == stop_node:
                return self.reconstruct_path(came_from, current), total_toll, total_fuel, total_distance
            
            neighbors = self.get_neighbors(current)
            for neighbor, costs in neighbors:
                # Calcula g(n) como o custo acumulado até o nó vizinho
                tentative_g = g[current] + sum(cost * weight for cost, weight in zip(costs, cost_weights))
                
                if tentative_g < g[neighbor]:
                    came_from[neighbor] = current
                    g[neighbor] = tentative_g
                    f[neighbor] = g[neighbor] + self.H.get(neighbor, 0)  # f(n) = g(n) + h(n)

                    if neighbor not in [n[1] for n in open_list]:  # Se o vizinho não está na open_list
                        heapq.heappush(open_list, (f[neighbor], neighbor))
                    
                    # Atualiza os custos acumulados
                    total_toll += costs[0]  # Portagem
                    total_fuel += costs[1]  # Combustível
                    total_distance += costs[2]  # Distância
        
        return None, None, None, None  # Se não encontrar um caminho

    def reconstruct_path(self, came_from, current):
        """Reconstrói o caminho a partir do dicionário de pais."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()  # Reverte para o caminho correto
        return path

def load_graph_from_csv(filename):
    """Carrega o grafo do CSV e trata erros."""
    adjacency_list = {}
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Pula o cabeçalho
            for row in reader:
                origem, destino = row[0], row[1]
                custos = tuple(map(float, row[2:]))  # Converte os custos para float
                
                if origem not in adjacency_list:
                    adjacency_list[origem] = []
                if destino not in adjacency_list:
                    adjacency_list[destino] = []
                    
                adjacency_list[origem].append((destino, custos))
                adjacency_list[destino].append((origem, custos))  # Grafo bidirecional
    except FileNotFoundError:
        return None
    return adjacency_list

# Carregar o grafo do CSV
filename = "cities_nodes_special.csv"
adjacency_list = load_graph_from_csv(filename)

if adjacency_list:
    # Definição de heurísticas arbitrárias (poderia ser baseado na distância ao destino)
    heuristics = {node: 1 for node in adjacency_list}  
    graph = Graph(adjacency_list, heuristics)

    # Escolher pontos de partida e chegada
    start_city = "Stockholm"
    destination_city = "Seville"

    # Executar A* para diferentes critérios
    path_cheapest, toll_cheapest, fuel_cheapest, distance_cheapest = graph.a_star(start_city, destination_city, cost_weights=(1, 0, 0))
    path_fastest, toll_fastest, fuel_fastest, distance_fastest = graph.a_star(start_city, destination_city, cost_weights=(0, 0, 1))
    path_most_economic, toll_economic, fuel_economic, distance_economic = graph.a_star(start_city, destination_city, cost_weights=(0, 1, 0))

    # Exibir os resultados
    print("\nCaminho mais barato (Menor custo de portagem):")
    if path_cheapest:
        print(" -> ".join(path_cheapest))
        print(f"Total Portagem (€): {toll_cheapest:.2f} | Combustível (L): {fuel_cheapest:.2f} | Distância (km): {distance_cheapest:.2f}")
    else:
        print("Nenhum caminho encontrado.")

    print("\nCaminho mais rápido (Menor distância):")
    if path_fastest:
        print(" -> ".join(path_fastest))
        print(f"Total Portagem (€): {toll_fastest:.2f} | Combustível (L): {fuel_fastest:.2f} | Distância (km): {distance_fastest:.2f}")
    else:
        print("Nenhum caminho encontrado.")

    print("\nCaminho mais econômico (Menor combustível gasto):")
    if path_most_economic:
        print(" -> ".join(path_most_economic))
        print(f"Total Portagem (€): {toll_economic:.2f} | Combustível (L): {fuel_economic:.2f} | Distância (km): {distance_economic:.2f}")
    else:
        print("Nenhum caminho encontrado.")
