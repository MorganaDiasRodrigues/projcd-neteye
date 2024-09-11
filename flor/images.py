import pandas as pd
import numpy as np
from PIL import Image
import io

import traceback

from ydata_profiling import ProfileReport

import pyodbc

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
    
    tabela = 'ALERTAS'

    query  = f"SELECT * FROM {database}.dbo.{tabela}"

    df = pd.read_sql(query, connection)

    # Função para extrair as estatísticas de uma imagem
    def extrair_estatisticas_imagem(imagem):

        imagem = Image.open(io.BytesIO(imagem))

        # Obter o tamanho (largura e altura)
        largura, altura = imagem.size
        
        # Obter o histograma
        histograma = np.array(imagem.histogram())
        
        # Dividir histograma em 3 canais (R, G, B)
        r_hist = histograma[0:256]
        g_hist = histograma[256:512]
        b_hist = histograma[512:768]
        
        # Cálculo de estatísticas adicionais: média e desvio padrão das cores
        media_r = np.mean(r_hist)
        media_g = np.mean(g_hist)
        media_b = np.mean(b_hist)
        
        desvio_r = np.std(r_hist)
        desvio_g = np.std(g_hist)
        desvio_b = np.std(b_hist)
        
        # Retornar um dicionário com as informações extraídas
        return {
            'pixels' : altura*largura,
            'media_r': media_r,
            'media_g': media_g,
            'media_b': media_b,
            'desvio_r': desvio_r,
            'desvio_g': desvio_g,
            'desvio_b': desvio_b
        }

    df = df[df["ARQUIVO"].notnull()]

    # Aplicar a função a cada imagem e manter o ID
    estatisticas = df[['ID', 'ARQUIVO', 'AUX']].copy()
    estatisticas = estatisticas.set_index('ID')['ARQUIVO'].apply(extrair_estatisticas_imagem)
    estatisticas_df = pd.DataFrame(estatisticas.tolist(), index=estatisticas.index)

    print(estatisticas_df.head())

    # Fazer merge dos resultados com o DataFrame original
    df = pd.merge(df, estatisticas_df, left_on='ID', right_index=True)

    print(df.info())

    estatisticas_df = df[['ID', 'ARQUIVO', 'pixels', 'AUX']]

    # salvar df em um csv
    estatisticas_df.to_csv('images.csv', index=False)

    try:
        # Gerar o relatório de profiling para o DataFrame
        profile = ProfileReport(df, title=f"Relatório da tabela {tabela}", explorative=True)
        profile.to_file(f"{tabela}_images_report.html")
        print(f"Relatório da tabela {tabela} gerado com sucesso.")
    except Exception as e:
        print("Erro ao gerar o relatório de profiling:")
        print(e)
        traceback.print_exc()

    
except Exception as e:
    try:
        print("erro 1")
        query = f"SELECT * FROM {database}.bi.{tabela}"
        df = pd.read_sql(query, connection)
    except Exception as e:
        try:
            query = f"SELECT * FROM {database}.bi.{tabela}"
            df = pd.read_sql(query, connection)

            print("aqui")
            
        except Exception as inner_e:
            print(f"Erro ao processar a tabela {tabela}: {inner_e}")
            pass
