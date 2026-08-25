import requests
import os
import json
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


def investigar_cliente(cliente_id, motivo_sinalizacao):
    mensagens = [
        {"role": "user", "content": f"O cliente {cliente_id} foi sinalizado como suspeito pelo seguinte motivo: {motivo_sinalizacao}. Use as ferramentas disponiveis para investigar o comportamento dele e depois de o parecer final."}
    ]
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    corpo = {
        "model": "openai/gpt-oss-20b",
        "messages": mensagens,
        "tools": ferramentas_disponiveis
    }
    
    resposta = requests.post(url, headers=headers, json=corpo)
    return resposta.json()

resultado = investigar_cliente("CLI-003", "fracionamento: 4 operacoes no dia 2026-05-02 somando R$ 50.846,72")
print(resultado)