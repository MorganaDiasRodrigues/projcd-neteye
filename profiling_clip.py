from ydata_profiling import ProfileReport
import pandas as pd

# Substitua 'seu_arquivo.csv' pelo caminho para o seu arquivo CSV
df = pd.read_csv('image_text_similarity_results.csv')

# Crie o relatório
profile = ProfileReport(df, title="Relatório de Profiling", explorative=True)

# Salve o relatório em um arquivo HTML
profile.to_file("clip_relatorio_profiling.html")
