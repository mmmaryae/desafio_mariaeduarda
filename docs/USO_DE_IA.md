# Uso de IA no desenvolvimento

## Ferramentas usadas
- - **Claude (Anthropic)**: usei como apoio durante todo o desenvolvimento,
  principalmente para entender conceitos que eu não conhecia no Jupyter
  Notebook e no Pandas, entender a diferença entre regras determinísticas e
  LLM, tirar dúvidas de código e revisar minha lógica antes de implementar.

  Eu sempre procurei dar o meu ponto de vista e pedi que a IA me ajudasse
  fazendo perguntas, para que eu pudesse desenvolver meu próprio raciocínio.
  A partir dessas perguntas, eu conseguia fazer minha própria análise e
  escolher os caminhos que faziam mais sentido para o projeto.

  Um exemplo foi a decisão sobre o que fazer com uma operação que estava sem
  data. A IA apresentou três possibilidades: retirar a operação da análise,
  preencher a data com uma data "estimada" ou manter a operação, mas deixá-la
  de fora das regras que dependem de data. Eu escolhi a terceira opção.

  Minha decisão foi manter a operação porque ela era uma operação real e não
  uma duplicata, então não faria sentido simplesmente excluí-la. Também não
  achei adequado preencher a data com uma data "estimada", pois isso poderia
  alterar a interpretação da análise.

  Apesar de o valor dessa operação ser baixo e, isoladamente, não representar
  uma operação que atingiria o limite da regra de fracionamento, imaginei uma
  situação em que o cliente tivesse feito duas operações no mesmo dia e essa
  operação sem data fosse justamente uma terceira operação. Nesse caso,
  poderíamos deixar de identificar uma situação que deveria ser analisada pela
  regra, caso simplesmente ignorássemos a operação.

  Por isso, decidi manter a operação na base original e criar uma tabela
  separada contendo apenas as operações com data preenchida. Dessa forma, a
  operação sem data não é excluída dos dados, mas também não é utilizada em
  análises que dependem de uma data conhecida.

  A IA foi utilizada como apoio para apresentar alternativas e questionar
  minhas decisões, mas a análise do problema e a escolha da abordagem foram
  minhas.


- **Gemini (Google AI Studio)**: usei no Nível 1 pra gerar o parecer 
  sobre o cliente sinalizado pela regra de fracionamento.
- **Groq**: usei no Nível 2, depois de esgotar o limite gratuito do 
  Gemini. É a IA por trás do agente que decide sozinho quais 
  ferramentas usar pra investigar cada cliente.

## Um momento em que a IA me levou pro caminho errado

Ao montar a comparação entre o agente e as regras (`confronto.py`), 
pedi ajuda pra detectar se o parecer do agente "concordava" com a 
regra. A sugestão inicial foi procurar por frases exatas, tipo 
"suspeita confirmada". Isso gerou um resultado errado: um cliente 
que o agente claramente considerava suspeito (recomendando bloqueio 
e escalando pro Compliance) apareceu como "discordou", só porque 
usou palavras diferentes das que eu esperava.

Percebi isso lendo o parecer completo desse cliente na mão e vendo 
que não batia com o resultado do código. Corrigi trocando as frases 
exatas por palavras-chave mais amplas, por exemplo eu troquei 
"suspeita confirmada" por apenas "suspeit" (que já pega "suspeita", 
"suspeito" e "suspensão").

Também tive alguns perrengues parecidos com nomes de modelo 
desatualizados. Passei por isso algumas vezes: pedi pra IA qual era 
o melhor modelo pra essa aplicação, mas ela me deu uns 3 modelos do 
Gemini que já estavam desatualizados. Acredito que isso influenciou 
bastante no desgaste dos meus tokens gratuitos, já que eu não tinha 
escolhido o melhor modelo desde o início. Fui na documentação oficial 
do Gemini, vi um exemplo de modelo na primeira página e usei ele ai sim
funcionou. Numa próxima vez, eu analisaria mais modelos para escolher um
mais simples que atenderia por completo as minhas requisições sem gastar muitos  tokens gratuitos.

Com o Groq também tive erro 404 por causa de modelo desatualizado, 
mas foi mais tranquilo, porque a chave dele durou bem mais tempo que 
a do Gemini. Também tive um FutureWarning do pandas 
que eu não entendi de cara, e pedi pra IA explicar o que significava 
antes de aplicar a correção.