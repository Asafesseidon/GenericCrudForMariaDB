import mariadb

# Author: Asafe Domingues Marcelino
# Main help: God
# Subhelper: Gemini to remember syntax and things like which function to call to acces the DB_HOST

# Informações do Banco

DB_HOST = 'localhost'
DB_NAME = 'tenochi'
DB_USER = 'tenochi'
DB_PASS = 'tenochi'
DB_PORT = 3305

# Variaveís iniciais

sistema = True;

conn=None

# Funções

def connectDB():
    global conn
    
    try:
        conn = mariadb.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
            )
        print("500")
        
    except mariadb.Error as e:
        print(f"Erro ao conectar: {e}")

def getTable(params, table, query):
    if query and query.strip():
        query = f"WHERE {query}"
    
    else:
        query = ""
        
    cursor = conn.cursor(dictionary=True)
    
    try:
        resultados = cursor.execute(f"SELECT {params} FROM {table} {query}")
        
        if resultados:
            res = [True, cursor.fetchall()]
        
        else:
            res = [False, f"\nNenhum registro encontrado em {table}."]
    
    except mariadb.Error as e:
        # Se a query estiver errada (tabela não existe, etc), cai aqui em vez de quebrar o código
        res = [False, f"\nErro na busca em {table}: {e}"]
    
    cursor.close()
    
    return res

def getTableById(id, table):
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(f"SELECT * FROM {table} WHERE id = {id}")
    
    if cursor.fetchall():
        res = [True, cursor.fetchall()]
    
    else: 
        res = [False, f"\n{table} com id: {id} não existe"]
    
    cursor.close()
    
    return res

def insertTable(table, params):
    cursor = conn.cursor(dictionary=True)
    
    # Salva o resultado do split em uma lista, separando cada par de paramêtros e valores
    listaParams = params.split(",")
        
    insertParams = []
    insertValue = []
    
    # Itera sobre cada par de paramêtros e valores
    for parameter in listaParams:
        
        # Salva o resultado do split  em uma lista, separando cada paramêtro de cada valor correspondente
        partes = parameter.split("=")
            
        insertParams.append(partes[0].strip())
        insertValue.append(partes[1].strip())
        
    try:
        cursor.execute(f"SELECT id FROM {table} WHERE {params}")
        
        if cursor.fetchall():
            
            res = [False, f"\n{table} com esses paramêtros: [{', '.join(insertParams)}] já existe"]
            
        else:
            
            cursor.execute(f"INSERT INTO {table}({', '.join(insertParams)}) Values({', '.join(insertValue)})")
            conn.commit()
            
            res = [True, f"\n{table} com os paramêtros: [{', '.join(insertParams)}]"]  
    
    except mariadb.Error as e:
        res = [False, f"\nNão foi possível criar na {table}: {e}"]
    
    cursor.close()
    
    return res
    
def updateTable(id, table, params):
    check = getTableById(id, table)
    
    if check[0] is True:
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"UPDATE {table} SET {params} WHERE id = {id}")
        
        res = [True, f"\n{table} com id: {id} foi atualizada"]
        conn.commit()
        
        cursor.close()
    else:
        res = check
    
    return res

def deleteTable(id, table):
    check = getTableById(id, table)
    
    if check[0] is True:
        
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM {table} WHERE id = {id}")
        
        conn.commit()
        res = [True, f"\n{table} com id:{id} foi deletado com sucesso"]
        
        cursor.close()
        
    else:
        res = check

    return res

def consultaSimples():
    # Busca de Registros no Banco
    busca = getTable("(id, Nome, info)", "Tabela1", "")
    
    if busca[0] is True:
        tabela = busca[1]
        
        registroEscolhido = -1        
        
        # Condição de loop
        consultando = True
                
        while consultando:
                
            print("\nEssas são os registros da tabela, qual escolherá?\n")
                    
            # Printa cada tabela pega na busca
            for i, registro in enumerate(tabela):
                print(f'{i} - Registro: {registro["Nome"]} - Id:{registro["id"]}')
        
            print(f"{len(tabela)} - Sair")
                    
            escolha = int(input());
                    
            # Caso a pessoa escolha sair da consulta
            if escolha == len(tabela):
                        
                # faz a condição do while principal falsa
                consultando = False
                        
            # Caso queira continuar
            else:
                
                for i, registro in enumerate(tabela):
                    # Compara o indice de cada tabela com a tabela escolhida pelo usuário 
                    if escolha == i:
                        print("\n", registro)
                        registroEscolhido = registro
                        
    
        res = [True, registroEscolhido]
    
    else:
        res = [False, f"\nHouve um problema no acesso a tabela"]
    
    return res

def newParameter(register):
    params = []
    
    for atributo, valor in register.items():
        if atributo.lower() == 'id':
            continue
        
        novo_valor = input(f"Novo {atributo}: ").strip()
        par_atributo_valor = f"{atributo} = '{novo_valor}'"
                        
        params.append(par_atributo_valor)
                        
    res = ", ".join(params)

    return res


# Sistema em si


while sistema:

    opcao = int(input("\nEscolha uma das operações \n 1 - Conectar-se ao banco \n 2 - Consulta \n 3 - Incluir \n 4 - Deletar \n 5 - Atualizar \n 6 - Sair \n"))
    
    # Conexão com o Banco
    if opcao == 1:
        connectDB();
    
    
    # Consulta
    elif opcao == 2:
        
        if conn:
            print(consultaSimples()[1])
            
        else:
            print("\nVocê não está conectado ao banco, conecte-se para consultar.")
            
    # Incluir    
    elif opcao == 3:
        
        if conn:

            busca = getTable("(id, Nome, info)", "Tabela1", "")
            
            if busca[0] is True:
                
                registro = busca[1][0]
                
                print("\nInsira os valores para cada paramêtro")
                
                params = newParameter(registro)
                
                print(insertTable("Tabela1", params))
        
            else: 
                print("\nHouve um problemas para pegar o formato de dados para requisitar o usuário, tente novamente.")
        
        
        else:
            print("\nVocê não está conectado ao banco, conecte-se para incluir.")

    # Deletar
    elif opcao == 4:
        
        if conn:
            registro = consultaSimples()
            
            if registro[0] is True:
                print(deleteTable(int(registro[1]["id"]), "Tabela1"))
                
            else: 
                print("\nHouve um problemas para pegar o formato de dados para requisitar o usuário, tente novamente.")
        
        
        else:
            print("\nVocê não está conectado ao banco, conecte-se para deletar.")

    # Atualizar
    elif opcao == 5:
        
        if conn:
            registro = consultaSimples()
            
            if registro[0] is True:
                
                print("\nInsira as novas informações")
                
                params = newParameter(registro[1])
                
                print(updateTable(int(registro[1]["id"]), "Tabela1", params))
            
            else: 
                print("\nHouve um problemas para pegar o formato de dados para requisitar o usuário, tente novamente.")
        
            
        else:
            print("\nVocê não está conectado ao banco, conecte-se para atualizar.")

    # Sair
    elif opcao == 6:
        print("\nObrigado por usar o programa\n")
        
        # Desconecta-se do Banco
        if conn:
            conn.close()
        
        # Faz a condição do while principal se tornar falsa
        sistema = False;
        
    else:
        print("\n Opção inválida, selecione uma das operações indicadas")
