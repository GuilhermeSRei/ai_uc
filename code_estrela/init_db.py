
"""
Arquivo: init_db.py
Descrição: Inicializa o banco de dados SQLite (grafo.db) com as tabelas e dados do grafo e heurística usados pelo algoritmo A*.
Execução:
1. Cria as tabelas 'arestas' e 'heuristica' se não existirem.
2. Insere os dados do grafo e heurística, limpando dados antigos.
3. Após rodar este script, o banco estará pronto para uso pelo estrela.py.
Dependências: sqlite3
"""


import sqlite3

conn = sqlite3.connect('grafo.db')
c = conn.cursor()

# Criação das tabelas
c.execute('''CREATE TABLE IF NOT EXISTS arestas (
    origem TEXT,
    destino TEXT,
    custo INTEGER
)''')
c.execute('''CREATE TABLE IF NOT EXISTS heuristica (
    estado TEXT PRIMARY KEY,
    valor INTEGER
)''')

# Dados do grafo (arestas e distâncias entre cidades)
arestas = [
    ('Arad', 'Zerind', 75),
    ('Arad', 'Sibiu', 140),
    ('Arad', 'Timisoara', 118),
    ('Zerind', 'Oradea', 71),
    ('Zerind', 'Arad', 75),
    ('Oradea', 'Zerind', 71),
    ('Oradea', 'Sibiu', 151),
    ('Sibiu', 'Arad', 140),
    ('Sibiu', 'Oradea', 151),
    ('Sibiu', 'Fagaras', 99),
    ('Sibiu', 'Rimnicu Vilcea', 80),
    ('Fagaras', 'Sibiu', 99),
    ('Fagaras', 'Bucharest', 211),
    ('Rimnicu Vilcea', 'Sibiu', 80),
    ('Rimnicu Vilcea', 'Pitesti', 97),
    ('Rimnicu Vilcea', 'Craiova', 146),
    ('Pitesti', 'Rimnicu Vilcea', 97),
    ('Pitesti', 'Craiova', 138),
    ('Pitesti', 'Bucharest', 101),
    ('Craiova', 'Rimnicu Vilcea', 146),
    ('Craiova', 'Pitesti', 138),
    ('Craiova', 'Dobreta', 120),
    ('Dobreta', 'Craiova', 120),
    ('Dobreta', 'Mehadia', 75),
    ('Mehadia', 'Dobreta', 75),
    ('Mehadia', 'Lugoj', 70),
    ('Lugoj', 'Mehadia', 70),
    ('Lugoj', 'Timisoara', 111),
    ('Timisoara', 'Lugoj', 111),
    ('Timisoara', 'Arad', 118),
    ('Bucharest', 'Fagaras', 211),
    ('Bucharest', 'Pitesti', 101),
    ('Bucharest', 'Giurgiu', 90),
    ('Bucharest', 'Urziceni', 85),
    ('Giurgiu', 'Bucharest', 90),
    ('Urziceni', 'Bucharest', 85),
    ('Urziceni', 'Hirsova', 98),
    ('Urziceni', 'Vaslui', 142),
    ('Hirsova', 'Urziceni', 98),
    ('Hirsova', 'Eforie', 86),
    ('Eforie', 'Hirsova', 86),
    ('Vaslui', 'Urziceni', 142),
    ('Vaslui', 'Iasi', 92),
    ('Iasi', 'Vaslui', 92),
    ('Iasi', 'Neamt', 87),
    ('Neamt', 'Iasi', 87)
]

# Heurística: distância em linha reta até Bucharest
heuristicas = [
    ('Arad', 366),
    ('Bucharest', 1),
    ('Craiova', 160),
    ('Dobreta', 242),
    ('Eforie', 161),
    ('Fagaras', 178),
    ('Giurgiu', 77),
    ('Hirsova', 151),
    ('Iasi', 226),
    ('Lugoj', 244),
    ('Mehadia', 241),
    ('Neamt', 234),
    ('Oradea', 380),
    ('Pitesti', 98),
    ('Rimnicu Vilcea', 193),
    ('Sibiu', 253),
    ('Timisoara', 329),
    ('Urziceni', 80),
    ('Vaslui', 199),
    ('Zerind', 374)
]

# Limpa dados antigos e insere novos
c.execute('DELETE FROM arestas')
c.execute('DELETE FROM heuristica')
c.executemany('INSERT INTO arestas VALUES (?, ?, ?)', arestas)
c.executemany('INSERT INTO heuristica VALUES (?, ?)', heuristicas)

conn.commit()
conn.close()
print('Banco de dados criado e populado com sucesso!')

