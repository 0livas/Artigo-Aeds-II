from Methods import tratar_csv_1, tratar_csv_2
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import time  # Para medir o tempo de execução

def RotinaPrincipal():
    start_time = time.time()
    
    df = pd.read_csv("framingham_heart_study_tratado_filtrado.csv", sep=";")
    df.reset_index(inplace=True)  # Garante que os índices correspondam às linhas reais

    continuous_columns = ['age', 'totChol', 'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose', 'cigsPerDay']
    binary_columns = ['male', 'currentSmoker', 'BPMeds', 'prevalentStroke', 'prevalentHyp', 'diabetes', 'TenYearCHD']

    df_filtered = df[df['TenYearCHD'] == 1].copy()
    print(f"Dados filtrados: {df_filtered.shape[0]} linhas restantes.")
    
    df_filtered.dropna(inplace=True)
    print(f"Dados após remoção de NaNs: {df_filtered.shape[0]} linhas restantes.")
    
    filter_time = time.time()
    print(f"Tempo para carregar e filtrar os dados: {filter_time - start_time:.2f} segundos.")

    # Normalização das colunas contínuas
    scaler = MinMaxScaler()
    df_filtered[continuous_columns] = scaler.fit_transform(df_filtered[continuous_columns]).astype(float)

    # Criando o grafo
    G = nx.Graph()
    
    # Adicionando nós
    for i, person in df_filtered.iterrows():
        G.add_node(person['index'])  # Usa o índice real

    # Calculando similaridade e adicionando arestas
    for i, person1 in df_filtered.iterrows():
        for j, person2 in df_filtered.iterrows():
            if i < j:  # Evita comparações duplicadas e auto-laços
                similarity = 1 - (np.sum(np.abs(person1[continuous_columns] - person2[continuous_columns])) + 
                                  np.sum(np.abs(person1[binary_columns] - person2[binary_columns]))) / len(person1)
                if similarity >= 0.8:
                    G.add_edge(person1['index'], person2['index'], weight=similarity)  # Adiciona peso da similaridade

    # Identificando hubs e nós com menor grau
    hub_graph = max(G.degree, key=lambda x: x[1])[0]
    min_graph = min(G.degree, key=lambda x: x[1])[0]

    print(f"No grafo original, o hub é o nó {hub_graph + 2} com grau {G.degree[hub_graph]}")
    print(f"No grafo original, o nó com menor grau é {min_graph + 2} com grau {G.degree[min_graph]}")
    
    
    MST = nx.minimum_spanning_tree(G, weight='weight') #Obriga o nó 
    MST_directed = nx.bfs_tree(MST, source=hub_graph)  #raiz a
    MST = MST_directed                                 #ser o hub
    
    #MST = nx.minimum_spanning_tree(G, weight='weight') #Raiz aleatória

    # Recalcular o novo hub da MST (agora é garantidamente o mesmo hub do grafo original)
    hub_mst = hub_graph  # O hub original já é a raiz da MST
    min_mst = min(MST.degree, key=lambda x: x[1])[0]
    print(f"\nNa MST, o hub é o nó {hub_mst + 2} com grau {MST.degree[hub_mst]}")
    
    def plot_graph(G, hub, min_node, title, show_labels=True):
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        if show_labels:
            nx.draw(G, pos, with_labels=True, labels={n: n for n in G.nodes()}, node_size=20, edge_color="skyblue")
        else:
            nx.draw(G, pos, with_labels=False, node_size=20, edge_color="skyblue")
        nx.draw_networkx_nodes(G, pos, nodelist=[hub], node_color="yellow", node_size=100)
        nx.draw_networkx_nodes(G, pos, nodelist=[min_node], node_color="red", node_size=100)
        plt.title(title)
        plt.show()
    
    plot_graph(G, hub_graph, min_graph, "Grafo Original com Hub e Menor Grau Destacados", show_labels=True)
    plot_graph(G, hub_graph, min_graph, "Grafo Original sem Rótulos", show_labels=False)
    plot_graph(MST, hub_mst, min_mst, "MST com Hub e Menor Grau Destacados", show_labels=True)
    plot_graph(MST, hub_mst, min_mst, "MST sem Rótulos", show_labels=False)

#--------------#
#     MAIN     #
#--------------#

RotinaPrincipal()
