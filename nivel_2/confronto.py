import json

with open("../outputs/pareceres_agente.json", "r", encoding="utf-8") as arquivo:
    pareceres = json.load(arquivo)

print(f"Total de clientes no arquivo: {len(pareceres)}")
for parecer in pareceres:
    print(parecer.get("cliente_id"), "-", "erro" if "erro" in parecer else "processado com sucesso")