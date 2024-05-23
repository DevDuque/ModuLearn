import sqlite3
import hashlib

# Documento responsável pelo login de aluno


# Conexão com o Banco de Dados
conn = sqlite3.connect('ModuLearn.db')
cursor = conn.cursor()

# Função para cadastro de usuário no BD
def cadastrar_usuario():

    nome = input("Nome: ")
    usuario = input("usuario: ")
    senha = input("Senha: ")

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    cursor.execute("INSERT INTO alunos (nomeAluno, nomeUsuario, senha) VALUES (?, ?, ?)", (nome, usuario, senha_hash))
    conn.commit()
    print("Usuário cadastrado com sucesso!")
    
# Função para autenticar o usuário
def verifica_usuario():

    usuario = input("usuario: ")
    senha = input("Senha: ")

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    cursor.execute("SELECT * FROM alunos WHERE nomeUsuario = ? AND senha = ?", (usuario, senha_hash))

    if usuario:
        print("Usuário autenticado:", usuario)
    else:
        print("Usuário ou senha incorretos.")

    return cursor.fetchone()



verifica_usuario()

