---
name: metodologia-orcamento-lances
description: Metodologia de orcamento e lances — como ler impression share perdido por orcamento versus rank, dimensionar aumentos e cortes, escolher e ajustar estrategias de lance (tCPA, tROAS, maximizar conversoes), e respeitar periodo de aprendizado. Aciona em "orcamento", "budget", "impression share", "lance", "tCPA", "tROAS", "aumentar investimento", "estrategia de lance", "perdendo impressao".
version: 0.1.0
---

# Metodologia de Orçamento e Lances

Orçamento e lance resolvem problemas diferentes. Confundi-los é o erro mais caro em gestão de Search.

- **Perdendo por orçamento** (`search_budget_lost_impression_share`) → a campanha para de aparecer porque acabou o dinheiro. Solução: orçamento.
- **Perdendo por rank** (`search_rank_lost_impression_share`) → o anúncio não é competitivo o suficiente. Solução: lance, qualidade do anúncio, relevância, landing page. **Não** é orçamento.

As três partes somam ~100%: `impression_share + budget_lost + rank_lost ≈ 1`.

## Diagnóstico de orçamento

### Passo 1 — puxe por dia, não agregado
Impression share agregado esconde o padrão. Puxe os últimos 14 dias por campanha por dia e olhe:
- O IS perdido por orçamento é **consistente** (todo dia) ou **pontual** (picos)?
- Há queda de IS no fim do dia? Isso indica esgotamento de orçamento antes do fim do dia.
- Os dias fracos coincidem com fim de semana? Volume menor com orçamento fixo pode dar falsa folga.

### Passo 2 — qualifique antes de aumentar
Só recomende aumento de orçamento quando **todas** forem verdadeiras:
1. `budget_lost_IS` ≥ 10% de forma consistente (≥ 5 dos últimos 7 dias).
2. A campanha está **dentro da meta** de CPA/ROAS — ou dentro do limite aceitável de `convencoes-conta`.
3. Há volume de conversão suficiente para confiar no CPA (≥ 15–30 conversões no período).
4. A campanha não teve mudança estrutural recente que ainda esteja em aprendizado.

Se (1) é verdade mas (2) não é: o problema não é orçamento, é eficiência. Aumentar orçamento só multiplica o prejuízo. Diga isso explicitamente.

### Passo 3 — dimensione o aumento
- **Incremento padrão: 20%.** Mudanças maiores jogam a campanha em reaprendizado e tornam a leitura de resultado impossível.
- Máximo de 30% por movimento, e apenas quando `budget_lost_IS` > 40%.
- Espere 7–14 dias entre aumentos consecutivos na mesma campanha.
- Estime o resultado: `impressões adicionais ≈ impressões atuais × (budget_lost_IS / IS_atual)`. Aplique o CTR e a taxa de conversão atuais para projetar cliques e conversões, e **declare que é projeção linear** — o CPC marginal tende a subir.

Formato da recomendação:
```
<Campanha> · R$ <atual>/dia → R$ <novo>/dia (+<x>%)
IS: <x>% · Perdido por orçamento: <x>% · Perdido por rank: <x>%
CPA atual: R$ <x> (meta: R$ <y>)
Projeção: +<n> cliques/dia, +<n> conversões/mês, +R$ <n> de gasto/mês
Observar: CPA em 14 dias. Reverter se CPA > R$ <limite>.
```

### Passo 4 — cortes
Corte orçamento quando: CPA/ROAS fora da meta com volume significativo **e** a campanha não tem papel estratégico (prospecção de topo, teste, marca). Prefira **realocar** para uma campanha limitada por orçamento e dentro da meta — corte que vira realocação é decisão de portfólio, não de economia.

Nunca corte mais de 25% de uma vez; corte abrupto também gera reaprendizado.

## Diagnóstico de lances

### Perdendo por rank — o que realmente fazer
`rank_lost_IS` alto significa que Ad Rank está baixo. Ad Rank ≈ lance × qualidade × impacto esperado dos assets. Antes de subir lance, verifique na ordem:
1. **Quality Score e componentes** — CTR esperado, relevância do anúncio, experiência na landing page. Um QS 4 por relevância de anúncio se resolve com copy, não com dinheiro.
2. **Ad strength / assets** — RSA fraco derruba Ad Rank.
3. **Match type e estrutura** — keyword genérica em ad group amplo perde para concorrente específico.
4. **Só então** lance / alvo de tCPA.

### Estratégias de lance — quando usar cada uma

| Estratégia | Use quando | Cuidados |
|---|---|---|
| **Maximizar conversões** | Conta nova ou < 15 conversões/mês; quer volume dentro do orçamento | Gasta o orçamento inteiro; CPA pode disparar |
| **tCPA** | ≥ 30 conversões/mês estáveis e meta de CPA clara | Alvo muito agressivo estrangula volume |
| **Maximizar valor de conversão** | E-commerce com valores variados, sem meta de ROAS firme | Precisa de valor de conversão confiável |
| **tROAS** | ≥ 50 conversões/mês com valor; meta de retorno definida | Exige qualidade do dado de receita |
| **CPC manual / eCPC** | Contas muito pequenas, ou controle granular temporário | Não escala; exige gestão ativa |

### Ajuste de alvos (tCPA / tROAS)
- Mova o alvo em **no máximo 15–20% por vez**.
- Espere o período de aprendizado completo (7–14 dias ou 30 conversões) antes do próximo ajuste.
- Se o CPA real está consistentemente **abaixo** do alvo e há `budget_lost_IS`, o gargalo é orçamento, não alvo.
- Se o CPA real está consistentemente **acima** do alvo, não baixe o alvo imediatamente — investigue mix de tráfego (marca vs não-marca), termos de busca e sazonalidade primeiro.
- Alvo de tCPA muito abaixo do CPA histórico **reduz entrega**; a campanha simplesmente para de comprar. Sinalize isso.

### Período de aprendizado
Após mudança de estratégia, alvo, orçamento > 20%, ou alteração estrutural relevante:
- A campanha entra em aprendizado por 7–14 dias.
- **Não avalie resultado nem faça nova mudança durante esse período.**
- Sempre declare quando uma campanha está em aprendizado antes de tirar qualquer conclusão sobre ela.

## Regras de portfólio

1. Não avalie campanha de marca com o mesmo limiar de não-marca.
2. Orçamento compartilhado esconde limitação individual — sinalize quando existir.
3. Antes de pedir mais orçamento total, procure desperdício: termos ruins, geo fora de área, horários improdutivos. Eficiência primeiro, escala depois.
4. Uma alavanca por vez por campanha. Orçamento **ou** lance, não os dois.
5. Toda recomendação declara: métrica de observação, prazo e critério de reversão.
