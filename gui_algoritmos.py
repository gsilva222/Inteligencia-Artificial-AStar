import tkinter as tk
from tkinter import ttk, messagebox
from CODIGOparacsv import Graph, load_graph_from_csv
from LRTA import Graph as LRTA_Graph, load_graph_from_csv as load_graph_lrta
from DinamicAStar import Graph as DStar_Graph, load_graph_from_csv as load_graph_dstar
import heapq

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Planeador de Rotas")

        # Algoritmo
        ttk.Label(root, text="Escolher algoritmo:").grid(row=0, column=0, padx=10, pady=10)
        self.algorithm = ttk.Combobox(root, values=["A*", "LRTA*", "D*"])
        self.algorithm.grid(row=0, column=1)
        self.algorithm.set("A*")

        # Cidade de origem
        ttk.Label(root, text="Origem:").grid(row=1, column=0, padx=10, pady=10)
        self.start_entry = ttk.Entry(root)
        self.start_entry.grid(row=1, column=1)

        # Cidade de destino
        ttk.Label(root, text="Destino:").grid(row=2, column=0, padx=10, pady=10)
        self.end_entry = ttk.Entry(root)
        self.end_entry.grid(row=2, column=1)

        # Botão
        self.run_button = ttk.Button(root, text="Calcular Caminho", command=self.run_algorithm)
        self.run_button.grid(row=3, columnspan=2, pady=20)

        # Resultados
        self.result_box = tk.Text(root, width=60, height=20)
        self.result_box.grid(row=4, columnspan=2)

    def run_algorithm(self):
        alg = self.algorithm.get()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()

        # Limpar output
        self.result_box.delete("1.0", tk.END)

        if not start or not end:
            messagebox.showerror("Erro", "Por favor preenche origem e destino.")
            return

        # Carrega grafo do CSV
        graph_data = load_graph_from_csv("cities_nodes_special.csv")
        if not graph_data:
            self.result_box.insert(tk.END, "Erro ao carregar o grafo.\n")
            return

        graph = Graph(graph_data)

        if start not in graph_data or end not in graph_data:
            self.result_box.insert(tk.END, "Erro: Uma ou ambas as cidades não existem.\n")
            return

        if alg == "A*":
            paths = graph.find_top_paths(start, end)

        elif alg == "LRTA*":
            graph = LRTA_Graph(graph_data)
            paths = graph.find_top_paths(start, end)

        elif alg == "D*":
            graph = DStar_Graph(graph_data)
            paths = graph.find_top_paths(start, end)

        else:
            self.result_box.insert(tk.END, f"Algoritmo {alg} ainda não está implementado.\n")
            return



        if not paths:
            self.result_box.insert(tk.END, "Nenhum caminho encontrado.\n")
            return

        for i, (path, toll, fuel, dist) in enumerate(paths, 1):
            self.result_box.insert(tk.END, f"\n--- Caminho #{i} ---\n")
            self.result_box.insert(tk.END, " → ".join(path) + "\n")
            self.result_box.insert(tk.END, f"Distância: {dist:.2f} km\n")
            self.result_box.insert(tk.END, f"Portagens: €{toll:.2f}\n")
            self.result_box.insert(tk.END, f"Combustível: {fuel:.2f} litros\n")
            self.result_box.insert(tk.END, "-" * 30 + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

