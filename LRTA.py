import csv
import heapq

class Graph:
    def __init__(self, adjacency_list, cost_weights=(1, 1, 1)):
        self.adjacency_list = adjacency_list
        self.cost_weights = cost_weights  # (Peso para portagem, combustível, distância)
        self.H = {node: float('inf') for node in self.adjacency_list}  # Inicializa as heurísticas

    def get_neighbors(self, v):
        """Retorna os vizinhos de um nó"""
        return self.adjacency_list.get(v, [])

    def lrta_star(self, start_node, stop_node, max_iterations=1000):
        """Implementação do LRTA* com cálculo de custos detalhados"""
        self.H[start_node] = 0  # Inicializa a heurística do nó de partida como 0
        self.H[stop_node] = 0    # O destino tem heurística 0

        current = start_node
        path = [current]
        visited = set()
        g = {node: float('inf') for node in self.adjacency_list}  # Custo real g(n)
        g[start_node] = 0  # O custo do nó inicial é 0
        total_toll, total_fuel, total_distance = 0, 0, 0  # Inicia os custos acumulados
        iteration_count = 0  # Contador de iterações

        while current != stop_node:
            iteration_count += 1
            if iteration_count > max_iterations:
                print("Aviso: Número máximo de iterações atingido. Loop possível detectado.")
                return None

            visited.add(current)
            neighbors = self.get_neighbors(current)
            if not neighbors:
                return None

            priority_queue = []
            for (neighbor, costs) in neighbors:
                if neighbor in visited:
                    continue
                total_cost = sum(cost * weight for cost, weight in zip(costs, self.cost_weights))
                tentative_g = g[current] + total_cost
                estimated_cost = tentative_g + self.H[neighbor]
                heapq.heappush(priority_queue, (estimated_cost, neighbor, total_cost, tentative_g, costs))

            if not priority_queue:
                return None

            estimated_cost, next_node, cost_to_next, g_next, costs = heapq.heappop(priority_queue)
            self.H[current] = max(self.H[current], cost_to_next + self.H[next_node])
            g[next_node] = g_next

            # Atualizar os custos totais
            total_toll += costs[0]  # Portagem
            total_fuel += costs[1]  # Combustível
            total_distance += costs[2]  # Distância

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
                print(f"Erro: O arquivo {filename} está vazio ou sem cabeçalho.")
                return None
            for row_number, row in enumerate(reader, start=2):
                if len(row) < 5:
                    print(f"Aviso: Linha {row_number} ignorada (dados insuficientes: {row})")
                    continue
                origem, destino = row[0], row[1]
                try:
                    custos = tuple(map(float, row[2:]))  # Convertendo os custos para float
                except ValueError:
                    print(f"Aviso: Linha {row_number} contém valores inválidos e foi ignorada: {row}")
                    continue
                if origem not in adjacency_list:
                    adjacency_list[origem] = []
                if destino not in adjacency_list:
                    adjacency_list[destino] = []
                adjacency_list[origem].append((destino, custos))
                adjacency_list[destino].append((origem, custos))  # Grafo bidirecional
    except FileNotFoundError:
        print(f"Erro: O arquivo {filename} não foi encontrado.")
        return None
    except Exception as e:
        print(f"Erro inesperado ao carregar o CSV: {e}")
        return None
    return adjacency_list


# Carregar o grafo do CSV
filename = "cities_nodes_special.csv"
adjacency_list = load_graph_from_csv(filename)

if adjacency_list:
    # Definir pesos para os fatores (portagem, combustível, distância)
    graph = Graph(adjacency_list, cost_weights=(1, 2, 1))  # Dá mais peso ao combustível
    
    # Escolher pontos de partida e chegada
    start_city = "Berlin"
    destination_city = "Milan"
    
    # Rodar o LRTA* para encontrar o caminho e obter custos
    result = graph.lrta_star(start_city, destination_city)
    
    if result:
        path, total_toll, total_fuel, total_distance = result
        print("\nPath found:", path)
        print(f"Total Portagem (€): {total_toll:.2f}")
        print(f"Total Combustível (litros): {total_fuel:.2f}")
        print(f"Total Distância (km): {total_distance:.2f}")
    else:
        print("Nenhum caminho encontrado.")
