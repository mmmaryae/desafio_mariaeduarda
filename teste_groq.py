import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {API_KEY}"}
corpo = {
    "model": "openai/gpt-oss-20b",
    "messages": [{"role": "user", "content": "Diga oi em uma frase"}]
}
resposta = requests.post(url, headers=headers, json=corpo)
print(resposta.json())