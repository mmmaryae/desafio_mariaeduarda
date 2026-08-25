import pandas as pd
import json

def carregar_dados():
    arquivo = open("../dados/dados_nivel_2.json")
    dados = json.load(arquivo)
    
    taxa_cambio = dados["taxa_cambio_usd_brl"]
    df = pd.DataFrame(dados["operacoes"])
    
    df = df.drop_duplicates()
    df["valor_brl"] = df["valor"].astype(float)
    df.loc[df["moeda"] == "USD", "valor_brl"] = df["valor"] * taxa_cambio
    
    return df

df = carregar_dados()
print(f"Total de operações: {len(df)}")
print(df.head())


def aplicar_regras(df):
    df_com_data = df[df["data"].notna()].copy()
    
    soma_por_cliente_dia = df_com_data.groupby(["cliente_id", "data"])["valor_brl"].sum()
    contagem_operacoes = df_com_data.groupby(["cliente_id", "data"])["id"].count()
    
    suspeitos_fracionamento = soma_por_cliente_dia[(soma_por_cliente_dia > 50000) & (contagem_operacoes > 1)]
    
    mediana_por_cliente = df.groupby("cliente_id")["valor_brl"].median()
    df["mediana_cliente"] = df["cliente_id"].map(mediana_por_cliente)
    df["valor_atipico"] = df["valor_brl"] > (df["mediana_cliente"] * 3)
    
    return df, suspeitos_fracionamento

df, suspeitos_fracionamento = aplicar_regras(df)
print("Clientes com fracionamento:")
print(suspeitos_fracionamento)
print("")
print("Operações com valor atípico:")
print(df[df["valor_atipico"] == True][["cliente_id", "valor_brl", "mediana_cliente"]])