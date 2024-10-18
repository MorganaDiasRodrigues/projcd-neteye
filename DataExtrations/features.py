import pandas as pd

def total_de_horas_trabalhadas(bi_sessoes):
    bi_sessoes['HORAS_TOTAIS'] = bi_sessoes['QT_SEGUNDOS'] / 3600
    return bi_sessoes

def dia_da_semana(bi_sessoes):
    bi_sessoes['DIA_SEMANA'] = pd.to_datetime(bi_sessoes['LOGIN']).dt.strftime('%A')
    return bi_sessoes

def transactions(df):

    df['group'] = (df['ID_STATUS_PROGRAMA'] != df['ID_STATUS_PROGRAMA'].shift()).cumsum()

    df = df.groupby(['group', 'ID_STATUS_PROGRAMA']).apply(
        lambda x: pd.Series({
            'DT_ACESSO': x['DT_ACESSO'].iloc[0],  # Taking the first date for the group
            'NM_PROGRAMA': ', '.join(x['NM_PROGRAMA']),  # Joining program names in the group
            'QT_MINUTO': x['QT_MINUTO'].sum(),  # Summing minutes
            'ID_STATUS_PROGRAMA': x['ID_STATUS_PROGRAMA'].iloc[0]  # Keeping the status
        })
    ).reset_index(drop=True)

    df['NEXT_STATUS'] = df['ID_STATUS_PROGRAMA'].shift(-1)
    df['NEXT_QT_MINUTO'] = df['QT_MINUTO'].shift(-1)

    df = df.dropna(subset=['NEXT_STATUS'])

    df['TRANSITION'] = df['ID_STATUS_PROGRAMA'].astype(str) + ' to ' + df['NEXT_STATUS'].astype(str)

    df['DURATION'] = df['QT_MINUTO']

    return df.groupby(['DT_ACESSO', 'TRANSITION'])['DURATION'].mean().unstack(fill_value=0)

def numero_de_programas():
    ...