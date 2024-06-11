import sqlite3

# Documento responsável pela criação das tabelas do banco de dados (Cursos, Modulos, Alunos, Professores)

# Conexão com o Banco de Dados
conn = sqlite3.connect('ModuLearn.db')
cursor = conn.cursor()

# Criando tabelas Curso e Aluno
def criaTabelas():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            alunoID TEXT PRIMARY KEY,
            nomeAluno TEXT NOT NULL,
            nota INTEGER,
            frequencia INTEGER,
            nomeUsuario TEXT NOT NULL,
            senha TEXT NOT NULL,
            cursoID TEXT,
            FOREIGN KEY (cursoID) REFERENCES cursos(cursoID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professores (
            professorID TEXT PRIMARY KEY,
            nomeProfessor TEXT NOT NULL,
            nomeUsuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS administradores (
            adminID TEXT PRIMARY KEY,
            nomeAdmin TEXT NOT NULL,
            nomeUsuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modulos (
                moduloID TEXT PRIMARY KEY,
                numeroModulo INTEGER,
                nomeModulo TEXT NOT NULL,
                cursoID TEXT,
                FOREIGN KEY (cursoID) REFERENCES cursos(cursoID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            cursoID TEXT PRIMARY KEY,
            nomeCurso TEXT NOT NULL,
            duracao INTEGER CHECK(duracao IN(45,60,100)) NOT NULL,
            professorID TEXT NOT NULL,
            tipo TEXT CHECK(tipo IN("EAD", "Presencial")),
            FOREIGN KEY (professorID) REFERENCES professores(professorID)
        ) 
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS requisicoes (
            requisicaoID TEXT PRIMARY KEY,
            alunoID TEXT,
            cursoID TEXT,
            status TEXT CHECK(status IN ('pendente', 'aceito', 'rejeitado')) NOT NULL,
            FOREIGN KEY (alunoID) REFERENCES alunos(alunoID),
            FOREIGN KEY (cursoID) REFERENCES cursos(cursoID)
        )
    ''')
    conn.close()