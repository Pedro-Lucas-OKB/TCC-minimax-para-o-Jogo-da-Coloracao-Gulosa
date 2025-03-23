import networkx as nx
import matplotlib.pyplot as plt

def mostrar_grafo(G, phi):
    num_de_clausulas = len(phi["clausulas"])
    dist_entre_vert = 100
    total_de_literais = 0
    for i in range(num_de_clausulas):
        total_de_literais = total_de_literais + len(phi["clausulas"][i])

    pos = {}

    # Camada superior
    pos["V"] = ( ((total_de_literais-1)*dist_entre_vert)/2, 770)
    

    # Camada intermediária (C1, C2, C3, ...)
    px = -1*dist_entre_vert
    px_ci  = 0
    for i in range(num_de_clausulas):
        px = px + dist_entre_vert
        tam_ci = len(phi["clausulas"][i])
        if i == 0:
            px_ci = ((tam_ci-1)*dist_entre_vert)/2
        else:
            tam_ci_1 = len(phi["clausulas"][i-1])
            px_ci = px_ci + ((tam_ci + tam_ci_1)/2 + 1)*dist_entre_vert
        pos[f"C{i+1}"] = (px_ci , 650)
    # Variáveis associadas aos cláusulas
        for x in range(len(phi["clausulas"][i])):
            pos[f"C{i+1}L{x+1}{phi["clausulas"][i][x]}"] = (px, 550)
            px = px + dist_entre_vert
    

    # Camada das variáveis principais
    v = len(phi["variaveis"])
    espaco = ((total_de_literais - 1)*dist_entre_vert)/(v+1)
    j = espaco
    for i in range(v):
        pos[f"X{i+1}"]  = (j, 350)
        pos[f"X{i+1}'"] = (j, 300)
        j = j + espaco
    
    cores_nos = nx.get_node_attributes(G, 'color')
    lista_cores = [cores_nos[vertice] for vertice in G.nodes]

    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color=lista_cores, node_size=1200, font_size=9)
    plt.show()