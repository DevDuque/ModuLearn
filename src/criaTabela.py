import sqlite3

# Documento responsável pela criação das tabelas do banco de dados (Cursos, Modulos, Alunos, Professores)

# Conexão com o Banco de Dados
conn = sqlite3.connect('ModuLearn.db')
cursor = conn.cursor()

# Criando tabelas Curso e Aluno
def criaTabelas():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            alunoID INTEGER PRIMARY KEY AUTOINCREMENT,
            nomeAluno TEXT NOT NULL,
            nota INTEGER,
            frequencia INTEGER,
            nomeUsuario TEXT NOT NULL,
            senha TEXT NOT NULL,
            cursoID INTEGER NOT NULL,
            FOREIGN KEY (cursoID) REFERENCES cursos(cursoID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professores (
            professorID INTEGER PRIMARY KEY AUTOINCREMENT,
            nomeProfessor TEXT NOT NULL,
            nomeUsuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modulos (
                moduloID INTEGER PRIMARY KEY AUTOINCREMENT,
                numeroModulo INTEGER,
                nomeModulo TEXT NOT NULL,
                cursoID INTEGER,
                FOREIGN KEY (cursoID) REFERENCES cursos(cursoID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            cursoID INTEGER PRIMARY KEY AUTOINCREMENT,
            nomeCurso TEXT NOT NULL,
            duracao INTEGER CHECK(duracao IN(45,60,100)) NOT NULL,
            professorID INTEGER NOT NULL,
            tipo TEXT CHECK(tipo IN("EAD", "Presencial")),
            FOREIGN KEY (professorID) REFERENCES professores(professorID)
        ) 
    ''')
    conn.close()