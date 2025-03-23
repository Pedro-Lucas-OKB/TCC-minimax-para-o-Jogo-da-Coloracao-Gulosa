from visualizacao import mostrar_grafo

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