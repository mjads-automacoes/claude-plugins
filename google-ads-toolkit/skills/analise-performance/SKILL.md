---
name: analise-performance
description: Metodologia de analise de performance — decomposicao de metricas, isolamento de causa raiz, significancia estatistica, comparacao de periodos e leitura correta de variacoes. Use para diagnosticar por que gasto, CPA, ROAS, volume ou taxa de conversao mudaram. Aciona em "por que caiu", "analise de performance", "diagnostico", "CPA subiu", "conversoes cairam", "eficiencia de gasto".
version: 0.1.0
---

# Metodologia de Análise de Performance

## A decomposição fundamental

Toda variação de resultado se explica por alguma parte desta cadeia. Sempre decomponha antes de opinar:

```
Conversões = Impressões × CTR × Taxa de Conversão
Custo       = Impressões × CTR × CPC
CPA         = CPC ÷ Taxa de Conversão
ROAS        = (Taxa de Conversão × Valor por Conversão) ÷ CPC
```

Quando alguém pergunta "por que o CPA subiu?", a resposta só pode ser: **o CPC subiu**, **a taxa de conversão caiu**, ou ambos. Identifique qual antes de qualquer hipótese. Depois desça um nível:

- **CPC subiu** → mais concorrência (leilão), Quality Score caiu, mudou o mix de keywords/match types, alvo de lance mudou, mix de dispositivo/geo mudou.
- **Taxa de conversão caiu** → mix de tráfego pior (termos novos, match mais amplo), landing page (quebrou, lenta, mudou), oferta, rastreamento de conversão quebrado, sazonalidade, mix de dispositivo.
- **Impressões caíram** → orçamento, alvo de lance restritivo, campanha/keyword pausada, IS perdido por rank, queda de demanda, mudança de segmentação.

## Ordem de investigação (sempre esta)

1. **O dado é real?** Verifique rastreamento antes de qualquer hipótese de mercado. Conversões que caem a zero de um dia para o outro quase sempre são tag quebrada, não mercado. Cheque também se o período recente está incompleto por janela de atribuição.
2. **Alguém mexeu?** Consulte o histórico de alterações do período. A causa mais frequente de mudança é uma mudança.
3. **É ruído?** Aplique os limiares de significância de `convencoes-conta`. Variação menor que 15% com menos de 100 conversões geralmente é ruído.
4. **Onde está concentrado?** Desça por campanha → ad group → keyword → termo de busca até achar onde a variação vive. Muitas vezes uma única entidade explica a maior parte do movimento.
5. **Mudou o mix?** Uma métrica agregada pode piorar sem que nenhuma parte piore, se o peso entre as partes mudou (paradoxo de Simpson). Sempre cheque marca vs não-marca, dispositivo, geo e tipo de campanha.
6. **Só então**: fatores externos — sazonalidade, concorrência, feriado, notícia.

## Regras de comparação

- Compare **períodos de mesmo tamanho e mesma composição de dias da semana**. 30 dias vs 30 dias, não 30 vs 28.
- Compare também **ano contra ano** quando houver sazonalidade.
- Exclua o dia corrente e sinalize a incompletude dos últimos dias.
- Ao comparar períodos, mostre sempre: valor A, valor B, variação absoluta e variação percentual. Percentual sozinho engana quando a base é pequena.
- Nunca compare campanha em aprendizado com período estável.

## Significância — quando você pode afirmar algo

| Decisão | Volume mínimo |
|---|---|
| Pausar uma keyword | 100 cliques sem conversão, ou gasto ≥ 3× CPA alvo |
| Declarar vencedor entre anúncios | 100 cliques por anúncio |
| Mudar alvo de lance | 30 conversões no período |
| Afirmar que um segmento é pior | 30 conversões ou 1.000 cliques |
| Afirmar tendência | 3 períodos consecutivos na mesma direção |

Abaixo disso, escreva explicitamente "sem volume para conclusão" em vez de sugerir ação. Recomendação sem base é o principal jeito de piorar uma conta.

## Análise de eficiência de gasto

Método padrão para "onde meu dinheiro está sendo mal usado":

1. Ordene entidades por **gasto decrescente** — os 20% que gastam mais geralmente contêm 80% do problema.
2. Para cada uma, calcule `CPA` (ou `ROAS`) e compare com a meta de `convencoes-conta`.
3. Classifique:
   - **Desperdício claro**: gasto ≥ 3× CPA alvo, zero conversão.
   - **Ineficiente**: converte, mas CPA ≥ 1,5× a meta.
   - **Saudável**: dentro da meta.
   - **Estrangulado**: dentro da meta **e** limitado por orçamento → oportunidade de escala.
4. Quantifique: quanto do gasto total está em cada classe. Isso transforma a análise em decisão de dinheiro.
5. Para cada item de desperdício, não pare no "pause" — diga **por quê** ele está desperdiçando (termos, anúncio, landing page, match type).

## Segmentações que mais revelam causa

Rode quando o agregado não explica:
- **Dia** — identifica evento pontual vs tendência.
- **Dia da semana e hora** — padrões de horário comercial, fins de semana.
- **Dispositivo** — mobile costuma ter taxa de conversão menor; mudança de mix distorce o agregado.
- **Geo** — desperdício em regiões não atendidas.
- **Rede** — parceiros de pesquisa e Display costumam performar diferente.
- **Marca vs não-marca** — a mais importante. Marca infla o resultado agregado.
- **Novo vs recorrente** (quando disponível).

## Como escrever a conclusão

Nunca entregue apenas números. Toda análise termina com:

1. **O que aconteceu** — uma frase, com número.
2. **Por quê** — a causa isolada, com a evidência que a sustenta.
3. **O que fazer** — ações priorizadas por impacto em dinheiro.
4. **O que observar** — métrica, prazo, e o que indicaria que a hipótese estava errada.

Se a causa não foi isolada, diga isso claramente e liste as hipóteses restantes com o dado que faltaria para decidir entre elas. Honestidade sobre incerteza vale mais que uma causa inventada.
