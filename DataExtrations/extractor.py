import pandas as pd
from connection import connect

def get_data_from_user_id(user_id:str) -> dict:
    connection = connect()
    query = f"""SELECT * FROM bi.fPRODUTIVIDADE WHERE SQ_USUARIO={user_id}"""
    bi_produtividade = pd.read_sql(query, connection).to_dict()

    query = f"""SELECT * FROM bi.fSESSOES WHERE SQ_USUARIO={user_id}"""
    bi_sessoes = pd.read_sql(query, connection).to_dict()

    return {"bi_produtividade":bi_produtividade, 
            "bi_sessoes":bi_sessoes}

