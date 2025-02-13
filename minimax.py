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
        #["X1", "X2", "X3", "X3", "X5", "X6"],  # Cláusula 4
        #["X1", "X2", "X2", "X4", "X5", "X6"],  # Cláusula 5
        #["X1", "X3", "X3", "X4", "X5", "X6"],  # Cláusula 6
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
    G = nx.Graph()
    G.add_node('V')
    
    nx.set_node_attributes(G, colors, 'color')

    clausula = formula["clausulas"][2]

    count_clausula = 1
    for clausula in formula["clausulas"]:
        G.add_node(f"C{count_clausula}")
        G.add_edge('V', f"C{count_clausula}")
        
        criar_ciclos_clausula(G, clausula, count_clausula)
            
        criar_vertices_variavel(formula, G, clausula)  

        count_clausula += 1      
        
    return G

def criar_vertices_variavel(formula, G, clausula):
    for variavel in clausula:
        if formula["valoracao"][variavel[:2]] == True:
            G.add_node(f"T{variavel}")
            G.add_node(f"Tnone{variavel}")

            G.add_edge(variavel, f"T{variavel}")
            G.add_edge(f"T{variavel}", f"Tnone{variavel}")

        else:
            G.add_node(f"F{variavel}")
            G.add_node(f"Fnone{variavel}")

            G.add_edge(variavel, f"F{variavel}")
            G.add_edge(f"F{variavel}", f"Fnone{variavel}")

def criar_ciclos_clausula(G, clausula, count_clausula):
    for i in range(len(clausula)):
        variavel = f"C{count_clausula}{clausula[i]}"
        G.add_node(variavel)
            
        if i == 0 or i == len(clausula) - 1:
            G.add_edge(f"C{count_clausula}", variavel)
            
        else:            
            G.add_edge(clausula[i - 1], variavel)
            G.add_edge(clausula[i + 1], variavel)
    
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

    pos = nx.nx_pydot.graphviz_layout(G, root='V')
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.show()

def main():

    grafo = {
        
    }

    estado = {
        'grafo': grafo,
        'coloracao': {vertice: None for vertice in grafo},
        'cores': set()
    }

    grafo = reducao(pos_cnf)
    show_graph(grafo)

main()