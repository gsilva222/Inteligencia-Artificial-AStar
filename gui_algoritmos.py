import tkinter as tk
from tkinter import ttk, messagebox
from CODIGOparacsv import Graph, load_graph_from_csv
from LRTA import Graph as LRTA_Graph, load_graph_from_csv as load_graph_lrta
from DinamicAStar import Graph as DStar_Graph, load_graph_from_csv as load_graph_dstar
import networkx as nx
import matplotlib.pyplot as plt

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Planeador de Rotas")

        # Carregar cidades
        self.graph_data = load_graph_from_csv("cities_nodes_special.csv")
        if not self.graph_data:
            messagebox.showerror("Erro", "Erro ao carregar o ficheiro CSV.")
            self.root.destroy()
            return

        self.cities = sorted(self.graph_data.keys())

        # Algoritmo
        ttk.Label(root, text="Escolher algoritmo:").grid(row=0, column=0, padx=10, pady=10)
        self.algorithm = ttk.Combobox(root, values=["A*", "LRTA*", "D*"], state="readonly")
        self.algorithm.grid(row=0, column=1)
        self.algorithm.set("A*")

        # Origem
        ttk.Label(root, text="Origem:").grid(row=1, column=0, padx=10, pady=10)
        self.start_combo = ttk.Combobox(root, values=self.cities, state="readonly")
        self.start_combo.grid(row=1, column=1)
        self.start_combo.set(self.cities[0])

        # Destino
        ttk.Label(root, text="Destino:").grid(row=2, column=0, padx=10, pady=10)
        self.end_combo = ttk.Combobox(root, values=self.cities, state="readonly")
        self.end_combo.grid(row=2, column=1)
        self.end_combo.set(self.cities[1])

        # Botão
        self.run_button = ttk.Button(root, text="Calcular Caminho", command=self.run_algorithm)
        self.run_button.grid(row=3, columnspan=2, pady=20)

        # Resultados
        self.result_box = tk.Text(root, width=60, height=20)
        self.result_box.grid(row=4, columnspan=2)

    def run_algorithm(self):
        alg = self.algorithm.get()
        start = self.start_combo.get()
        end = self.end_combo.get()

        self.result_box.delete("1.0", tk.END)

        if not start or not end:
            messagebox.showerror("Erro", "Por favor preenche origem e destino.")
            return

        if start not in self.graph_data or end not in self.graph_data:
            self.result_box.insert(tk.END, "Erro: Uma ou ambas as cidades não existem.\n")
            return

        # Escolher o algoritmo
        if alg == "A*":
            graph = Graph(self.graph_data)
        elif alg == "LRTA*":
            graph = LRTA_Graph(self.graph_data)
        elif alg == "D*":
            graph = DStar_Graph(self.graph_data)
        else:
            self.result_box.insert(tk.END, f"Algoritmo {alg} ainda não está implementado.\n")
            return

        paths = graph.find_top_paths(start, end)

        if not paths:
            self.result_box.insert(tk.END, "Nenhum caminho encontrado.\n")
            return

        # Mostrar os caminhos encontrados
        for i, (path, toll, fuel, dist) in enumerate(paths, 1):
            self.result_box.insert(tk.END, f"\n--- Caminho #{i} ---\n")
            self.result_box.insert(tk.END, " → ".join(path) + "\n")
            self.result_box.insert(tk.END, f"Distância: {dist:.2f} km\n")
            self.result_box.insert(tk.END, f"Portagens: €{toll:.2f}\n")
            self.result_box.insert(tk.END, f"Combustível: {fuel:.2f} litros\n")
            self.result_box.insert(tk.END, "-" * 30 + "\n")

        # Desenhar o melhor caminho
        best_path = paths[0][0]
        self.draw_path_on_map(self.graph_data, best_path)

    def draw_path_on_map(self, graph_data, path):
        G = nx.Graph()

        # Adicionar todos os nós (para contexto visual)
        for cidade, vizinhos in graph_data.items():
            G.add_node(cidade)
            for vizinho, custos in vizinhos:
                G.add_edge(cidade, vizinho, weight=custos[2])

        pos = nx.spring_layout(G, seed=42)

        # Cores e estilos
        edge_colors = []
        for u, v in G.edges():
            if u in path and v in path and abs(path.index(u) - path.index(v)) == 1:
                edge_colors.append("blue")
            else:
                edge_colors.append("gray")

        node_colors = ["orange" if n in path else "lightgray" for n in G.nodes]

        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=700,
                node_color=node_colors, edge_color=edge_colors, width=2, font_size=8)

        plt.title("Mapa com o Caminho Calculado")
        plt.axis("off")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()