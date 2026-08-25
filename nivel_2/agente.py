import requests
import os
import json
import time
from dotenv import load_dotenv
from tools import carregar_dados, aplicar_regras, ferramenta_historico_cliente, ferramenta_operacoes_do_dia, ferramenta_perfil_por_canal

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

df = carregar_dados()
df, suspeitos_fracionamento = aplicar_regras(df)

print("Ferramentas e dados carregados com sucesso")


ferramentas_disponiveis = [
    {
        "type": "function",
        "function": {
            "name": "historico_cliente",
            "description": "Retorna o historico geral de um cliente: total de operacoes, soma total e mediana",
            "parameters": {
                "type": "object",
                "properties": {
                    "cliente_id": {"type": "string", "description": "ID do cliente, ex: CLI-003"}
                },
                "required": ["cliente_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "operacoes_do_dia",
            "description": "Retorna as operacoes de um cliente em um dia especifico",
            "parameters": {
                "type": "object",
                "properties": {
                    "cliente_id": {"type": "string"},
                    "data": {"type": "string", "description": "Data no formato AAAA-MM-DD"}
                },
                "required": ["cliente_id", "data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "perfil_por_canal",
            "description": "Retorna quantas operacoes o cliente fez em cada canal (pix, ted, boleto, etc)",
            "parameters": {
                "type": "object",
                "properties": {
                    "cliente_id": {"type": "string"}
                },
                "required": ["cliente_id"]
            }
        }
    }
]

print("Ferramentas descritas com sucesso")


url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}"}


def executar_ferramenta(nome_ferramenta, argumentos):
    args = json.loads(argumentos)
    if nome_ferramenta == "historico_cliente":
        return ferramenta_historico_cliente(df, args["cliente_id"])
    elif nome_ferramenta == "operacoes_do_dia":
        return ferramenta_operacoes_do_dia(df, args["cliente_id"], args["data"])
    elif nome_ferramenta == "perfil_por_canal":
        return ferramenta_perfil_por_canal(df, args["cliente_id"])


def investigar_e_salvar(cliente_id, motivo_sinalizacao):
    mensagens = [
        {"role": "user", "content": f"O cliente {cliente_id} foi sinalizado como suspeito pelo seguinte motivo: {motivo_sinalizacao}. Use as ferramentas disponiveis para investigar o comportamento dele e depois de o parecer final."}
    ]
    tokens_totais = 0
    inicio = time.time()

    for rodada in range(5):
        corpo = {
            "model": "openai/gpt-oss-20b",
            "messages": mensagens,
            "tools": ferramentas_disponiveis
        }
        resposta = requests.post(url, headers=headers, json=corpo)
        resposta_json = resposta.json()
        tokens_totais += resposta_json.get("usage", {}).get("total_tokens", 0)
        mensagem_do_agente = resposta_json["choices"][0]["message"]

        if "tool_calls" not in mensagem_do_agente:
            tempo_total = time.time() - inicio
            return {
                "cliente_id": cliente_id,
                "motivo_sinalizacao": motivo_sinalizacao,
                "parecer_final": mensagem_do_agente["content"],
                "tokens_usados": tokens_totais,
                "tempo_segundos": round(tempo_total, 2)
            }

        chamada = mensagem_do_agente["tool_calls"][0]
        nome_ferramenta = chamada["function"]["name"]
        argumentos = chamada["function"]["arguments"]
        print(f"Rodada {rodada + 1}: agente pediu a ferramenta {nome_ferramenta}")
        resultado_ferramenta = executar_ferramenta(nome_ferramenta, argumentos)
        print("Resultado:", resultado_ferramenta)

        mensagens.append({"role": "assistant", "content": None, "tool_calls": mensagem_do_agente["tool_calls"]})
        mensagens.append({"role": "tool", "tool_call_id": chamada["id"], "content": json.dumps(resultado_ferramenta)})

    return {"cliente_id": cliente_id, "erro": "excedeu limite de rodadas"}


resultado_teste = investigar_e_salvar("CLI-003", "fracionamento: 4 operacoes no dia 2026-05-02 somando R$ 50.846,72")
print(resultado_teste)