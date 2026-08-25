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

def listar_top_10_suspeitos(df, suspeitos_fracionamento):
    clientes_fracionamento = set(suspeitos_fracionamento.index.get_level_values("cliente_id"))
    clientes_valor_atipico = set(df[df["valor_atipico"] == True]["cliente_id"])
    
    todos_suspeitos = clientes_fracionamento | clientes_valor_atipico
    
    contagem_flags = {}
    for cliente in todos_suspeitos:
        flags = 0
        if cliente in clientes_fracionamento:
            flags += 1
        if cliente in clientes_valor_atipico:
            flags += 1
        contagem_flags[cliente] = flags
    
    top_10 = sorted(contagem_flags.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_10

top_10_suspeitos = listar_top_10_suspeitos(df, suspeitos_fracionamento)
print("Top 10 clientes mais sinalizados:")
for cliente, flags in top_10_suspeitos:
    print(f"{cliente}: sinalizado por {flags} regra(s)")

def ferramenta_historico_cliente(df, cliente_id):
    operacoes = df[df["cliente_id"] == cliente_id]
    return {
        "cliente": cliente_id,
        "total_operacoes": len(operacoes),
        "soma_total": float(operacoes["valor_brl"].sum()),
        "mediana": float(operacoes["valor_brl"].median())
    }

def ferramenta_operacoes_do_dia(df, cliente_id, data):
    operacoes = df[(df["cliente_id"] == cliente_id) & (df["data"] == data)]
    return {
        "cliente": cliente_id,
        "data": data,
        "quantidade": len(operacoes),
        "soma": float(operacoes["valor_brl"].sum())
    }

def ferramenta_perfil_por_canal(df, cliente_id):
    operacoes = df[df["cliente_id"] == cliente_id]
    contagem = operacoes["canal"].value_counts().to_dict()
    return {
        "cliente": cliente_id,
        "canais_usados": contagem
    }


# As 3 ferramentas abaixo sao o que o agente vai poder usar pra investigar
# um cliente sinalizado. Cada uma responde uma pergunta diferente sobre
# o comportamento do cliente.

teste = ferramenta_historico_cliente(df, "CLI-003")
print(teste)

teste2 = ferramenta_operacoes_do_dia(df, "CLI-003", "2026-05-02")
print(teste2)

teste3 = ferramenta_perfil_por_canal(df, "CLI-003")
print(teste3)