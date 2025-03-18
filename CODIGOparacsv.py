import csv

class Graph:
    def __init__(self, adjacency_list, cost_weights=(1, 1, 1)):
        self.adjacency_list = adjacency_list
        self.cost_weights = cost_weights  # Pesos para cada fator: (kms, litros, minutos)
    
    def get_neighbors(self, v):
        return self.adjacency_list.get(v, [])
    
    def h(self, n):
        # Heurística fictícia (pode ser aprimorada)
        H = {node: 1 for node in self.adjacency_list}  
        return H.get(n, 1)
    
    def weighted_cost(self, costs):
        # Calcula o custo ponderado levando em conta os três fatores (kms, litros, minutos)
        return sum(c * w for c, w in zip(costs, self.cost_weights))
    
    def a_star_algorithm(self, start_node, stop_node):
        open_list = set([start_node])
        closed_list = set([])
        g = {start_node: 0}
        parents = {start_node: start_node}

        while open_list:
            n = min(open_list, key=lambda v: g[v] + self.h(v))

            if n == stop_node:
                reconst_path = []
                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]
                reconst_path.append(start_node)
                reconst_path.reverse()
                return reconst_path

            for (m, costs) in self.get_neighbors(n):
                weight = self.weighted_cost(costs)  # Calcula o custo ponderado
                
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                elif g[m] > g[n] + weight:
                    g[m] = g[n] + weight
                    parents[m] = n
                    if m in closed_list:
                        closed_list.remove(m)
                        open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)
        
        return None


def load_graph_from_csv(filename):
    adjacency_list = {}
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
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

# Aqui, você pode escolher os pesos para cada fator: (kms, litros, minutos)
# Por exemplo, se você quiser priorizar 'litros', pode usar algo como (1, 2, 1)
graph1 = Graph(adjacency_list, cost_weights=(1, 1, 1))  # Peso dos fatores
path = graph1.a_star_algorithm('A', 'G')

print(f"Path found:", path)
