# Documento responsável pela criação das tabelas do banco de dados (Cursos, Modulos, Alunos, Professores)

import sqlite3

# Conexão com o Banco de Dados
conn = sqlite3.connect('ModuLearn.db')
cursor = conn.cursor()

# Criando tabelas Curso e Aluno
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cursos (
            cursoID INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
            duracao INTEGER CHECK(duracao IN(45,60,100)) NOT NULL,
            professorID INTEGER NOT NULL,
            alunoID INTEGER NOT NULL,
            tipo TEXT CHECK(tipo IN("EAD", "Presencial"))
               
            FOREIGN KEY (professorID)
               REFERENCES professores (professorID)

            FOREIGN KEY (alunoID)
               REFERENCES alunos (alunoID)
    )
               
    CREATE TABLE IF NOT EXISTS alunos(
            alunoID INTEGER PRIMARY KEY AUTOINCREMENT
            nome TEXT NOT NULL,
            nota REAL,
            frequencia REAL,
            nomeUsuario TEXT NOT NULL,
            senha TEXT NOT NULL
    )
''')

conn.commit()