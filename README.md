# Jogo da Coloração Gulosa e Algoritmo Minimax

Este repositório contém a implementação do **Jogo da Coloração Gulosa**, um problema estudado no contexto de complexidade computacional. Além disso, apresenta a aplicação do **Algoritmo MiniMax** para análise de estratégias vencedoras no jogo.

## Descrição

O Jogo da Coloração Gulosa é uma variante do **Jogo da Coloração**, onde dois jogadores (Alice e Bob) alternam turnos para colorir os vértices de um grafo seguindo regras específicas:

- As cores devem ser números inteiros não negativos.
- Cada vértice recebe a menor cor disponível que não esteja sendo utilizada por seus vizinhos.
- Alice vence se conseguir colorir todo o grafo usando um conjunto finito de cores.
- Bob vence se for possível forçar a necessidade de mais cores do que as disponíveis.

O repositório contém a implementação deste jogo utilizando a biblioteca **NetworkX** para manipulação de grafos e **Matplotlib** para visualização.

## Funcionalidades

- **Redução de fórmulas POS-CNF-6 para grafos:** Transforma uma fórmula lógica na forma normal conjuntiva positiva (POS-CNF-6) em um grafo específico usado no jogo.
- **Implementação do Algoritmo Minimax:** Avaliação das jogadas de Alice e Bob para determinar estratégias vencedoras.
- **Modo interativo:** Permite jogar contra a Inteligência Artificial baseada no Minimax.
- **Visualização dos grafos:** Gera representações gráficas dos estados do jogo.

## Como executar

### Pré-requisitos

- Python 3.x
- Bibliotecas necessárias: `networkx`, `matplotlib`

Para instalar as dependências, utilize:

```bash
pip install -r .\requisitos.txt
```

### Execução

Para iniciar o jogo, execute o seguinte comando:

```bash
python main.py
```

O programa solicitará que o usuário escolha se deseja jogar como **Alice** ou **Bob**. A IA tomará as decisões do adversário utilizando o **Minimax**.

## Estrutura do Código

- `minimax.py` → Implementação do jogo, minimax e funções auxiliares.
- `reducao_grafo.py` → Código responsável por transformar fórmulas POS-CNF-6 em grafos para o jogo.
- `visualizacao.py` → Geração de imagens dos grafos durante a execução do jogo.

## Exemplos de Uso

### Exemplo de Fórmula POS-CNF-6

```python
pos_cnf_6 = {
    'clausulas': [
        ["X1", "X2", "X2", "X2", "X2", "X1"],
        ["X1", "X2", "X3", "X4", "X5", "X6"],
        ["X1", "X3", "X3", "X4", "X4", "X1"],
    ],
    'variaveis': ["X1", "X2", "X3", "X4", "X5", "X6"],
    'valoracao': {
        "X1": None,
        "X2": None,
        "X3": None,
        "X4": None,
        "X5": None,
        "X6": None
    }
}
```

Esse exemplo representa uma fórmula lógica que pode ser reduzida a um grafo para o jogo.

## Referências

Este código foi desenvolvido como parte do **Trabalho de Conclusão de Curso (TCC)**, que explora a complexidade computacional de espaço do **Jogo da Coloração Gulosa**.