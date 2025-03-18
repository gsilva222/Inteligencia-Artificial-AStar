class Graph:
    def __init__(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def h(self, n):
        H = {node: 1 for node in self.adjacency_list}
        return H[n]

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
                return reconst_path  # Retorna o caminho encontrado

            for (m, weight) in self.get_neighbors(n):
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
        
        return None  # Se nenhum caminho for encontrado

# Definição do grafo
adjacency_list = {
    'A': [('B', 5), ('F', 3)],
    'B': [('A', 5), ('C', 2), ('G', 3)],
    'C': [('B', 2), ('D', 6), ('H', 10)],
    'D': [('C', 6), ('E', 3)],
    'E': [('D', 3), ('F', 8), ('H', 5)],
    'F': [('A', 3), ('E', 8), ('G', 7)],
    'G': [('B', 3), ('F', 7), ('H', 2)],
    'H': [('C', 10), ('E', 5), ('G', 2)],
}

graph1 = Graph(adjacency_list)
path = graph1.a_star_algorithm('A', 'H')
print("Path found:", path)
