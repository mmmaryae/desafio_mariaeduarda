import json

with open("../outputs/pareceres_agente.json", "r", encoding="utf-8") as arquivo:
    pareceres = json.load(arquivo)

print(f"Total de clientes no arquivo: {len(pareceres)}")
for parecer in pareceres:
    print(parecer.get("cliente_id"), "-", "erro" if "erro" in parecer else "processado com sucesso")


def agente_concordou(texto_avaliacao):
    texto_minusculo = texto_avaliacao.lower()
    palavras_confirma = ["suspeit", "risco elevado", "risco alto", "bloqueio", "investigação adicional", "compliance", "monitorar", "alerta"]
    palavras_discorda = ["não há indícios", "comportamento normal", "sem suspeita", "baixo risco", "não suspeito"]
    
    for palavra in palavras_discorda:
        if palavra in texto_minusculo:
            return False
    
    for palavra in palavras_confirma:
        if palavra in texto_minusculo:
            return True
    
    return None

print("")
print("Comparação regra vs agente:")

for avaliacao in pareceres:
    if "erro" in avaliacao:
        print(f"{avaliacao['cliente_id']}: nao foi possivel comparar (erro na chamada)")
        continue
    
    concordou = agente_concordou(avaliacao["parecer_final"])
    if concordou is True:
        resultado_comparacao = "CONCORDOU"
    elif concordou is False:
        resultado_comparacao = "DISCORDOU"
    else:
        resultado_comparacao = "INCERTO (revisar manualmente)"
    print(f"{avaliacao['cliente_id']}: regra sinalizou por '{avaliacao['motivo_sinalizacao']}' | agente {resultado_comparacao}")
