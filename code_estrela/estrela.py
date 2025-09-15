"""
Arquivo: estrela.py
Descrição: Implementa o algoritmo A* para encontrar o caminho ótimo entre dois pontos em um grafo, usando dados armazenados em um banco SQLite. Após o cálculo, exibe o caminho e uma visualização gráfica destacando o resultado.
Execução:
1. O usuário informa o ponto inicial e final.
2. O algoritmo A* calcula o caminho ótimo usando dados do banco.
3. O caminho é exibido no terminal e visualizado graficamente.
Dependências: matplotlib, networkx, sqlite3
Banco de dados deve ser inicializado previamente com init_db.py.
"""

import heapq
import sqlite3
import matplotlib.pyplot as plt
import networkx as nx
import os

# Classe que representa um nó do grafo, guarda estado, custos e pai
class No:
    def __init__(self, estado, g=0, h=0, pai=None):
        self.estado = estado
        self.g = g  # custo real até o nó
        self.h = h  # heurística
        self.f = g + h  # custo total estimado
        self.pai = pai
    def __lt__(self, outro):
        return self.f < outro.f

# Função principal do algoritmo A*, encontra o caminho ótimo
# Usa listas aberta/fechada e funções de custo/heurística
# Retorna o caminho como lista de estados

def a_estrela(nó_inicial, nó_objetivo, gerar_sucessores, h, w):
    aberta = []  # Lista de nós a serem explorados
    fechada = set()  # Conjunto de nós já explorados
    nó_inicial = No(nó_inicial, g=0, h=h(nó_inicial))  # Cria nó inicial com heurística
    heapq.heappush(aberta, nó_inicial)  # Adiciona nó inicial na lista aberta
    abertos_dict = {nó_inicial.estado: nó_inicial}  # Dicionário para acesso rápido aos nós abertos
    while aberta:  # Enquanto houver nós para explorar
        nó_atual = heapq.heappop(aberta)  # Seleciona nó com menor f
        abertos_dict.pop(nó_atual.estado, None)  # Remove nó atual do dicionário de abertos
        if nó_atual.estado == nó_objetivo:  # Se chegou ao objetivo
            caminho = []  # Lista para reconstruir o caminho
            while nó_atual:  # Percorre os pais até o início
                caminho.append(nó_atual.estado)
                nó_atual = nó_atual.pai
            return list(reversed(caminho))  # Retorna caminho do início ao objetivo
        for sucessor in gerar_sucessores(nó_atual.estado):  # Para cada sucessor do nó atual
            custo_atual_sucessor = nó_atual.g + w(nó_atual.estado, sucessor)  # Calcula custo g do sucessor
            if sucessor in abertos_dict:  # Se já está na aberta
                nó_sucessor = abertos_dict[sucessor]
                if nó_sucessor.g <= custo_atual_sucessor:  # Se o caminho não é melhor, ignora
                    continue
            elif sucessor in fechada:  # Se já está na fechada
                continue  # Ignora
            else:
                nó_sucessor = No(sucessor)  # Cria novo nó sucessor
            nó_sucessor.g = custo_atual_sucessor  # Atualiza custo g
            nó_sucessor.h = h(sucessor)  # Atualiza heurística
            nó_sucessor.f = nó_sucessor.g + nó_sucessor.h  # Atualiza custo total f
            nó_sucessor.pai = nó_atual  # Define pai do sucessor
            heapq.heappush(aberta, nó_sucessor)  # Adiciona sucessor na aberta
            abertos_dict[sucessor] = nó_sucessor  # Atualiza dicionário de abertos
        fechada.add(nó_atual.estado)  # Adiciona nó atual na fechada
    return None  # Se não encontrou caminho, retorna None

# Função que retorna uma conexão com o banco de dados
def get_conexao():
    return sqlite3.connect('grafo.db')  # Retorna uma conexão com o banco de dados SQLite

# Função que busca os sucessores de um nó no banco
def gerar_sucessores_sql(estado):
    conn = get_conexao()  # Abre conexão com o banco
    c = conn.cursor()  # Cria cursor para executar comandos SQL
    c.execute('SELECT destino FROM arestas WHERE origem = ?', (estado,))  # Busca sucessores do estado
    res = [row[0] for row in c.fetchall()]  # Extrai resultados em uma lista
    conn.close()  # Fecha conexão
    return res  # Retorna lista de sucessores

# Função que busca o valor heurístico de um nó no banco
def h_sql(estado):
    conn = get_conexao()  # Abre conexão com o banco
    c = conn.cursor()  # Cria cursor para executar comandos SQL
    c.execute('SELECT valor FROM heuristica WHERE estado = ?', (estado,))  # Busca valor heurístico do estado
    row = c.fetchone()  # Pega o resultado
    conn.close()  # Fecha conexão
    return row[0] if row else 0  # Retorna valor heurístico ou 0 se não encontrado

# Função que busca o custo entre dois nós no banco
def w_sql(atual, sucessor):
    conn = get_conexao()  # Abre conexão com o banco
    c = conn.cursor()  # Cria cursor para executar comandos SQL
    c.execute('SELECT custo FROM arestas WHERE origem = ? AND destino = ?', (atual, sucessor))  # Busca custo entre os nós
    row = c.fetchone()  # Pega o resultado
    conn.close()  # Fecha conexão
    return row[0] if row else float('inf')  # Retorna custo ou infinito se não encontrado

# Ponto de entrada do programa
if __name__ == "__main__":
    # Exibe lista somente com os nomes das cidades da heurística
    import sqlite3
    conn = sqlite3.connect('grafo.db')
    c = conn.cursor()
    c.execute('SELECT estado FROM heuristica')
    cidades_heuristica = [row[0] for row in c.fetchall()]
    conn.close()
    print("Cidades presentes na heurística:")
    for cidade in cidades_heuristica:
        print(cidade)
    # Recebe do usuário a cidade inicial e final
    inicio = input("Digite o nome da cidade inicial: ").strip().title()
    fim = input("Digite o nome da cidade final: ").strip().title()
    # Executa o algoritmo A* para encontrar o caminho
    caminho = a_estrela(inicio, fim, gerar_sucessores_sql, h_sql, w_sql)
    print("Caminho encontrado:", ' -> '.join(caminho) if caminho else "Nenhum caminho encontrado")

    # Visualização gráfica do grafo e do caminho encontrado
    conn = get_conexao()
    c = conn.cursor()
    c.execute('SELECT origem, destino, custo FROM arestas')
    arestas = c.fetchall()
    conn.close()

    # Cria o grafo usando networkx
    G = nx.DiGraph()
    for origem, destino, custo in arestas:
        G.add_edge(origem, destino, weight=custo)

    # Define posições dos nós para o desenho
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8,6))
    # Desenha todos os nós e arestas
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1200, font_size=14)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Destaca o caminho encontrado
    if caminho and len(caminho) > 1:
        caminho_edges = list(zip(caminho, caminho[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=caminho_edges, edge_color='red', width=3)
        nx.draw_networkx_nodes(G, pos, nodelist=caminho, node_color='orange', node_size=1300)
    plt.title(f'Caminho: {" -> ".join(caminho) if caminho else "Nenhum"}')
    plt.show()

