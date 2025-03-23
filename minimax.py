from turtle import color
import networkx as nx
import matplotlib.pyplot as plt

jogadas = {
    'Alice': 0,
    'Bob': 1
}

colors = {
    1: 'red',
    2: 'green',
    3: 'blue',
    4: 'yellow',
    0: 'gray' # representa os vértices não coloridos
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

def minimax(G, k, jogada):
    if grafo_colorido(G, k): 
        return True, "AEND", None, None

    if vertice_nao_colorivel(G, k)[0]: 
        return False, "BEND", None, None
    
    vertices_nao_coloridos = pegar_vertices_nao_coloridos(G)
    if jogada == jogadas["Alice"]:
        for vertice in vertices_nao_coloridos:
            colorir_vertice(G, vertice)

            if minimax(G, k, jogadas["Bob"])[0] == True: 
                descolorir_vertice(G, vertice)
                return True, "A", vertice, G.nodes[vertice]["color"]

            descolorir_vertice(G, vertice)
        
        return False, "A", None, None
    
    elif jogada == jogadas["Bob"]:
        for vertice in vertices_nao_coloridos:
            colorir_vertice(G, vertice)
            
            if minimax(G, k, jogadas["Alice"])[0] == False: 
                descolorir_vertice(G, vertice)
                return False, "B", vertice, G.nodes[vertice]["color"]

            descolorir_vertice(G, vertice)

        return True, "B", None, None

def pegar_vertices_nao_coloridos(G):
    return [vertice for vertice in G.nodes if G.nodes[vertice]["color"] == colors[0]]

def colorir_vertice(G, vertice):
    G.nodes[vertice]["color"] = colors[pegar_menor_cor(G, vertice)]

def descolorir_vertice(G, vertice):
    G.nodes[vertice]["color"] = colors[0] # cinza

def pegar_menor_cor(G, vertice):
    cor = 1 # vermelho
    while verificar_cores_vizinhas(G, vertice, colors[cor]):
        cor += 1
    return cor
 
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
            if G.nodes[vizinho]["color"] not in cores and G.nodes[vizinho]["color"] != colors[0]: 
                cores.append(G.nodes[vizinho]["color"])
        
        if len(cores) >= k: 
            return True, vertice

    return False, None

def verificar_cores_vizinhas(G, vertice, cor):
    vizinhos = list(G.neighbors(vertice))

    for vizinho in vizinhos:
        if cor == G.nodes[vizinho]["color"]:
            return True
    
    return False
                
def minimax_cnf(formula, jogada):
    if literal_verdadeiro(formula):
        #print(formula["valoracao"])
        #print(formula["clausulas"])
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

def jogo_coloracao_gulosa(G, phi, jogador, k):
    jogador_escolhido = None
    while jogador_escolhido not in jogadas.values():
        escolha = input("Escolha um jogador (Alice ou Bob): ")
        if escolha in jogadas:
            jogador_escolhido = jogadas[escolha]
        else:
            print("Escolha inválida. Tente novamente.")
        
    #jogador_escolhido = -1 # Descomente essa linha para deixar o jogo da forma IA vs IA
    jogo = 0
    num_turnos = 0

    while(jogo == 0):
        vertices_nao_coloridos = pegar_vertices_nao_coloridos(G)
        
        print(f"Turno: {num_turnos}")

        if jogador == jogadas["Alice"]:
            if jogador_escolhido == jogadas["Alice"]:
                print("Vértices não coloridos: ", vertices_nao_coloridos)
                vertice = input("ALICE - Digite o vértice: ")
            
                if vertice in vertices_nao_coloridos:
                    colorir_vertice(G, vertice)
                else:
                    print("Vértice já está colorido ou não existe")
                    continue

            else:
                G_copia = G.copy()
                res = minimax(G_copia, k, jogadas["Alice"])
                if res[0] == False:
                    vertice = pegar_vertices_nao_coloridos(G)[0];
                    colorir_vertice(G, vertice)
                    print(f"Resp. MiniMax: Alice perde | Vertice: {vertice} | Cor: {G.nodes[vertice]['color']}")
                else:
                    colorir_vertice(G, res[2])
                    print(f"Resp. MiniMax: Alice vence | Vertice: {res[2]} | Cor: {G.nodes[res[2]]['color']}")

            jogador = jogadas["Bob"]

        else:
            if jogador_escolhido == jogadas["Bob"]:
                print("Vértices não coloridos: ", vertices_nao_coloridos)
                vertice = input("Bob - Digite o vértice: ")
            
                if vertice in vertices_nao_coloridos:
                    colorir_vertice(G, vertice)
                else:
                    print("Vértice já está colorido ou não existe")
                    continue

            else:
                G_copia = G.copy()
                res = minimax(G_copia, k, jogadas["Bob"])
                if res[0] == True:
                    vertice = pegar_vertices_nao_coloridos(G)[0];
                    colorir_vertice(G, vertice)
                    print(f"Resp. MiniMax: Bob perde | Vertice: {vertice} | Cor: {G.nodes[vertice]['color']}")
                else:
                    colorir_vertice(G, res[2])
                    print(f"Resp. MiniMax: Bob vence | Vertice: {res[2]} |  {G.nodes[res[2]]['color']}")
            
            jogador = jogadas["Alice"]
    
        if grafo_colorido(G, k):
            jogo = 1
        if vertice_nao_colorivel(G, k)[0]:
            jogo = -1
            vertice = vertice_nao_colorivel(G, k)[1]
        num_turnos += 1
        mostrar_grafo(G, phi)
    
    if jogo == 1:
        print("Jogo terminou com Alice vencendo")
    else:
        print(f"Jogo terminou com Bob vencendo | Vertice não colorivel: {vertice}") 

def main():

    total_variaveis = 2

    pos_cnf_phi = {
        'clausulas': [
            ["X1", "X2", "X2", "X2", "X2", "X1"],
            #["X1", "X2", "X3", "X4", "X5", "X6"],
            #["X1", "X3", "X3", "X4", "X4", "X1"],
            #["X1", "X2", "X2", "X2", "X2", "X2"],
            #["X1", "X2", "X1", "X2", "X2", "X2"],
        ],
        'variaveis': [],
        'valoracao': {
        }
    }

    pos_cnf_phi["variaveis"] = [f"X{i+1}" for i in range(total_variaveis)]
    for i in range(total_variaveis):
        pos_cnf_phi["valoracao"][f"X{i+1}"] = None

    grafo = reducao(pos_cnf_phi)
    print(grafo.nodes)

    mostrar_grafo(grafo, pos_cnf_phi)
    jogo_coloracao_gulosa(grafo, pos_cnf_phi, jogadas["Bob"], 3)

main()