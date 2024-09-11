"""Script para extrair estatísticas de imagens de um banco de dados SQL Server e gerar um relatório de profiling."""
import pyodbc
import pandas as pd
from ydata_profiling import ProfileReport

# Parte onde você conecta no banco SQL Server que você criou
server = 'NOTEBOOK' 
database = "neteye_pucrs"


# String de conexão
connection_string = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
    'TrustServerCertificate=yes;'
)

try:
    # Estabelecer conexão com o banco de dados
    connection = pyodbc.connect(connection_string)
    print("Conexão bem-sucedida!")
    
    # Criação do cursor
    cursor = connection.cursor()

    # Buscar os nomes de todas as tabelas
    query_tables = """
    SELECT TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE = 'BASE TABLE' AND TABLE_CATALOG = ?
    """
    cursor.execute(query_tables, database)
    tables = cursor.fetchall()

    # Para cada tabela, faça a consulta e passe para pandas profiling
    for table in tables:
        table_name = table[0]
        try:
            connection = pyodbc.connect(connection_string)
            print("Conexão bem-sucedida!")
            
            # Criação do cursor
            cursor = connection.cursor()
            print(table_name)
            query = f"SELECT * FROM {database}.dbo.{table_name}"
            df = pd.read_sql(query, connection)
            
            # Gerar o relatório de profiling para o DataFrame
            profile = ProfileReport(df, title=f"Relatório da tabela {table_name}", explorative=True)
            profile.to_file(f"{table_name}_report.html")
            print(f"Relatório da tabela {table_name} gerado com sucesso.")

        except Exception as e:
            try:
                query = f"SELECT * FROM {database}.bi.{table_name}"
                df = pd.read_sql(query, connection)
                
                # Gerar o relatório de profiling para o DataFrame
                profile = ProfileReport(df, title=f"Relatório da tabela {table_name}", explorative=True)
                profile.to_file(f"tables_reports/{table_name}_report.html")
                print(f"Relatório da tabela {table_name} gerado com sucesso.")
            except Exception as inner_e:
                print(f"Erro ao processar a tabela {table_name}: {inner_e}")
                pass

finally:
    # Fechar conexão
    if 'connection' in locals():
        connection.close()
        print("Conexão fechada.")

