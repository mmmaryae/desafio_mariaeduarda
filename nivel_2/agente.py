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




