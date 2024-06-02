import sqlite3
import hashlib
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
        cursor.execute("INSERT INTO alunos (nomeAluno, nomeUsuario, senha) VALUES (?, ?, ?)", (nome, usuario, senhaHash))

    elif escolha == 2:  # Professor
        cursor.execute("INSERT INTO professores (nomeProfessor, nomeUsuario, senha) VALUES (?, ?, ?)", (nome, usuario, senhaHash))

    elif escolha == 3:  # Administrador
        cursor.execute("INSERT INTO administradores (nomeAdmin, nomeUsuario, senha) VALUES (?, ?, ?)", (nome, usuario, senhaHash))

    conn.commit()
    print("Usuário cadastrado com sucesso!")

# Função para autenticar usuário
def verifica_usuario():
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    senhaHash = hashlib.sha256(senha.encode()).hexdigest()

    cursor.execute("SELECT * FROM alunos WHERE nomeUsuario = ? AND senha = ?", (usuario, senhaHash))
    aluno = cursor.fetchone()

    cursor.execute("SELECT * FROM professores WHERE nomeUsuario = ? AND senha = ?", (usuario, senhaHash))
    professor = cursor.fetchone()

    cursor.execute("SELECT * FROM administradores WHERE nomeUsuario = ? AND senha = ?", (usuario, senhaHash))
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
            cursor.execute("SELECT * FROM cursos WHERE cursoID = ?", (aluno[6],))

            cursos = cursor.fetchall()
            print("Cursos nos quais está registrado:", cursos)

        elif escolha == 2:
            cursor.execute("SELECT cursoID, nomeCurso FROM cursos")
            cursos = cursor.fetchall()

            print("Cursos disponíveis:")
            for curso in cursos:
                print(curso)

            curso_id = int(input("Digite o ID do curso para solicitar inscrição: "))

            cursor.execute("INSERT INTO requisicoes (alunoID, cursoID, status) VALUES (?, ?, 'pendente')", (aluno[0], curso_id))
            
            conn.commit()
            print("Solicitação enviada.")

        elif escolha == 3:
            novo_nome = input("Novo nome: ")
            nova_senha = input("Nova senha: ")

            nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()
            cursor.execute("UPDATE alunos SET nomeAluno = ?, senha = ? WHERE alunoID = ?", (novo_nome, nova_senha_hash, aluno[0]))

            conn.commit()
            print("Dados atualizados.")

        elif escolha == 4:
            cursor.execute("DELETE FROM alunos WHERE alunoID = ?", (aluno[0],))

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
        print("1. Ver todos os cursos")
        print("2. Selecionar curso e ver alunos")
        print("3. Ver e gerenciar requisições")
        print("4. Sair")
        escolha = int(input("Escolha uma opção: "))

        if escolha == 1:
            cursor.execute("SELECT * FROM cursos")
            cursos = cursor.fetchall()
            print("Todos os cursos:", cursos)

        elif escolha == 2:
            curso_id = int(input("Digite o ID do curso para ver alunos: "))
            cursor.execute("SELECT * FROM alunos WHERE cursoID = ?", (curso_id,))
            
            alunos = cursor.fetchall()

            print("Alunos no curso:", alunos)

            cursor.execute("SELECT * FROM modulos WHERE cursoID = ?", (curso_id,))
            modulos = cursor.fetchall()

            print("Módulos do curso:", modulos)

        elif escolha == 3:
            cursor.execute("SELECT * FROM requisicoes WHERE status = 'pendente'")
            requisicoes = cursor.fetchall()

            if requisicoes:
                print("Requisições pendentes:", requisicoes)
                for requisicao in requisicoes:
                    aluno_id, curso_id = requisicao[1], requisicao[2]

                    cursor.execute("SELECT nomeAluno FROM alunos WHERE alunoID = ?", (aluno_id,))
                    aluno_nome = cursor.fetchone()[0]

                    cursor.execute("SELECT nomeCurso FROM cursos WHERE cursoID = ?", (curso_id,))
                    curso_nome = cursor.fetchone()[0]

                    print(f"Requisição ID: {requisicao[0]} - Aluno: {aluno_nome} - Curso: {curso_nome}")

                    decisao = input("Aceitar (A) ou Rejeitar (R) esta solicitação? ").upper()
                    if decisao == 'A':
                        cursor.execute("UPDATE requisicoes SET status = 'aceito' WHERE requisicaoID = ?", (requisicao[0],))
                        cursor.execute("UPDATE alunos SET cursoID = ? WHERE alunoID = ?", (curso_id, aluno_id))

                    elif decisao == 'R':
                        cursor.execute("UPDATE requisicoes SET status = 'rejeitado' WHERE requisicaoID = ?", (requisicao[0],))

                    conn.commit()
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
        print("1. Ver todos os cursos com o professor responsável")
        print("2. Adicionar novo curso")
        print("3. Visualizar curso")
        print("4. Editar curso")
        print("5. Deletar curso")
        print("6. Sair")
        escolha = int(input("Escolha uma opção: "))

        if escolha == 1:
            cursor.execute("SELECT cursos.*, professores.nomeProfessor FROM cursos INNER JOIN professores ON cursos.professorID = professores.professorID")

            cursos = cursor.fetchall()

            print("Cursos com professor responsável:")
            for curso in cursos:
                print(curso)

        elif escolha == 2:
            nome_curso = input("Nome do novo curso: ")

            duracao = int(input("Duração do curso (45, 60, 100): "))

            tipo = input("Tipo do curso (EAD ou Presencial): ")

            professor_id = int(input("ID do professor responsável pelo curso: "))

            cursor.execute("INSERT INTO cursos (nomeCurso, duracao, professorID, tipo) VALUES (?, ?, ?, ?)", (nome_curso, duracao, professor_id, tipo))

            conn.commit()
            print("Novo curso adicionado com sucesso!")

        elif escolha == 3:
            curso_id = int(input("Digite o ID do curso para visualizar: "))
            cursor.execute("SELECT * FROM cursos WHERE cursoID = ?", (curso_id,))

            curso = cursor.fetchone()

            print("Detalhes do curso:")
            print(curso)

        elif escolha == 4:
            curso_id = int(input("Digite o ID do curso para editar: "))
            novo_nome = input("Novo nome do curso: ")

            cursor.execute("UPDATE cursos SET nomeCurso = ? WHERE cursoID = ?", (novo_nome, curso_id))

            conn.commit()
            print("Nome do curso atualizado.")

        elif escolha == 5:
            curso_id = int(input("Digite o ID do curso para deletar: "))

            cursor.execute("DELETE FROM cursos WHERE cursoID = ?", (curso_id,))

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