---
name: otimizar-orcamento
description: Analisa impression share perdido por orcamento versus rank, identifica campanhas estranguladas e ineficientes, e propoe realocacao ou aumento de orcamento dimensionado com projecao e criterio de reversao. Aciona em "orcamento", "budget", "quanto investir", "impression share por dia", "estou perdendo impressao", "realocar verba".
version: 0.1.0
---

# Otimizar Orçamento

Carregue `acesso-dados`, `convencoes-conta` e `metodologia-orcamento-lances`.

## Argumentos
`$ARGUMENTS` pode conter campanha, período e restrição ("sem aumentar o total", "tenho +R$ 5.000"). Padrão: conta inteira, últimos 14 dias.

## Passos

### 1. Puxar impression share por dia
Por campanha, por dia, últimos 14 dias: orçamento diário, `search_impression_share`, `search_budget_lost_impression_share`, `search_rank_lost_impression_share`, `search_absolute_top_impression_share`, custo, cliques, conversões, valor.

Nunca promedie impression share ingenuamente entre linhas — pondere por impressões ou reporte por dia.

### 2. Classificar cada campanha

| Classe | Critério | Ação |
|---|---|---|
| **Estrangulada** | `budget_lost_IS` ≥ 10% consistente **e** dentro da meta de CPA/ROAS | Candidata a aumento |
| **Limitada mas ineficiente** | `budget_lost_IS` ≥ 10% **e** fora da meta | Corrigir eficiência antes; **não** aumentar |
| **Perdendo por rank** | `rank_lost_IS` alto, `budget_lost_IS` baixo | Problema de lance/qualidade, não de orçamento |
| **Folgada** | `budget_lost_IS` < 5% e gasto abaixo do orçamento | Orçamento não é o gargalo |
| **Ineficiente com folga** | Dentro do orçamento, fora da meta | Candidata a corte/realocação |

Sinalize campanhas em aprendizado e campanhas com orçamento compartilhado (a limitação individual fica mascarada).

### 3. Dimensionar
Para cada candidata a aumento: +20% padrão (até +30% se `budget_lost_IS` > 40%). Projete impressões, cliques, conversões e gasto adicional pela fórmula de `metodologia-orcamento-lances`, declarando que é projeção linear e que o CPC marginal tende a subir.

Para cortes: máximo −25% por movimento, preferindo realocar para as estranguladas dentro da meta.

Se houver restrição de orçamento total, monte a proposta como **realocação de soma zero**: de onde sai, para onde vai, e o efeito líquido esperado.

### 4. Entregar

1. **Tabela por dia** da(s) campanha(s) em foco: `Data | IS | Perdido p/ orçamento | Perdido p/ rank | Custo | Conv.`
2. **Leitura em texto**: qual é a restrição dominante e desde quando; padrão de fim de semana; se o orçamento esgota antes do fim do dia.
3. **Proposta por campanha**, no formato de recomendação de `metodologia-orcamento-lances`: valor atual → novo, %, IS, CPA vs meta, projeção, critério de observação e reversão.
4. **Efeito agregado**: gasto mensal atual → proposto, conversões projetadas, CPA projetado da conta.
5. **Oferta de execução** com aprovação explícita.

Salve a proposta em `outputs/recomendacoes-orcamento-YYYY-MM-DD.csv` com colunas:
```
Campaign,Current Daily Budget,Proposed Daily Budget,Change %,IS,Budget Lost IS,Rank Lost IS,CPA,Target CPA,Projected Added Conversions,Projected Added Spend,Rationale,Review Date,Revert If
```

### 5. Execução (após "sim")
`seguranca-aprovacoes`. Orçamento é risco médio até 20% e alto acima disso. Uma alavanca por campanha: não mexa em orçamento e lance na mesma campanha no mesmo movimento. Defina a data de revisão.

## Regras
- Nunca recomende aumento para campanha fora da meta — diga que o problema é eficiência e aponte para `investigar-campanha`.
- Nunca some impression share de campanhas diferentes como se fosse uma média simples.
- Sempre distinga perda por orçamento de perda por rank na primeira frase da análise.
- Sempre diga quando os dados do período recente estão incompletos.
