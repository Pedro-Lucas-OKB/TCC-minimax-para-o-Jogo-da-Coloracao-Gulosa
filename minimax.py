""" from copy import deepcopy
from sympy import true, false
from sympy.logic.boolalg import to_cnf
from sympy.abc import xi """
from itertools import count
from math import e
import networkx as nx
import matplotlib.pyplot as plt
from numpy import var

colors = {
        1: 'red',
        2: 'green',
        3: 'blue',
        4: 'yellow',
        0: 'none',
    }

pos_cnf = {
    'clausulas': [
        ["X1", "X2", "X3", "X4", "X5", "X6"],  # Cláusula 1
        ["X1", "X1", "X2", "X3", "X4", "X5"],  # Cláusula 2
        ["X2", "X3", "X4", "X5", "X6", "X6\'"],  # Cláusula 3
        ["X1", "X2", "X3", "X3", "X5", "X6"],  # Cláusula 4
        ["X1", "X2", "X2", "X4", "X5", "X6"],  # Cláusula 5
        ["X1", "X3", "X3", "X4", "X5", "X6"],  # Cláusula 6
    ],
    'variaveis': ['X1', 'X2', 'X3', 'X4', 'X5', 'X6'],
    'valoracao': {
        'X1': False,
        'X2': False,
        'X3': True,
        'X4': True,
        'X5': False,
        'X6': True,
    }
}

def reducao(formula):
    grafo = {
        'V': ['C'],
        'C': [],
        'Ciclos': [],
        'Nos_false': [],
        'Nos_true': []
    }

    G = nx.Graph()
    G.add_node('V')
    G.add_node('C')
    G.add_edge('V', 'C')
    nx.set_node_attributes(G, colors, 'color')
    ciclo = ['C']

    """ for variavel in formula["variaveis"]:
        grafo[variavel] = set() """

    #print(G.nodes)

    clausula = formula["clausulas"][2]
    #G.add_nodes_from(clausula)

    for i in range(len(clausula)):
        variavel = clausula[i]
        vertice = f"V{i}{variavel}"
        grafo[vertice] = set()
        

        if i == 0:
            grafo[vertice].add('C')
            grafo[vertice].add(clausula[i + 1])
            G.add_node(variavel)
            G.add_edge('C', variavel)
        
        elif i == len(formula["clausulas"]) - 1:
            grafo[vertice].add('C')
            grafo[vertice].add(clausula[i - 1])
            G.add_node(variavel)
            G.add_edge('C', variavel)
        
        else:
            grafo[vertice].add(clausula[i - 1])
            grafo[vertice].add(clausula[i + 1])
            G.add_node(variavel)
        
            G.add_edge(clausula[i - 1], variavel)
            G.add_edge(clausula[i + 1], variavel)
        

        ciclo.append(vertice)

    

    for variavel in clausula:
        if formula["valoracao"][variavel[:2]] == True:
            grafo["Nos_true"].append(variavel)
            grafo["Nos_false"].append('none')
            G.add_node(f"T{variavel}")
            G.add_node(f"Tnone{variavel}")

            G.add_edge(variavel, f"T{variavel}")
            G.add_edge(f"T{variavel}", f"Tnone{variavel}")

        else:
            grafo["Nos_false"].append(variavel)
            grafo["Nos_true"].append('none')
            G.add_node(f"F{variavel}")
            G.add_node(f"Fnone{variavel}")

            G.add_edge(variavel, f"F{variavel}")
            G.add_edge(f"F{variavel}", f"Fnone{variavel}")        

    show_graph(G)
    #grafo[formula["variaveis"][0]].add('C')
    #grafo[formula["variaveis"][len(formula["variaveis"]) - 1]].add('C')

    grafo["Ciclos"].append(tuple(ciclo))
    
    print(grafo)

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
                print('aqui')
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
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.show()



def main():
    

    print(pos_cnf["clausulas"][0][0])

    grafo = {
        
    }

    estado = {
        'grafo': grafo,
        'coloracao': {vertice: None for vertice in grafo},
        'cores': set()
    }

    reducao(pos_cnf)

    """ G = nx.Graph()
    G.add_node(1)
    G.add_node(2)

    G.add_edge(1, 2)
    print(G.) """

main()