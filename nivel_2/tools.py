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