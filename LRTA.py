import csv
import heapq

class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list  # Grafo carregado do CSV

    def get_neighbors(self, v):
        """Retorna os vizinhos de um nó"""
        return self.adjacency_list.get(v, [])

    def lrta_star(self, start_node, stop_node, cost_weights):
        """Executa o LRTA* com diferentes critérios"""
        H = {node: float('inf') for node in self.adjacency_list}
        H[start_node] = 0
        H[stop_node] = 0

        current = start_node
        path = [current]
        visited = set()
        g = {node: float('inf') for node in self.adjacency_list}
        g[start_node] = 0
        total_toll, total_fuel, total_distance = 0, 0, 0
        iteration_count = 0

        while current != stop_node:
            iteration_count += 1
            if iteration_count > 1000:
                return None, None, None, None

            visited.add(current)
            neighbors = self.get_neighbors(current)
            if not neighbors:
                return None, None, None, None

            priority_queue = []
            for (neighbor, costs) in neighbors:
                if neighbor in visited:
                    continue
                total_cost = sum(cost * weight for cost, weight in zip(costs, cost_weights))
                tentative_g = g[current] + total_cost
                estimated_cost = tentative_g + H[neighbor]
                heapq.heappush(priority_queue, (estimated_cost, neighbor, total_cost, tentative_g, costs))

            if not priority_queue:
                return None, None, None, None

            estimated_cost, next_node, cost_to_next, g_next, costs = heapq.heappop(priority_queue)
            H[current] = max(H[current], cost_to_next + H[next_node])
            g[next_node] = g_next

            total_toll += costs[0]
            total_fuel += costs[1]
            total_distance += costs[2]

            current = next_node
            path.append(current)

        return path, total_toll, total_fuel, total_distance


def load_graph_from_csv(filename):
    """Carrega o grafo do CSV e trata erros"""
    adjacency_list = {}
    try:
        with open(filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None)
            if not header:
                return None
            for row_number, row in enumerate(reader, start=2):
                if len(row) < 5:
                    continue
                origem, destino = row[0], row[1]
                try:
                    custos = tuple(map(float, row[2:]))
                except ValueError:
                    continue
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
    graph = Graph(adjacency_list)

    # Pedir ao utilizador as cidades de origem e destino
    start_city = input("Digite a cidade de origem: ")
    destination_city = input("Digite a cidade de destino: ")

    # Executar LRTA* para diferentes critérios
    path_cheapest, toll_cheapest, fuel_cheapest, distance_cheapest = graph.lrta_star(start_city, destination_city, cost_weights=(1, 0, 0))
    path_fastest, toll_fastest, fuel_fastest, distance_fastest = graph.lrta_star(start_city, destination_city, cost_weights=(0, 0, 1))
    path_most_economic, toll_economic, fuel_economic, distance_economic = graph.lrta_star(start_city, destination_city, cost_weights=(0, 1, 0))

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
