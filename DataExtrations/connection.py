import pyodbc

def connect():
    server = '45.7.171.233,51433'  # ou o endereço IP do servidor SQL Server
    database = 'neteye_pucrs_full'   # nome do banco de dados restaurado
    username = 'neteye_pucrs'       # nome de usuário do SQL Server
    password = '1goE$6G^3Ng6!dKZ'  # senha do usuário


    # String de conexão
    connection_string = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'TrustServerCertificate=yes;'
    )

    try:
        # Estabelecer conexão com o banco de dados
        connection = pyodbc.connect(connection_string)
        print("Conexão bem-sucedida!")

    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)

    return connection