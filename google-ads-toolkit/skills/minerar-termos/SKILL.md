---
name: minerar-termos
description: Minera o relatorio de termos de busca para encontrar palavras negativas e oportunidades de keyword, com avaliacao de relevancia e CSV pronto para bulk upload no Google Ads Editor. Aciona em "minerar termos", "negativar", "limpar termos de busca", "search term report", "achar desperdicio".
version: 0.1.0
---

# Minerar Termos de Busca

Carregue `acesso-dados`, `convencoes-conta` e `metodologia-termos-busca` antes de começar. O entregável final é um **CSV pronto para bulk upload** no Google Ads Editor mais um resumo que permita auditar a lógica antes de qualquer execução.

## Argumentos

`$ARGUMENTS` pode conter: nome ou ID de campanha, período ("últimos 14 dias"), foco ("só desperdício", "só oportunidades"). Sem argumentos, use a conta inteira e os últimos 30 dias.

## Passos

### 1. Puxar os termos
Consulte `search_term_view` com `status = NONE`, `clicks >= 1`, ordenado por `cost_micros` desc, limite 2000. Filtre por campanha se especificado. Traga: termo, keyword que casou, match type, campanha, ad group, custo, cliques, impressões, CPC, CTR, conversões, valor de conversão.

Declare no topo: conta, período, nº de termos analisados, gasto total nesses termos.

### 2. Avaliar cada termo
Aplique integralmente `metodologia-termos-busca`: cruze termo × keyword × campanha/ad group e decida **Negativar**, **Realocar**, **Manter** ou **Promover**.

Para cada termo negativado, registre:
- o **motivo** da taxonomia oficial (rótulo exato)
- o **nível** de aplicação (ad group / campanha / lista compartilhada)
- o **match type** do negativo (exato por padrão)
- uma **frase de reasoning** que um humano consiga auditar sem ver o resto

Relevância manda sobre contagem de conversões: termo on-theme sem conversão é **Manter** (e vira achado de investigação, não negativo).

### 3. Verificar colateral
Antes de propor qualquer negativo de frase ou amplo, cruze o token com as keywords ativas e com os termos que converteram. Se houver colisão, rebaixe para exato. Declare essa verificação no relatório.

### 4. Detectar padrões
Suba um nível e reporte:
- tokens recorrentes (candidatos a lista compartilhada)
- keywords que mais vazam termos ruins
- ad groups com mira ruim (> 30% do gasto não acionado é off-theme)
- concentração: % do desperdício nos 10 primeiros termos

### 5. Construir o CSV
Salve em `outputs/termos-negativos-YYYY-MM-DD.csv`, **apenas com os termos recomendados para negativação**, com as colunas nesta ordem:

```
Campaign,Ad Group,Keyword,Search Term,Match Type,Cost,Clicks,Impressions,CPC,CTR,Conversions,Negative Level,Negative Match Type,Reason Code,Reasoning
```

- `Keyword` = a keyword que casou com o termo (contexto para auditoria).
- `Negative Match Type` = Exact / Phrase / Broad.
- `Reason Code` = rótulo da taxonomia.
- `Reasoning` = frase legível explicando a decisão.
- Ordene por `Cost` decrescente.
- Formate números com a moeda da conta e sem separador que quebre CSV.

Se houver **oportunidades** (Promover / Realocar), gere um segundo arquivo `outputs/termos-oportunidades-YYYY-MM-DD.csv` com:
```
Campaign,Ad Group,Search Term,Suggested Keyword,Suggested Match Type,Destination Ad Group,Cost,Clicks,Conversions,CPA,Rationale
```

### 6. Apresentar o resumo
Na resposta, entregue nesta ordem:

1. **Cabeçalho**: conta, período, termos analisados, gasto analisado.
2. **Números-chave**: gasto desperdiçado identificado (R$ e % do gasto do período), nº de negativos propostos, nº de oportunidades.
3. **Tabela dos 10 negativos de maior gasto**: `# | Termo | Ad Group | Custo | Motivo (frase curta)`.
4. **Breakdown por categoria**: contagem e gasto por `Reason Code`, ordenado por gasto.
5. **Padrões encontrados**: tokens recorrentes, keywords vazando, ad groups com mira ruim.
6. **Oportunidades**: termos a promover/realocar, com CPA.
7. **Link para os arquivos** gerados.
8. **Oferta de execução**, exatamente neste espírito:
   > Quer que eu adicione esses negativos? Vou agrupar por campanha e ad group, mostrar cada lote e aguardar seu "sim" explícito antes de executar qualquer coisa.

### 7. Execução (somente após "sim")
Siga `seguranca-aprovacoes`. Agrupe por campanha/ad group, mostre o preview de cada lote, execute um lote por vez, verifique o estado final e grave o `historico-alteracoes`.

## Regras
- Nunca negative sem reasoning auditável — a coluna de reasoning é o motivo de este fluxo existir.
- Nunca inclua no CSV termos marcados como Manter.
- Se um termo já converteu e ainda assim é candidato a negativo, marque-o em destaque e exija confirmação individual.
- Se o volume de termos for grande demais para avaliar todos, avalie por gasto até cobrir **90% do gasto não acionado** e diga explicitamente quantos termos ficaram de fora e quanto gasto representam.
- PMax: analise por categoria via `campaign_search_term_insight` e diga que a granularidade é menor.
