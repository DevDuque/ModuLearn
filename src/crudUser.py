import sqlite3
import hashlib
from uuid import uuid4

import criaTabela

# Criando as tabelas antes de executar o CRUD
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

    if escolha == 1:  # Aluno
        aluno_id = str(uuid4())

        cursor.execute('''
            INSERT INTO alunos (alunoID, nomeAluno, nomeUsuario, senha, cursoID)
            VALUES (?, ?, ?, ?, ?)
        ''', (aluno_id, nome, usuario, senhaHash, None))
        
    elif escolha == 2:  # Professor
        professor_id = str(uuid4())

        cursor.execute('''
            INSERT INTO professores (professorID, nomeProfessor, nomeUsuario, senha)
            VALUES (?, ?, ?, ?)
        ''', (professor_id, nome, usuario, senhaHash))

    elif escolha == 3:  # Administrador
        admin_id = str(uuid4())

        cursor.execute('''
            INSERT INTO administradores (adminID, nomeAdmin, nomeUsuario, senha)
            VALUES (?, ?, ?, ?)
        ''', (admin_id, nome, usuario, senhaHash))

    conn.commit()
    print("Usuário cadastrado com sucesso!")

# Função para autenticar usuário
def verifica_usuario():
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    senhaHash = hashlib.sha256(senha.encode()).hexdigest()

    cursor.execute('''
        SELECT * FROM alunos WHERE nomeUsuario = ? AND senha = ?
    ''', (usuario, senhaHash))
    aluno = cursor.fetchone()

    cursor.execute('''
        SELECT * FROM professores WHERE nomeUsuario = ? AND senha = ?
    ''', (usuario, senhaHash))
    professor = cursor.fetchone()

    cursor.execute('''
        SELECT * FROM administradores WHERE nomeUsuario = ? AND senha = ?
    ''', (usuario, senhaHash))
    admin = cursor.fetchone()

    if aluno:
        print("Aluno autenticado:", usuario)
        return 'aluno', aluno

    elif professor:
        print("Professor autenticado:", usuario)
        return 'professor', professor

    elif admin:
        print("Administrador autenticado:", usuario)
        return 'admin', admin

    else:
        print("Usuário ou senha incorretos.")
        return None, None

# Funções específicas para alunos
def aluno_menu(aluno):
    while True:
        print("\nMenu do Aluno:")
        print("1. Ver dados dos cursos que está cadastrado")
        print("2. Ver cursos disponíveis e solicitar inscrição")
        print("3. Editar dados")
        print("4. Deletar conta")
        print("5. Sair")
        escolha = int(input("Escolha uma opção: "))

        if escolha == 1:
            cursor.execute('''
                SELECT * FROM cursos WHERE cursoID = ?
            ''', (aluno[6],))  # aluno[6] é cursoID
            curso = cursor.fetchone()
            print("Cursos nos quais está registrado:", curso)

        elif escolha == 2:
            cursor.execute('''
                SELECT cursoID, nomeCurso FROM cursos
            ''')
            cursos = cursor.fetchall()
            print("Cursos disponíveis:")
            for curso in cursos:
                print(curso)

            nome_curso = input("Digite o nome do curso para solicitar inscrição: ")
        
            cursor.execute('''
                SELECT cursoID FROM cursos WHERE nomeCurso = ?
            ''', (nome_curso,))
            curso = cursor.fetchone()
            if curso:
                requisicao_id = str(uuid4())
                cursor.execute('''
                    INSERT INTO requisicoes (requisicaoID, alunoID, cursoID, status)
                    VALUES (?, ?, ?, ?)
                ''', (requisicao_id, aluno[0], curso[0], 'pendente'))
                conn.commit()
                print("Solicitação enviada.")
            else:
                print("Curso não encontrado.")

        elif escolha == 3:
            novo_nome = input("Novo nome: ")
            nova_senha = input("Nova senha: ")
            nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()

            cursor.execute('''
                UPDATE alunos
                SET nomeAluno = ?, senha = ?
                WHERE alunoID = ?
            ''', (novo_nome, nova_senha_hash, aluno[0]))  # aluno[0] é alunoID
            conn.commit()
            print("Dados atualizados.")

        elif escolha == 4:
            cursor.execute('''
                DELETE FROM alunos WHERE alunoID = ?
            ''', (aluno[0],))  # aluno[0] é alunoID
            conn.commit()
            print("Conta deletada.")
            break

        elif escolha == 5:
            break

        else:
            print("Opção inválida.")

# Funções específicas para professores
def professor_menu(professor):
    while True:
        print("\nMenu do Professor:")
        print("1. Visualizar cursos que é responsável")
        print("2. Selecionar curso e ver alunos")
        print("3. Ver e gerenciar requisições")
        print("4. Sair")
        escolha = int(input("Escolha uma opção: "))

        if escolha == 1:
            cursor.execute('''
                SELECT * FROM cursos WHERE professorID = ?
            ''', (professor[0],))  # professor[0] é professorID
            cursos = cursor.fetchall()
            print("Cursos que você é responsável:")
            for curso in cursos:
                print(curso)

        elif escolha == 2:
            cursor.execute('''
                SELECT cursoID, nomeCurso FROM cursos WHERE professorID = ?
            ''', (professor[0],))  # professor[0] é professorID
            cursos = cursor.fetchall()
            print("Cursos que você é responsável:")
            for curso in cursos:
                print(curso)

            curso_id = input("Digite o ID do curso para ver alunos: ")
            cursor.execute('''
                SELECT * FROM cursos WHERE cursoID = ? AND professorID = ?
            ''', (curso_id, professor[0]))  # professor[0] é professorID
            curso = cursor.fetchone()
            if curso:
                cursor.execute('''
                    SELECT * FROM alunos WHERE cursoID = ?
                ''', (curso_id,))
                alunos = cursor.fetchall()
                print("Alunos no curso:")
                for aluno in alunos:
                    print(aluno)
            else:
                print("Você não é responsável por este curso.")

        elif escolha == 3:
            cursor.execute('''
                SELECT * FROM requisicoes WHERE status = 'pendente'
            ''')
            requisicoes = cursor.fetchall()
            if requisicoes:
                print("Requisições pendentes:")
                for requisicao in requisicoes:
                    cursor.execute('''
                        SELECT nomeAluno FROM alunos WHERE alunoID = ?
                    ''', (requisicao[1],))  # requisicao[1] é alunoID
                    aluno = cursor.fetchone()
                    cursor.execute('''
                        SELECT nomeCurso FROM cursos WHERE cursoID = ?
                    ''', (requisicao[2],))  # requisicao[2] é cursoID
                    curso = cursor.fetchone()
                    if aluno and curso:
                        print(f"Requisição ID: {requisicao[0]} - Aluno: {aluno[0]} - Curso: {curso[0]}")
                        decisao = input("Aceitar (A) ou Rejeitar (R) esta solicitação? ").upper()

                        if decisao == 'A':
                            cursor.execute('''
                                UPDATE requisicoes
                                SET status = 'aceito'
                                WHERE requisicaoID = ?
                            ''', (requisicao[0],))  # requisicao[0] é requisicaoID
                            cursor.execute('''
                                UPDATE alunos
                                SET cursoID = ?
                                WHERE alunoID = ?
                            ''', (requisicao[2], requisicao[1]))  # requisicao[2] é cursoID, requisicao[1] é alunoID

                        elif decisao == 'R':
                            cursor.execute('''
                                UPDATE requisicoes
                                SET status = 'rejeitado'
                                WHERE requisicaoID = ?
                            ''', (requisicao[0],))  # requisicao[0] é requisicaoID
                        conn.commit()
                    else:
                        print("Aluno ou curso não encontrado.")
            else:
                print("Não há requisições pendentes.")

        elif escolha == 4:
            break

        else:
            print("Opção inválida.")

# Funções específicas para administradores
def admin_menu(admin):
    while True:
        print("\nMenu do Administrador:")
        print("1. Ver todos os professores")
        print("2. Visualizar cursos")
        print("3. Adicionar novo curso")
        print("4. Editar curso")
        print("5. Deletar curso")
        print("6. Sair")
        escolha = int(input("Escolha uma opção: "))

        if escolha == 1:
            print("Professores ativos no banco:")
            cursor.execute('''
                SELECT * FROM professores
            ''')
            professores = cursor.fetchall()
            for professor in professores:
                print(professor)

        elif escolha == 2:
            cursor.execute('''
                SELECT * FROM cursos
            ''')
            cursos = cursor.fetchall()
            print("Todos os cursos:")
            for curso in cursos:
                print(curso)

        elif escolha == 3:
            curso_id = str(uuid4())
            nome_curso = input("Nome do novo curso: ")
            duracao = int(input("Duração do curso (45, 60, 100): "))
            tipo = input("Tipo do curso (EAD ou Presencial): ")
            professor_id = input("ID do professor responsável pelo curso: ")

            cursor.execute('''
                INSERT INTO cursos (cursoID, nomeCurso, duracao, professorID, tipo)
                VALUES (?, ?, ?, ?, ?)
            ''', (curso_id, nome_curso, duracao, professor_id, tipo))
            conn.commit()
            print("Novo curso adicionado com sucesso!")

        elif escolha == 4:
            curso_id = input("Digite o ID do curso para editar: ")
            novo_nome = input("Novo nome do curso: ")

            cursor.execute('''
                UPDATE cursos
                SET nomeCurso = ?
                WHERE cursoID = ?
            ''', (novo_nome, curso_id))
            conn.commit()
            print("Nome do curso atualizado.")

        elif escolha == 5:
            curso_id = input("Digite o ID do curso para deletar: ")
            cursor.execute('''
                DELETE FROM cursos WHERE cursoID = ?
            ''', (curso_id,))
            conn.commit()
            print("Curso deletado com sucesso.")

        elif escolha == 6:
            break

        else:
            print("Opção inválida.")

# Função do menu principal
def menu_principal():
    while True:
        print("\nMenu Principal:")
        print("1. Criar conta")
        print("2. Logar")
        print("3. Sair")
        escolha = int(input("Escolha uma opção: "))

        if escolha == 1:
            # Para cadastrar usuário
            escolha = int(input("Escolha o tipo de usuário para cadastrar (1: Aluno, 2: Professor, 3: Administrador): "))
            cadastrar_usuario(escolha)

        elif escolha == 2:
            # Para autenticar usuário
            tipo_usuario, usuario = verifica_usuario()

            # Chamar o menu apropriado baseado no tipo de usuário
            if tipo_usuario == 'aluno':
                aluno_menu(usuario)

            elif tipo_usuario == 'professor':
                professor_menu(usuario)
                
            elif tipo_usuario == 'admin':
                admin_menu(usuario)

        elif escolha == 3:
            break

        else:
            print("Opção inválida.")

# Chamada da função do menu principal
menu_principal()
conn.close()