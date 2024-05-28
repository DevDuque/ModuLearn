import sqlite3
import hashlib
import criaTabela

# Documento responsável pelo CRUD de Alunos & Professores

criaTabela.criaTabelas()

# Conexão com o Banco de Dados
conn = sqlite3.connect('ModuLearn.db')
cursor = conn.cursor()

# Função para cadastro de usuário no BD
def cadastrar_usuario(escolha):

    nome = input("Nome: ")
    usuario = input("Nome de Usuário: ")
    senha = input("Senha: ")

    senhaHash = hashlib.sha256(senha.encode()).hexdigest()

    if escolha == 1:
        cursoID = input("ID do Curso: ")

        cursor.execute("INSERT INTO alunos (nomeAluno, nomeUsuario, senha, cursoID) VALUES (?, ?, ?, ?)", (nome, usuario, senhaHash, cursoID))
        conn.commit()

    elif escolha == 2:

        cursor.execute("INSERT INTO professores (nomeProfessor, nomeUsuario, senha) VALUES (?, ?, ?)", (nome, usuario, senhaHash))
        conn.commit()

    print("Usuário cadastrado com sucesso!")
    
# Função para autenticar usuário
def verifica_usuario(escolha):
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    senhaHash = hashlib.sha256(senha.encode()).hexdigest()

    if escolha == 1:
        cursor.execute("SELECT * FROM alunos WHERE nomeUsuario = ? AND senha = ?", (usuario, senhaHash))

    elif escolha == 2:
        cursor.execute("SELECT * FROM professores WHERE nomeUsuario = ? AND senha = ?", (usuario, senhaHash))

    resultado = cursor.fetchone()
    
    if resultado:
        print("Usuário autenticado:", usuario)
        return resultado
    else:
        print("Usuário ou senha incorretos.")
        return None


## Chamadas de funções
cadastrar_usuario(1)

verifica_usuario(1)

