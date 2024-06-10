from bson import ObjectId
from pymongo import MongoClient
import hashlib

# Conexão com o MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ModuLearn']

# Criando índices para garantir a unicidade dos campos necessários
db.alunos.create_index('alunoID', unique=True)
db.professores.create_index('professorID', unique=True)
db.administradores.create_index('adminID', unique=True)

# Função para cadastro de usuário no BD
def cadastrar_usuario(escolha):
    nome = input("Nome: ")
    usuario = input("Nome de Usuário: ")
    senha = input("Senha: ")

    senhaHash = hashlib.sha256(senha.encode()).hexdigest()

    if escolha == 1:  # Aluno
        aluno_id = str(ObjectId())

        db.alunos.insert_one({
            'alunoID': aluno_id,
            'nomeAluno': nome,
            'nomeUsuario': usuario,
            'senha': senhaHash,
            'cursoID': None  # Inicialmente, sem curso
        })

    elif escolha == 2:  # Professor
        professor_id = str(ObjectId())
        
        db.professores.insert_one({
            'professorID': professor_id,
            'nomeProfessor': nome,
            'nomeUsuario': usuario,
            'senha': senhaHash
        })

    elif escolha == 3:  # Administrador
        admin_id = str(ObjectId())

        db.administradores.insert_one({
            'adminID': admin_id,
            'nomeAdmin': nome,
            'nomeUsuario': usuario,
            'senha': senhaHash
        })

    print("Usuário cadastrado com sucesso!")

# Função para autenticar usuário
def verifica_usuario():
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    senhaHash = hashlib.sha256(senha.encode()).hexdigest()

    aluno = db.alunos.find_one({'nomeUsuario': usuario, 'senha': senhaHash})
    professor = db.professores.find_one({'nomeUsuario': usuario, 'senha': senhaHash})
    admin = db.administradores.find_one({'nomeUsuario': usuario, 'senha': senhaHash})

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
            curso = db.cursos.find_one({'_id': 0, 'cursoID': aluno['cursoID']})
            print("Cursos nos quais está registrado:", curso)

        elif escolha == 2:
            cursos = db.cursos.find({}, {'_id': 0, 'cursoID': 1, 'nomeCurso': 1}) 
            print("Cursos disponíveis:")
            for curso in cursos:
                print(curso)

            nome_curso = input("Digite o nome do curso para solicitar inscrição: ")
        
            curso = db.cursos.find_one({'nomeCurso': nome_curso})
            if curso:
                db.requisicoes.insert_one({
                    'alunoID': aluno['alunoID'],
                    'cursoID': curso['cursoID'],  # Usando o ID do curso encontrado
                    'status': 'pendente'
                })
                print("Solicitação enviada.")
            else:
                print("Curso não encontrado.")

        elif escolha == 3:
            novo_nome = input("Novo nome: ")
            nova_senha = input("Nova senha: ")
            nova_senha_hash = hashlib.sha256(nova_senha.encode()).hexdigest()

            db.alunos.update_one({'_id': aluno['_id']}, {'$set': {'nomeAluno': novo_nome, 'senha': nova_senha_hash}})
            print("Dados atualizados.")

        elif escolha == 4:
            db.alunos.delete_one({'_id': aluno['_id']})
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
            cursos = db.cursos.find({'professorID': professor['professorID']})
            print("Cursos que você é responsável:")
            for curso in cursos:
                print(curso)

        elif escolha == 2:
            cursos = db.cursos.find({'professorID': professor['_id']})
            print("Cursos que você é responsável:")
            for curso in cursos:
                print(curso)

            curso_id = input("Digite o ID do curso para ver alunos: ")
            curso = db.cursos.find_one({'cursoID': curso_id, 'professorID': professor['professorID']})
            if curso:
                alunos = db.alunos.find({'cursoID': curso_id})
                print("Alunos no curso:")
                for aluno in alunos:
                    print(aluno)
            else:
                print("Você não é responsável por este curso.")

        elif escolha == 3:
            requisicoes = db.requisicoes.find({'status': 'pendente'})
            if requisicoes:
                print("Requisições pendentes:")
                for requisicao in requisicoes:
                    aluno = db.alunos.find_one({'alunoID': requisicao['alunoID']})  # Corrigido para 'alunoID'
                    if aluno:
                        curso = db.cursos.find_one({'cursoID': requisicao['cursoID']})
                        if curso:
                            print(f"Requisição ID: {requisicao['_id']} - Aluno: {aluno['nomeAluno']} - Curso: {curso['nomeCurso']}")
                            decisao = input("Aceitar (A) ou Rejeitar (R) esta solicitação? ").upper()

                            if decisao == 'A':
                                db.requisicoes.update_one({'_id': requisicao['_id']}, {'$set': {'status': 'aceito'}})
                                db.alunos.update_one({'alunoID': requisicao['alunoID']}, {'$set': {'cursoID': requisicao['cursoID']}})

                            elif decisao == 'R':
                                db.requisicoes.update_one({'_id': requisicao['_id']}, {'$set': {'status': 'rejeitado'}})
                        else:
                            print("Curso não encontrado.")
                    else:
                        print("Aluno não encontrado.")
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
            professores = db.professores.find()
            for professor in professores:
                print(professor)

        elif escolha == 2:
            cursos = db.cursos.find()
            print("Todos os cursos:")
            for curso in cursos:
                print(curso)

        elif escolha == 3:
            curso_id = str(ObjectId())
            
            nome_curso = input("Nome do novo curso: ")
            duracao = int(input("Duração do curso (45, 60, 100): "))
            tipo = input("Tipo do curso (EAD ou Presencial): ")
            professor_id = input("ID do professor responsável pelo curso: ")

            db.cursos.insert_one({
                'cursoID': curso_id,
                'nomeCurso': nome_curso,
                'duracao': duracao,
                'professorID': professor_id,
                'tipo': tipo
            })
            print("Novo curso adicionado com sucesso!")


        elif escolha == 4:
            curso_id = input("Digite o ID do curso para editar: ")
            novo_nome = input("Novo nome do curso: ")

            db.cursos.update_one({'cursoID': curso_id}, {'$set': {'nomeCurso': novo_nome}})
            print("Nome do curso atualizado.")

        elif escolha == 5:
            curso_id = input("Digite o ID do curso para deletar: ")
            db.cursos.delete_one({'cursoID': curso_id})
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

