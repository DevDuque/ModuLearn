import sqlite3
import hashlib

# Conexão com o DB
conn = sqlite3.connect('ModuLearn.db')
cursor = conn.cursor()

# Criando a tabela "cursos"
cursor.execute('''
                CREATE TABLE IF NOT EXISTS cursos (
                cursoID INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
                )
               ''')

# Criando a tabela "modulos"
cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS modulos (
                moduloID INTEGER PRIMARY KEY AUTOINCREMENT,
                numeroModulo INT,
                nomeModulo TEXT NOT NULL,
                cursoID INTEGER,
                FOREIGN KEY (cursoID) REFERENCES cursos(cursoID)
                )               
''')

# Criando a tabela "professores"
cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS professores (
                professorID INTEGER PRIMARY KEY AUTOINCREMENT,
                nomeProfessor TEXT NOT NULL,
                nomeUsuario TEXT UNIQUE NOT NULL,
                senhaProfessor TEXT NOT NULL
                )
''')

# Inserindo dados na tabela "cursos"
cursor.execute("INSERT INTO cursos (nome) VALUES ('Curso Exemplo')")

# Pegando o cursoID do curso inserido
curso_id = cursor.lastrowid

# Inserindo dados na tabela "modulos"
cursor.execute("INSERT INTO modulos (numeroModulo, nomeModulo, cursoID) VALUES (11, 'Introdução', ?)", (curso_id,))

# Inserindo dados na tabela "professores"

cursor.execute("INSERT INTO professores (nomeProfessor, nomeUsuario, senhaProfessor) VALUES ('Caio', 'caioca', 1234)")

# Selecionando e imprimindo os valores da tabela "modulos"
cursor.execute("SELECT * FROM modulos")
modulos = cursor.fetchall()
print("Dados da tabela modulos:")
for modulo in modulos:
    print(modulo)

# Selecionando e imprimindo os valores da tabela "professores"
cursor.execute("SELECT * FROM professores")
professores = cursor.fetchall()
print("Dados da tabela professores:")
for professor in professores:
    print(professor)

conn.commit()
conn.close()
