import sqlite3

# Conexão com o Banco de Dados
conn = sqlite3.connect('ModuLearn.db')
cursor = conn.cursor()

# Criando tabelas Curso e Aluno
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos(
        alunoID INTEGER PRIMARY KEY AUTOINCREMENT,
        nomeAluno TEXT NOT NULL,
        nota INTEGER,
        frequencia INTEGER,
        nomeUsuario TEXT NOT NULL,
        senha TEXT NOT NULL
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
            numeroModulo INT,
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