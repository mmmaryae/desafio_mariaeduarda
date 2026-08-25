# desafio_mariaeduarda

# Desafio Técnico — Engenharia de IA (PLD/AML)

Esse projeto foi feito para o teste técnico da vaga de estágio em 
Engenharia de IA. 

# O que o projeto faz

A ideia é identificar comportamento suspeito de lavagem de dinheiro 
em operações financeiras, combinando regras de negócio feitas com 
pandas,  com a interpretação de um LLM que só entra depois, pra explicar o caso como um analista faria.

- Nível 1: limpeza dos dados, 2 regras (fracionamento e valor 
  atípico), e um parecer gerado pelo Gemini pra um cliente sinalizado.
- Nível 2: a mesma lógica numa base bem maior, mais um agente 
  (usando o Groq) que decide sozinho quais ferramentas ele precisa 
  usar pra investigar cada cliente, não é um script fixo, ele 
  realmente escolhe.

## Como rodar

# Pré-requisitos
- Python 3.9+
- Uma chave gratuita do [Google AI Studio](https://aistudio.google.com/app/apikey) (Nível 1)
- Uma chave gratuita do [Groq](https://console.groq.com/keys) (Nível 2)

# Passos
1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Copie o `.env.example` para `.env` e cola suas chaves
4. Nível 1: abre `nivel_1/nivel_1.ipynb` e roda célula por célula
5. Nível 2: roda os scripts em `nivel_2/` (`tools.py`, `agente.py`, `confronto.py`)

## O que consegui terminar

- Nível 1: completo
- Nível 2: completo, só que o agente só processou 5 dos 10 clientes 
  sinalizados — a API gratuita do Groq começou a dar erro de 
  instabilidade/limite no meio do processo
- Nível 3: não fiz. Preferi deixar os Níveis 1 e 2 bem feitos.

Tem mais detalhes de cada decisão em `docs/DECISOES.md`, e de como 
usei IA no processo em `docs/USO_DE_IA.md`.