---
name: checagem-diaria
description: Verificacao diaria rapida da conta — anomalias de gasto, quedas de conversao, campanhas travadas, anuncios reprovados e alertas de orcamento. Roda em poucos minutos e so reporta o que exige atencao. Aciona em "checagem diaria", "tudo certo hoje", "alguma anomalia", "status da conta", "bom dia".
version: 0.1.0
---

# Checagem Diária

Carregue `acesso-dados` e `convencoes-conta`. Esta skill é curta por natureza: **se está tudo normal, diga em duas linhas e pare.** Relatório diário longo deixa de ser lido.

## O que verificar

### Alarmes (reportar sempre que ocorrerem)
1. **Gasto anômalo** — gasto de ontem fora da faixa de ±30% da média dos 7 dias anteriores (mesmo dia da semana quando possível).
2. **Conversões zeradas** — campanha que converte normalmente e ficou em zero ontem. Suspeite de rastreamento antes de mercado.
3. **Campanha ou ad group pausado inesperadamente** — cruze com o histórico de alterações.
4. **Anúncio reprovado ou com política pendente**.
5. **Campanha ativa sem impressões** nas últimas 24h.
6. **Orçamento esgotado cedo** — `budget_lost_IS` muito acima do normal.
7. **Erro de faturamento / método de pagamento** (quando visível pela API).
8. **Salto de CPC** — CPC médio de ontem > 1,4× a média dos 7 dias.
9. **Landing page com erro** — URL final retornando falha, quando verificável.

### Contexto (reportar só se houver alarme)
- Gasto do mês contra o ritmo necessário para o orçamento mensal.
- Alterações feitas na conta nas últimas 24h.

## Formato da resposta

Se **nada** disparar:
```
Conta <nome> · <data>: sem anomalias.
Gasto ontem: R$ <x> (média 7d: R$ <y>) · Conv.: <n> · CPA: R$ <z>
```

Se **houver** alarme:
```
⚠ <n> pontos de atenção — <conta> · <data>

1. <alarme> — <campanha>
   Dado: <número vs esperado>
   Provável causa: <hipótese ou "não determinado">
   Sugestão: <ação, ou "investigar com /investigar-campanha">
...

Gasto ontem: R$ <x> (média 7d: R$ <y>) · Conv.: <n> · CPA: R$ <z>
```

## Regras
- **Não proponha otimizações aqui.** Esta skill detecta anomalias; otimização é trabalho das outras skills.
- Lembre que os dados de ontem podem estar incompletos por janela de atribuição — sinalize quando a conclusão depender disso.
- Não dispare alarme por variação dentro do ruído normal da conta; calibre com a média móvel, não com um dia isolado.
- Nunca execute nada nesta skill — ela é somente leitura.
