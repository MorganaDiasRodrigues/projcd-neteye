import pandas as pd
import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import io
import pyodbc
from sqlalchemy import create_engine

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
    # Estabelecer conexão com o banco de dados
    connection = pyodbc.connect(connection_string)
    print("Conexão bem-sucedida!")
    
    tabela = 'ALERTAS'

    query  = f"SELECT * FROM {database}.dbo.{tabela}"

    df = pd.read_sql(query, connection)

    df = df[df["ARQUIVO"].notnull()]

    # Configuração do dispositivo (GPU ou CPU)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Carregar o modelo CLIP e o processador
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    # Função para processar uma imagem a partir do caminho no DataFrame
    def process_row(row):
        try:
            image_bytes = row['ARQUIVO']  # Dados binários diretamente
            image = Image.open(io.BytesIO(image_bytes))

            inputs = processor(text=[row['AUX']], images=image, return_tensors="pt", padding=True)
            inputs = inputs.to(device)

            with torch.no_grad():
                outputs = model(**inputs)

            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)
            return probs.cpu().numpy()
        except Exception as e:
            print(f"Erro ao processar a linha: {e}")
            return None

    # Aplicar o processamento para cada linha do DataFrame
    df['probs'] = df.apply(process_row, axis=1)

    # Filtrar as colunas de interesse para exibir os resultados
    df = df[['ID', 'AUX', 'probs']]

    # Salvar o DataFrame com os resultados em um novo arquivo CSV, se necessário
    df.to_csv("clip_results.csv", index=False)
    print('Aqui')

except Exception as e:
    print(f"Erro ao conectar ao banco de dados ou processar os dados: {e}")
