from minimax import jogo_coloracao_gulosa, jogadas
from reducao_grafo import reducao
from visualizacao import mostrar_grafo

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