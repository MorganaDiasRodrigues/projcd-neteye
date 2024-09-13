import pandas as pd

# Carregar o DataFrame
df = pd.read_csv('images.csv')

# Verificar os nomes das colunas
print(df.columns)

# Iterar sobre as linhas do DataFrame
for index, row in df.iterrows():
    img_bytes = eval(row['ARQUIVO'])  # 'eval' converte a string de bytes para bytes reais
    aux_value = row['AUX'].strip()
        # Passo 3: Salvar a imagem
    with open(f'C:\\Users\\Dell\\OneDrive - PUCRS - BR\\7 Semestre 2024-2\\8 Projeto em Ciência de Dados I\\Projeto NetEye\\dados\\images\\img_{index+1}_{aux_value}.png', 'wb') as img_file:
        img_file.write(img_bytes)

print("Imagens convertidas e salvas.")
