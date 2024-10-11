"""Script para extrair estatísticas de imagens de um banco de dados SQL Server e gerar um relatório de profiling."""
import pyodbc
import pandas as pd
from ydata_profiling import ProfileReport

# Parte onde você conecta no banco SQL Server que você criou
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

    try:
        connection = pyodbc.connect(connection_string)
        print("Conexão bem-sucedida!")
        
        table_name = 'fALERTAS_SEGURANCA'

        # Criação do cursor
        cursor = connection.cursor()
        #query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'"
        query = f"SELECT * FROM {database}.bi.{table_name}"
        df = pd.read_sql(query, connection)

        print(table_name)
        print(df)
        print(df.info())
        cols_to_convert = ['DT_ACESSO', 'TP_ALERTA', 'DS_TITULO','DS_ALERTA','SQ_USUARIO','SQ_ESTACAO','NM_ARQUIVO','NM_DOMINIO']
        df[cols_to_convert] = df[cols_to_convert].astype(str)
        print(df.info())

        # Gerar o relatório de profiling para o DataFrame selecionado
        try:
            profile = ProfileReport(df, title=f"Relatório {table_name}", explorative=True)
            profile.to_file(f"reports/{table_name}_report.html")
            print(f"Relatório gerado com sucesso.")
        except Exception as e:
            print(f"Erro ao processar relatório: {e}")

    except Exception as e:
        print(f"Erro ao processar a tabela {table_name}: {e}")

except Exception as e:
        print(f"Erro ao processar: {e}")

finally:
    # Fechar conexão
    if 'connection' in locals():
        connection.close()
        print("Conexão fechada.")

