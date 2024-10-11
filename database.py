import pyodbc
import pandas as pd

server = '45.7.171.233,51433'
database = 'neteye_pucrs_full'
username = 'neteye_pucrs'
password = '1goE$6G^3Ng6!dKZ'

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
    
    # Consulta para listar todas as tabelas
    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG = ?"
    
    # Executar a consulta
    df = pd.read_sql(query, connection, params=[database])
    print(df['TABLE_NAME']=='ALERTAS')
except pyodbc.Error as e:
    print("Erro ao conectar ao banco de dados:", e)