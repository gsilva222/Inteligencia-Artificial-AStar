import csv
import heapq
import networkx as nx
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, adjacency_list, cost_weights=(1, 1, 1)):
        self.adjacency_list = adjacency_list
        self.cost_weights = cost_weights
        self.H = {node: float('inf') for node in self.adjacency_list}

    def get_neighbors(self, v):
        return self.adjacency_list.get(v, [])

    def lrta_star_top10(self, start_node, stop_node, max_iterations=10000):
        self.H[start_node] = 0
        self.H[stop_node] = 0

        paths_found = []
        queue = [(0, [start_node], 0, 0, 0)]  # (total_cost, path, total_toll, total_fuel, total_distance)
        iteration_count = 0

        while queue and len(paths_found) < 10 and iteration_count < max_iterations:
            iteration_count += 1
            queue.sort()
            current_cost, current_path, toll, fuel, distance = queue.pop(0)
            current = current_path[-1]

            if current == stop_node:
                paths_found.append((current_path, toll, fuel, distance))
                continue

            neighbors = self.get_neighbors(current)
            for neighbor, costs in neighbors:
                if neighbor not in current_path:  # evita ciclos
                    total_cost = sum(cost * weight for cost, weight in zip(costs, self.cost_weights))
                    new_cost = current_cost + total_cost
                    queue.append((new_cost, current_path + [neighbor],
                                  toll + costs[0], fuel + costs[1], distance + costs[2]))

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

if adjacency_list:
    graph = Graph(adjacency_list, cost_weights=(1, 2, 1))

    start_city = input("Insira a cidade inicial: ")
    while start_city not in adjacency_list:
        print("Cidade inicial não encontrada. Tente novamente.")
        start_city = input("Insira a cidade inicial: ")

    destination_city = input("Insira a cidade de destino: ")
    while destination_city not in adjacency_list:
        print("Cidade de destino não encontrada. Tente novamente.")
        destination_city = input("Insira a cidade de destino: ")

    top_10_paths = graph.lrta_star_top10(start_city, destination_city)

    mostrar_caminhos(top_10_paths)
else:
    print("Erro ao carregar o grafo.")