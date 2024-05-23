import sqlite3
import hashlib

import criaTabela

# Documento responsável pelo login de professores

conn = sqlite3.connect('ModuLearn.db')
cursor = conn.cursor()

# Função para cadastro de professores no banco de dados
def cadastrar_professor():
    nomeProfessor = input("Entre o seu nome: ")
    nomeUsuario = input("Entre o nome de usuário: ")
    senha = input("Entre a senha: ")
    
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    cursor.execute("INSERT INTO professores (nomeProfessor, nomeUsuario, senha) VALUES (?, ?, ?)", (nomeProfessor, nomeUsuario, senha_hash))
    conn.commit()

# Função para autenticar o professor
def verificar_cadastro():
    nomeUsuario = input("Entre o nome de usuário: ")
    senha = input("Entre a senha: ")

    senha_hash = hashlib.sha256(senha.encode()).hexdigest()

    cursor.execute("SELECT * FROM usuarios WHERE nomeUsuario ? AND senha = ?", (nomeUsuario, senha_hash))
    return cursor.fetchone()