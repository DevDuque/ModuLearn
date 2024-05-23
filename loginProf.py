# Documento responsável pelo login de professores

conn = sqlite3.connect('ModuLearn.db')
cursor = conn.cursor()

# Função para cadastro de professores no banco de dados
def cadastrar_professor()