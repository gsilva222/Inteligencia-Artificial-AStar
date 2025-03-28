import csv
import heapq

class Graph:
    def __init__(self, adjacency_list, heuristics, cost_weights=(1, 1, 1)):
        self.adjacency_list = adjacency_list
        self.H = heuristics
        self.cost_weights = cost_weights

    def get_neighbors(self, v):
        return self.adjacency_list.get(v, [])

    def dynamic_a_star_top10(self, start_node, stop_node):
        paths_found = []
        open_list = [(self.H[start_node], 0, [start_node], 0, 0, 0)]  # (f, g, path, total_toll, total_fuel, total_distance)

        while open_list and len(paths_found) < 10:
            open_list.sort()
            f, g, path, total_toll, total_fuel, total_distance = open_list.pop(0)
            current = path[-1]

            if current == stop_node:
                paths_found.append((path, total_toll, total_fuel, total_distance))
                continue

            for neighbor, costs in self.get_neighbors(current):
                if neighbor not in path:
                    new_g = g + sum(c * w for c, w in zip(costs, self.cost_weights))
                    new_f = new_g + self.H.get(neighbor, 0)
                    open_list.append((new_f, new_g, path + [neighbor],
                                      total_toll + costs[0], total_fuel + costs[1], total_distance + costs[2]))

        return paths_found


def load_graph_from_csv(filename):
    adjacency_list = {}
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

    return adjacency_list


def mostrar_caminhos(paths):
    for idx, (path, toll, fuel, distance) in enumerate(paths, start=1):
        print(f"\nTop {idx} caminho encontrado:")
        print(f"  Caminho: {' -> '.join(path)}")
        print(f"  Total Portagem (€): {toll:.2f}")
        print(f"  Total Combustível (litros): {fuel:.2f}")
        print(f"  Total Distância (km): {distance:.2f}")


filename = "cities_nodes_special.csv"
adjacency_list = load_graph_from_csv(filename)

heuristics = {node: 1 for node in adjacency_list}

if adjacency_list:
    graph = Graph(adjacency_list, heuristics, cost_weights=(1, 2, 1))

    start_city = input("Insira a cidade inicial: ")
    while start_city not in adjacency_list:
        print("Cidade inicial não encontrada. Tente novamente.")
        start_city = input("Insira a cidade inicial: ")

    destination_city = input("Insira a cidade de destino: ")
    while destination_city not in adjacency_list:
        print("Cidade de destino não encontrada. Tente novamente.")
        destination_city = input("Insira a cidade de destino: ")

    top_10_paths = graph.dynamic_a_star_top10(start_city, destination_city)

    mostrar_caminhos(top_10_paths)
else:
    print("Erro ao carregar o grafo.")