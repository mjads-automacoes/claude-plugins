---
name: acesso-dados
description: Contrato de acesso a dados do Google Ads. Define as capacidades que toda skill deste plugin assume (leitura via GAQL, escrita via mutate) e como degradar para CSV exportado quando nao ha conexao de API. Carregue esta skill antes de qualquer outra skill deste plugin que precise de dados da conta. Aciona em "puxar dados", "conectar conta", "nao tenho MCP", "exportei o relatorio", "qual conta".
version: 0.1.0
---

# Contrato de Acesso a Dados

Esta skill é a **camada de abstração** entre as skills de análise e a origem dos dados. Nenhuma outra skill deste plugin deve assumir um servidor MCP específico. Todas pedem *capacidades*, e esta skill resolve como atendê-las.

## Modos de operação

Ao iniciar qualquer tarefa, determine em qual modo você está — nesta ordem de preferência:

| Modo | Como detectar | O que é possível |
|---|---|---|
| **A — API conectada** | Existe um conector/servidor MCP de Google Ads disponível na sessão | Leitura via GAQL e escrita via mutate, com aprovação |
| **B — Leitura conectada** | MCP disponível mas sem escopo de escrita, ou escrita desativada pelo usuário | Leitura completa; entregáveis viram CSV/instruções |
| **C — CSV exportado** | Sem MCP; o usuário anexa ou aponta arquivos exportados do Google Ads | Análise completa sobre o que foi exportado; entregáveis viram CSV |

**Nunca invente dados.** Se você está no modo C e o relatório necessário não foi fornecido, peça exatamente o relatório que falta (veja "Exports necessários" abaixo) em vez de estimar números.

Sempre declare o modo no início da resposta, em uma linha: `Modo: A (API conectada) · Conta: <nome/ID> · Período: <datas>`.

## Mapeamento: Porter MCP (conexão ativa)

A conexão desta conta é o **Porter** — plataforma de dados de marketing com o conector
`google-ads` autorizado. Atende ao **Modo A**: leitura e escrita.

### Leitura — dois caminhos

**1. `query_data`** — métricas e dimensões curadas. Use para quase tudo.
- `accounts`: refs assinadas vindas de `list_accounts(connector="google-ads", query="<nome>")`.
  Passe a ref **verbatim**; nunca monte IDs à mão.
- `metrics` / `dimensions`: nomes vindos de `list_fields(connector="google-ads")`.
- `date_range`: `{"preset": "last_30_days"}` **ou** `{"from": ..., "to": ...}` — nunca os dois.
- `filters`: `{field, operator, value}` com `eq|neq|gt|gte|lt|lte|contains|ncontains|in|null|notnull`.
- Presets resolvem em UTC; `last_7_days` e `last_30_days` terminam ontem.

**2. GAQL puro** — via `execute_action` com `google_ads.keyword_list` ou
`google_ads.budget_list`, que aceitam o parâmetro `query` com GAQL completo. Use quando
`query_data` não cobrir o recorte: histórico de alterações, Quality Score por componente,
negativos existentes, e os *resource names* necessários para mutação.

### ⚠ Grupos de campos que NÃO se combinam

Verificado em execução real. O Porter recusa combinações que atravessam recursos
diferentes do Google Ads, com o erro genérico *"cannot be combined"*:

- **`google_ads_search_term` × keyword** — termo de busca vive em `search_term_view`,
  keyword vive em `keyword_view`. **Não podem ser pedidos na mesma chamada de `query_data`.**
- `google_ads_keyword` **não é o texto da keyword** — é um resource name que vive em
  `click_view` e arrasta um filtro obrigatório de um único dia. O texto é
  `google_ads_keyword_info_text`.
- `google_ads_historical_quality_score` só existe em `keyword_view` e **não aceita**
  `campaign_name` nem `ad_group_name` junto.
- `google_ads_asset_group_name` só retorna linhas de campanhas PMax.

**Consequência para este plugin:** o cruzamento termo × keyword × ad group, que é o núcleo
de `metodologia-termos-busca`, **não pode ser feito por `query_data`**. Use GAQL via
`execute_action` → `google_ads.keyword_list`, onde a API do Google entrega tudo junto:

```sql
SELECT search_term_view.search_term, search_term_view.status,
       segments.keyword.info.text, segments.keyword.info.match_type,
       campaign.name, ad_group.name,
       metrics.cost_micros, metrics.clicks, metrics.impressions,
       metrics.conversions, metrics.ctr
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS AND metrics.clicks >= 1
ORDER BY metrics.cost_micros DESC LIMIT 500
```

Params: `customer_id` (sem hífens), `login-customer-id` (o MCC) e `query`.

O retorno vem em `result[].results[]`, com chaves em camelCase (`searchTermView.searchTerm`,
`metrics.costMicros`) — diferente do snake_case do GAQL enviado. Uma conta com algumas
centenas de termos estoura o limite de tokens da resposta e é salva em arquivo; processe
esse arquivo com script em vez de tentar lê-lo inteiro.

Em caso de erro inesperado do Porter, `get_knowledge` traz o padrão erro→correção.

### Campos equivalentes

| Capacidade | Campo no Porter |
|---|---|
| Termo de busca | `google_ads_search_term` |
| Status do termo (acionado ou não) | `google_ads_search_term_status` |
| Match type do termo | `google_ads_search_term_match_type` |
| Keyword que casou | `google_ads_keyword` |
| Impression share | `google_ads_search_impression_share` |
| IS perdido por orçamento | `google_ads_search_budget_lost_impression_share` |
| IS perdido por rank | `google_ads_search_rank_lost_impression_share` |
| IS absoluto no topo | `google_ads_search_absolute_top_impression_share` |
| Headlines do RSA | `google_ads_ad_group_ad_ad_responsive_search_ad_headlines` |
| Descrições do RSA | `google_ads_ad_group_ad_ad_responsive_search_ad_descriptions` |
| Orçamento compartilhado? | `google_ads_campaign_budget_explicitly_shared` |
| CTR / impressões | `google_ads_ctr` / `google_ads_impressions` |

Confirme sempre o nome exato com `list_fields(connector="google-ads", query="<termo>")`:
o campo `exact_match` na resposta aponta o correto. Passe `account_id` ao `list_fields`
para trazer junto as ações de conversão customizadas da conta.

### Escrita — ações disponíveis

| Ação do plugin | Ação no Porter | Observação |
|---|---|---|
| Adicionar negativo | `google_ads.keyword_create` com `negative: true` | Exige `ad_group` (resource name) e `match_type` |
| Adicionar keyword | `google_ads.keyword_create` | `negative` ausente ou `false` |
| Pausar keyword | `google_ads.keyword_update` com `status` | Texto e match type são imutáveis |
| Alterar orçamento | `google_ads.budget_update` com `amount_micros` | Use esta, **não** `campaign_update` |
| Pausar campanha / alvo de lance | `google_ads.campaign_update` | |
| Pausar ad group / lance | `google_ads.adgroup_update` | |
| Pausar anúncio | `google_ads.ad_update` | Só `status`; mudar conteúdo exige recriar |

**Valores monetários vão em micros**: R$ 8.160,00 → `amount_micros: "8160000000"`.

Mutação exige o **resource name** da entidade. Obtenha-o antes com o `*_list`
correspondente via GAQL — nunca construa um resource name por conta própria.

### Proibido nesta conexão

`google_ads.keyword_remove` é marcada como **irreversível** pelo próprio Porter. Este
plugin não a utiliza. Para desativar uma keyword use `keyword_update` com
`status: "PAUSED"` — reversível e com o mesmo efeito prático.

### Cuidado com licenças

`query_data` **materializa** uma conta listada como `available`, e cada materialização
consome um slot de licença do workspace. Consulte apenas as contas que o usuário pediu;
nunca varra a lista inteira "para ver quais têm dados".

### Operação multi-conta

Esta conexão tem **65 contas** de Google Ads, em estrutura de agência. Portanto:

1. **Sempre confirme de qual conta se trata** antes de qualquer análise, e declare o nome
   dela no cabeçalho do entregável. Nunca assuma a primeira da lista.
2. Várias contas aparecem **duplicadas** — a mesma conta sob MCCs diferentes
   (ex.: `GARAGEM 37 (1458159046) - Managed by 1458159046` e `- Managed by 7755113695`).
   São a mesma conta vista por dois caminhos: escolha uma, diga qual, e **nunca some as duas**.
3. `convencoes-conta` descreve **uma** conta. Em operação de agência, mantenha um bloco de
   convenções por cliente e carregue o do cliente em questão.

## Capacidades de leitura exigidas

As skills deste plugin assumem que é possível obter os conjuntos abaixo. Os nomes são conceituais — mapeie-os para as ferramentas que existirem na sessão.

1. **`accounts`** — lista de contas acessíveis (ID, nome, moeda, fuso, se é MCC).
2. **`campaigns`** — id, nome, status, tipo de canal, estratégia de lance, orçamento diário, métricas.
3. **`ad_groups`** — id, nome, status, campanha pai, métricas.
4. **`keywords`** — texto, match type, status, ad group, lance, quality score e componentes, métricas.
5. **`search_terms`** — termo, keyword que casou, match type, campanha, ad group, status de ação (`NONE` / `ADDED` / `EXCLUDED`), métricas.
6. **`ads`** — RSA com headlines, descriptions, paths, final URL, ad strength, métricas; assets do PMax.
7. **`negative_keywords`** — negativos em nível de conta, campanha, ad group e listas compartilhadas.
8. **`metrics_by_segment`** — métricas segmentadas por dia, dispositivo, geo, hora, dia da semana, rede.
9. **`auction_insights` / `impression_share`** — search_impression_share, search_budget_lost_impression_share, search_rank_lost_impression_share, search_top_impression_share, search_absolute_top_impression_share.
10. **`conversion_actions`** — ações de conversão, se contam em "Conversions", categoria e janela de atribuição.
11. **`change_history`** — alterações recentes na conta, com data, tipo e responsável.
12. **`assets` / `asset_groups`** — para Performance Max: grupos de ativos, temas de busca, sinais de audiência, performance por ativo.

### Métricas mínimas em qualquer recorte
`impressions`, `clicks`, `cost_micros` (→ dividir por 1.000.000), `conversions`, `conversions_value`, `ctr`, `average_cpc`, `cost_per_conversion`, `conversions_from_interactions_rate`, `value_per_conversion`.

## Capacidades de escrita exigidas

Toda escrita passa pelo protocolo de aprovação (ver `seguranca-aprovacoes`). As mutações previstas são:

- adicionar negativos (ad group / campanha / lista compartilhada)
- adicionar e pausar keywords
- alterar orçamento diário de campanha
- alterar alvos de tCPA / tROAS
- pausar/ativar campanha, ad group, keyword, anúncio
- criar e editar RSAs
- ajustar modificadores de lance por dispositivo, geo e horário
- criar e aplicar rótulos (labels)

## Padrões de consulta (GAQL)

Quando houver API, use GAQL. Padrões que as skills deste plugin reutilizam:

**Termos de busca não acionados, por gasto:**
```sql
SELECT search_term_view.search_term, search_term_view.status,
       segments.keyword.info.text, segments.keyword.info.match_type,
       campaign.name, ad_group.name,
       metrics.cost_micros, metrics.clicks, metrics.impressions,
       metrics.conversions, metrics.conversions_value, metrics.ctr
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
  AND search_term_view.status = 'NONE'
  AND metrics.clicks >= 1
ORDER BY metrics.cost_micros DESC
LIMIT 2000
```

**Impression share por dia:**
```sql
SELECT campaign.name, campaign.id, segments.date,
       campaign_budget.amount_micros,
       metrics.search_impression_share,
       metrics.search_budget_lost_impression_share,
       metrics.search_rank_lost_impression_share,
       metrics.search_absolute_top_impression_share,
       metrics.cost_micros, metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_14_DAYS
  AND campaign.status = 'ENABLED'
ORDER BY campaign.name, segments.date
```

**Keywords com Quality Score e componentes:**
```sql
SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
       ad_group_criterion.quality_info.quality_score,
       ad_group_criterion.quality_info.creative_quality_score,
       ad_group_criterion.quality_info.post_click_quality_score,
       ad_group_criterion.quality_info.search_predicted_ctr,
       campaign.name, ad_group.name,
       metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.ctr
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
```

**Comparação período a período** — rode a mesma query duas vezes com `segments.date BETWEEN 'YYYY-MM-DD' AND 'YYYY-MM-DD'` e compare, em vez de confiar em campos de variação.

### Cuidados com GAQL
- `cost_micros` é micro-unidade: divida por 1.000.000.
- Métricas de impression share **não podem ser somadas nem promediadas ingenuamente** entre linhas: pondere por impressões ou trate por dia.
- `search_term_view` só tem dados dos últimos ~60 dias em muitas contas — não peça períodos longos demais.
- PMax não expõe termos de busca no `search_term_view`; use `campaign_search_term_insight`.
- Segmentar por `segments.date` multiplica linhas: agregue depois, não antes.

## Exports necessários no modo C (sem API)

Se não houver conexão, peça ao usuário o export exato. Sempre cite o caminho na interface:

| Análise | Export | Caminho no Google Ads |
|---|---|---|
| Termos de busca | Search terms report | Campanhas → Insights e relatórios → Termos de pesquisa |
| Orçamento / IS | Campaign report com colunas de impression share e segmentação por dia | Campanhas → colunas: Competitive metrics |
| Anúncios | Ad report com headlines/descrições e Ad strength | Anúncios e assets → Anúncios |
| Keywords | Keyword report com Quality Score e componentes | Keywords de pesquisa → colunas: Quality Score |
| Segmentos | Relatório segmentado por dispositivo / geo / hora | Segmentar no relatório desejado |

Peça CSV ou XLSX com cabeçalho e sem linha de total. Avise que o período do export precisa bater com o período da análise.

## Regras invariantes

1. **Declare o período e a conta** em todo entregável. Análise sem período é inútil.
2. **Nunca misture períodos** em uma mesma tabela sem rotular.
3. **Moeda**: use a moeda da conta, nunca converta silenciosamente.
4. **Fuso horário**: os dados seguem o fuso da conta; se o usuário perguntar "hoje", confirme qual fuso.
5. **Dados parciais**: o dia corrente e, dependendo da janela de atribuição, os últimos 1–7 dias de conversão estão incompletos. Sinalize isso sempre que a conclusão depender do período recente.
