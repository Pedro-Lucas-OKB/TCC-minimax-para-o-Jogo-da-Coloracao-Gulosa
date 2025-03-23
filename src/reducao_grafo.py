import networkx as nx
from minimax import colors

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
        G.add_node(variavel) # X1, X2, X3, ...
        G.add_node(f"{variavel}\'") # X1', X2', X3', ...

        G.add_edge(variavel, f"{variavel}\'") # X1 - X1', X2 - X2', X3 - X3', ...
    
        for vertice in G.nodes:
            if variavel in vertice and variavel != vertice:
                G.add_edge(variavel, vertice)
        
def criar_ciclos_clausula(G, clausula, count_clausula):
    for i in range(len(clausula)):
        variavel = f"C{count_clausula}L{i + 1}{clausula[i]}" # C1L1X1, C1L2X2, C1L3X3, ...
        G.add_node(variavel)
            
        if i == 0:
            G.add_edge(f"C{count_clausula}", variavel)
        
        elif i == len(clausula) - 1:
            G.add_edge(f"C{count_clausula}", variavel)
            G.add_edge(f"C{count_clausula}L{i}{clausula[i - 1]}", variavel)
            
        else:            
            G.add_edge(f"C{count_clausula}L{i}{clausula[i - 1]}", variavel)