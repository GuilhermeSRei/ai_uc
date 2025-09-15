"""
Arquivo: init_db.py
Descrição: Inicializa o banco de dados SQLite (grafo.db) com as tabelas e dados do grafo e heurística usados pelo algoritmo A*.
Execução:
1. Cria as tabelas 'arestas' e 'heuristica' se não existirem.
2. Insere os dados do grafo e heurística caso estejam ausentes.
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

# Dados do grafo
arestas = [
    ('A', 'B', 1),
    ('A', 'C', 4),
    ('B', 'D', 5),
    ('B', 'E', 1),
    ('C', 'F', 3),
    ('E', 'F', 1)
]

heuristicas = [
    ('A', 7),
    ('B', 6),
    ('C', 2),
    ('D', 1),
    ('E', 1),
    ('F', 0)
]

# Inserção dos dados
c.execute('DELETE FROM arestas')
c.execute('DELETE FROM heuristica')
c.executemany('INSERT INTO arestas VALUES (?, ?, ?)', arestas)
c.executemany('INSERT INTO heuristica VALUES (?, ?)', heuristicas)

conn.commit()
conn.close()
print('Banco de dados criado e populado com sucesso!')
