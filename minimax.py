""" from copy import deepcopy
from sympy import true, false
from sympy.logic.boolalg import to_cnf
from sympy.abc import xi """
from itertools import count
from math import e
from turtle import color
from matplotlib.pylab import f
import networkx as nx
import matplotlib.pyplot as plt
from numpy import var

jogadas = {
    'Alice': 0,
    'Bob': 1
}

colors = {
    1: 'red',
    2: 'green',
    3: 'blue',
    4: 'yellow',
    0: 'gray',
}

pos_cnf = {
    'clausulas': [
        #["X1", "X2", "X3", "X4", "X5", "X6"],  # Cláusula 1
        #["X1", "X1\'", "X2", "X3", "X4", "X5"],  # Cláusula 2
        #["X2", "X3", "X4", "X5", "X6", "X6\'"],  # Cláusula 3
        #["X1", "X2", "X3", "X3", "X5", "X6"],  # Cláusula 4
        #["X1", "X2", "X2", "X4", "X5", "X6"],  # Cláusula 5
        #["X1", "X3", "X3", "X4", "X5", "X6"],  # Cláusula 6
        #"X1_1", "X1_2", "X1_3", "X2_1", "X2_2", "X2_3"],  # Cláusula 1
        #["X2_1", "X2_2", "X2_3", "X3_1", "X3_2", "X3_3"],  # Cláusula 2
        #["X3_1", "X3_2", "X3_3", "X4_1", "X4_2", "X4_3"],  # Cláusula 3
        #["X4_1", "X4_2", "X4_3", "X1_1", "X1_2", "X1_3"],  # Cláusula 4
        ["X1", "X2_1", "X2_2", "X2_3", "X2_4", "X2_5"],  # Cláusula 4
        ["X1_1", "X1_2", "X2_1", "X2_2", "X2_3", "X2_4"],  # Cláusula 4
    ],
    'variaveis': ['X1', 'X2'],
    'valoracao': {
        'X1': None,
        'X2': None,
        #'X3': None,
        #'X4': None,
        #'X5': None,
        #'X6': None,
    }
}

pos_cnf_jogo_valoracao = {
    'clausulas': [
        #["X1", "X2", "X3", "X4", "X5", "X6"],  # Cláusula 1
        #["X1", "X1\'", "X2", "X3", "X4", "X5"],  # Cláusula 2
        #["X2", "X3", "X4", "X5", "X6", "X6\'"],  # Cláusula 3
        #["X1", "X2", "X3", "X3", "X5", "X6"],  # Cláusula 4
        #["X1", "X2", "X2", "X4", "X5", "X6"],  # Cláusula 5
        #["X1", "X3", "X3", "X4", "X5", "X6"],  # Cláusula 6
        #"X1_1", "X1_2", "X1_3", "X2_1", "X2_2", "X2_3"],  # Cláusula 1
        #["X2_1", "X2_2", "X2_3", "X3_1", "X3_2", "X3_3"],  # Cláusula 2
        #["X3_1", "X3_2", "X3_3", "X4_1", "X4_2", "X4_3"],  # Cláusula 3
        #["X4_1", "X4_2", "X4_3", "X1_1", "X1_2", "X1_3"],  # Cláusula 4
        ["X1", "X2_1", "X2_2", "X2_3", "X2_4", "X2_5"],  # Cláusula 4
        ["X1_1", "X1_2", "X2_1", "X2_2", "X2_3", "X2_4"],  # Cláusula 4
    ],
    'variaveis': ['X1', 'X2'],
    'valoracao': {
        'X1': None,
        'X2': None,
        #'X3': None,
        #'X4': None,
        #'X5': None,
        #'X6': None,
    }
}

def reducao(formula):
    G = nx.Graph()
    G.add_node('V')
    
    count_clausula = 1
    for clausula in formula["clausulas"]:
        G.add_node(f"C{count_clausula}")
        G.add_edge('V', f"C{count_clausula}")
        
        criar_ciclos_clausula(G, clausula, count_clausula)
            
        count_clausula += 1

    criar_vertices_variavel(formula, G)  
        
    nx.set_node_attributes(G, colors[0], 'color')

    #pintar_variaveis(G, formula)

    """ G.add_edge("X1", "auxred")
    G.add_edge("X2", "auxred2")

    G.nodes["auxred"]["color"] = colors[2]
    G.nodes["auxred2"]["color"] = colors[2] """

    return G

def pintar_variaveis(G, formula):
    for vertice in G.nodes:
        if vertice in formula["variaveis"]:
            if formula["valoracao"][vertice] == False:
                G.nodes[vertice]["color"] = colors[1]
            else:
                G.nodes[f"{vertice}\'"]["color"] = colors[1]

def criar_vertices_variavel(formula, G):
    for variavel in formula["variaveis"]:
        G.add_node(variavel)
        G.add_node(f"{variavel}\'")

        G.add_edge(variavel, f"{variavel}\'")
    
        for vertice in G.nodes:
            if variavel in vertice and variavel != vertice:
                G.add_edge(variavel, vertice)
                #print(variavel, vertice)
        
def criar_ciclos_clausula(G, clausula, count_clausula):
    for i in range(len(clausula)):
        variavel = f"C{count_clausula}{clausula[i]}"
        G.add_node(variavel)
            
        if i == 0 or i == len(clausula) - 1:
            G.add_edge(f"C{count_clausula}", variavel)
            
        else:            
            G.add_edge(f"C{count_clausula}{clausula[i - 1]}", variavel)
            if f"C{count_clausula}{clausula[i - 1]}" == variavel:
                print(clausula[i - 1], variavel)

            G.add_edge(f"C{count_clausula}{clausula[i + 1]}", variavel)
            if f"C{count_clausula}{clausula[i + 1]}" == variavel:
                print(clausula[i + 1], variavel)
    
def show_graph(G):
    print(G.nodes)
    print(G.edges)
    pos = nx.spectral_layout(G)

    pos = {
        1: (0, 6),
        2: (0, 4),
        3: (-6, 2),
        4: (-4, 2),
        5: (-2, 2),
        6: (2, 2),
        7: (4, 2),
        8: (6, 2),
        9: (-6, 0),
        10: (-4, 0),
        11: (-2, 0),
        12: (2, 0),
        13: (4, 0),
        14: (6, 0),
        15: (-6, -2),
        16: (-4, -2),
        17: (-2, -2),
        18: (2, -2),
        19: (4, -2),
        20: (6, -2),
    }
    
    pos = {}
    count = 0
    pos_x = -6
    pos_y = 2
    for node in G.nodes:
        if node == 'V':
            pos[node] = (0, 6)
        elif node == 'C':
            pos[node] = (0, 4)
        else:
            
            if 'none' in node:
                pos_y = -2
                pos[node] = (pos_x, pos_y)
                pos_x += 2

            elif 'F' in node or 'T' in node:
                pos_y = 0
                pos[node] = (pos_x, pos_y)
            
            else:
                pos[node] = (pos_x, pos_y)
                pos_x += 2
                pos_y = 2    

                count += 1
                if count == 6:
                    pos_x = -6
                    pos_y -= 2
                    count = 0


            if pos_x == 0:
                pos_x = 2

    pos = nx.nx_pydot.graphviz_layout(G, prog='neato')
    
    pos_phi = {
    # Camada superior
    "V": (250, 800),

    # Camada intermediária (conjuntos C1, C2, C3)
    "C1": (100, 650),
    "C2": (250, 650),
    "C3": (400, 650),

    # Variáveis associadas aos conjuntos
    "C1X1": (25, 550), "C1X2_1": (50, 550), "C1X2_2": (75, 550),
    "C1X4": (100, 550), "C1X5": (125, 550), "C1X6": (150, 550),

    "C2X1": (200, 550), "C2X1'": (225, 550),
    "C2X2": (250, 550), "C2X3": (275, 550), "C2X4": (300, 550), "C2X5": (325, 550),

    "C3X2": (375, 550), "C3X3": (400, 550), "C3X4": (425, 550),
    "C3X5": (450, 550), "C3X6": (475, 550), "C3X6'": (500, 550),

    # Camada das variáveis principais
    "X1": (100, 450), "X1'": (100, 400),
    "X2": (200, 450), "X2'": (200, 400),
    "X3": (300, 450), "X3'": (300, 400),
    "X4": (400, 450), "X4'": (400, 400),
    "X5": (500, 450), "X5'": (500, 400),
    "X6": (600, 450), "X6'": (600, 400),

    "auxred": (50, 475),
    "auxred2": (150, 475),
    }

    #print(pos)

    cores_nos = nx.get_node_attributes(G, 'color')

    lista_cores = [cores_nos[node] for node in G.nodes]
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_color=lista_cores, node_size=1200, font_size=9)
    plt.show()

def minimax(G, k, jogada):
    if grafo_colorido(G, k): 
        show_graph(G)
        return True

    if vertice_nao_colorivel(G, k): 
        #show_graph(G)
        return False
    
    vertices_nao_coloridos = [vertice for vertice in G.nodes if G.nodes[vertice]["color"] == colors[0]]
    
    if jogada == jogadas["Alice"]:
        #print(f"Jogada: Alice | Vertices não coloridos: {vertices_nao_coloridos}")
        for vertice in vertices_nao_coloridos:
            index  = 1
            
            while cores_vizinhos(G, vertice, colors[index]):
                index += 1
            
            G.nodes[vertice]["color"] = colors[index]
            print("Jogada ALICE: " + vertice, G.nodes[vertice]["color"])

            if minimax(G, k, jogadas["Bob"]): return True

            G.nodes[vertice]["color"] = colors[0]
        
        return False
    elif jogada == jogadas["Bob"]:
        #print(f"Jogada: Bob | Vertices não coloridos: {vertices_nao_coloridos}")
        for vertice in vertices_nao_coloridos:
            index  = 1
            
            while cores_vizinhos(G, vertice, colors[index]):
                index += 1
            
            G.nodes[vertice]["color"] = colors[index]
            print("Jogada BOB: " + vertice, G.nodes[vertice]["color"])

            if minimax(G, k, jogadas["Alice"]) == False: return False

            G.nodes[vertice]["color"] = colors[0]

        return True
 
def grafo_colorido(G, qtd_cores):
    for vertice in G.nodes:
        if G.nodes[vertice]["color"] == colors[qtd_cores + 1] or G.nodes[vertice]["color"] == colors[0]:
            return False
    return True

def vertice_nao_colorivel(G, k):
    for vertice in G.nodes:
        cores = []
        vizinhos = list(G.neighbors(vertice))

        for vizinho in vizinhos:
            if G.nodes[vizinho]["color"] not in cores and G.nodes[vizinho]["color"] != colors[0]: cores.append(G.nodes[vizinho]["color"])
        
        if len(cores) >= k: 
            print(f"Vertice {vertice} não colorível | Cores: {cores}")
            return True

    return False

def cores_vizinhos(G, vertice, cor):
    vizinhos = list(G.neighbors(vertice))

    for vizinho in vizinhos:
        if cor == G.nodes[vizinho]["color"]:
            return True
    
    return False
    
                
def minimax_cnf(formula, jogada):
    if literal_verdadeiro(formula):
        print(formula["valoracao"])
        print(formula["clausulas"])
        return True
    
    literais_nao_valorados = [literal for literal in formula["valoracao"] if formula["valoracao"][literal] == None]
    if jogada == jogadas["Alice"]:
        for literal in literais_nao_valorados:
            formula["valoracao"][literal] = True

            if minimax_cnf(formula, jogadas["Bob"]): return True

            formula["valoracao"][literal] = None
        return False
    
    elif jogada == jogadas["Bob"]:
        for literal in literais_nao_valorados:
            formula["valoracao"][literal] = False

            if minimax_cnf(formula, jogadas["Alice"]) == False: return False

            formula["valoracao"][literal] = None
        return True

    
def literal_verdadeiro(formula):
    count = 0
    for clausula in formula["clausulas"]:
        for literal in clausula:
            if literal[:2] in formula["valoracao"] and formula["valoracao"][literal[:2]] == True:
                count += 1
                break
    if count == len(formula["clausulas"]): return True
    return False

def main():

    grafo = {
        
    }

    estado = {
        'grafo': grafo,
        'coloracao': {vertice: None for vertice in grafo},
        'cores': set()
    }

    grafo = reducao(pos_cnf)
    #grafo.nodes["V"]["color"] = colors[1]
    #print(nx.get_node_attributes(grafo, 'color'))
    #show_graph(grafo)
    #print(list(grafo.neighbors("V")))
    
    res = minimax(grafo, 3, jogadas["Bob"])
    show_graph(grafo)

    print(f"Minimax grafo: {res}")

    res = minimax_cnf(pos_cnf_jogo_valoracao, jogadas["Alice"])
    print(f"Minimax CNF: {res}")

main()