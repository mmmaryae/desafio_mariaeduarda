# Decisões Técnicas

Esse documento reúne as principais decisões que tomei ao longo do 
desafio, e o porquê de cada uma.

## Limpeza de dados

Encontrei 3 problemas nos dados: uma operação duplicada, uma data 
faltando, e um valor em dólar que precisava ser convertido. Removi 
a duplicata com drop_duplicates(). Pra data faltando, decidi manter 
a operação na tabela principal pra não perder o valor dela nas 
somas gerais porque ela representa uma operação real e não é uma duplicata, 
então criei uma tabela separada sem ela pra usar nas 
regras que comparam datas, pois não dá pra saber se ela aconteceu "no 
mesmo dia" que outra sem essa informação. Converti o valor em USD 
usando a taxa de câmbio que já vinha no próprio arquivo, não exclui a 
a operação  porque ela é uma operação real e válida. O problema não é que o dado esteja errado é que ele só está em uma moeda diferente.

## Regra de fracionamento

No começo, minha regra pegava qualquer cliente que passasse de 
R$ 50.000 num dia, mas percebi que isso também capturava clientes 
com uma única operação grande o que não é fracionamento de 
verdade pois fracionamento é dividir um valor grande em partes menores 
pra não chamar atenção. Ajustei pra exigir soma > R$ 50.000 **e** 
mais de 1 operação no mesmo dia.

## Regra de valor atípico

Usei mediana em vez de média pra definir o "comportamento normal" 
de cada cliente. A média seria distorcida pela própria operação 
atípica que eu tô tentando detectar, então a mediana é uma referência 
mais confiável.

## Por que troquei de Gemini pra Groq

Comecei o Nível 1 com o Gemini. No meio do Nível 1, esgotei o limite 
gratuito da minha chave (erro 429), então troquei pra API do Groq no Nível 2, 
ela se desenvolvel bem melhor, durou mais tempo.
Também precisei trocar o nome do modelo algumas vezes, porque os 
modelos que eu tentava usar iam sendo descontinuados no meio do 
processo isso tá tudo documentado com mais detalhes no 
USO_DE_IA.md.

## O agente com ferramentas

A parte que mais gostei de fazer: em vez de sempre chamar as 3 
ferramentas pra todo cliente, o agente decide sozinho quais ele 
precisa. Fiz um loop que deixa ele pedir mais de uma ferramenta em 
sequência, até ele ter informação suficiente pra dar o parecer 
final. Testando com o CLI-003, por exemplo, ele pediu as 3 
ferramentas em sequência, sem eu ter programado essa ordem.

## Por que só 5 dos 10 clientes foram processados

Ao rodar o agente nos 10 clientes sinalizados, os primeiros 5 
funcionaram certinho, mas os outros 5 deram erro (a própria API do 
Groq retornou "Internal Server Error", provavelmente relacionado ao 
limite de requisições por minuto do plano gratuito). Adicionei 
tratamento de erro pra que uma falha não travasse a análise dos 
demais clientes, e pausas de 3 segundos entre as chamadas pra tentar 
reduzir o problema. Não consegui resolver 100% dentro do tempo que 
tinha. Se tivesse mais tempo, implementaria um retry automático com 
espera progressiva entre tentativas ou mudaria o provedor de IA, 
analisando qual suportaria por mais tempo responder as chamadas que 
eu precisava. Tentaria também escrever um prompt mais detalhado com 
palavras-chave desde o início, e com isso eu acredito que o limite não seria 
atingido tão rápido.

## Comparação entre agente e regras

Nos 5 clientes que processei, o agente concordou com a regra em 
100% dos casos. Minha primeira tentativa de detectar isso usava uma 
lista pequena de frases exatas tipo "suspeita confirmada", e isso 
gerou um falso resultado: um cliente que o agente claramente 
considerava suspeito (recomendando bloqueio e escalando pro 
Compliance) apareceu como "discordou" só porque usou palavras 
diferentes das que eu esperava. Corrigi usando palavras-chave mais 
amplas depois de investigar esse caso manualmente por exemplo:
troquei na ordem "suspeita confirmada" por "suspeit" que já vai incluir 
"suspeita", "suspeito" e "suspensão".

## Sobre o Nível 3

Optei por não fazer. Com o tempo que tinha, achei melhor garantir 
que os Níveis 1 e 2 estivessem completos, testados e bem explicados.