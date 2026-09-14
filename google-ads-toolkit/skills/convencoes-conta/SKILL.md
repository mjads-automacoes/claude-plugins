---
name: convencoes-conta
description: Convencoes da conta — nomenclatura de campanhas e ad groups, estrutura esperada, KPIs alvo, acoes de conversao validas, limiares de decisao e vocabulario do negocio. Carregue antes de qualquer analise para interpretar nomes corretamente. Aciona em "nomenclatura", "estrutura da conta", "o que significa essa campanha", "qual o CPA alvo", "meta".
version: 0.1.0
---

# Convenções da Conta

> **Este é o arquivo que você personaliza primeiro.** Ele é o contexto que transforma análise genérica em análise correta para esta conta. Onde houver `<preencher>`, pergunte ao usuário na primeira execução e atualize este arquivo.

## Identificação

- **Conta / Customer ID:** `<preencher>`
- **MCC:** `<preencher — ou "não aplicável">`
- **Moeda:** `<preencher>`
- **Fuso horário da conta:** `<preencher>`
- **Modelo de negócio:** `<lead gen | e-commerce | ambos | outro>`
- **O que é vendido:** `<preencher>`
- **Ticket médio / valor de um lead:** `<preencher>`
- **Ciclo de venda:** `<preencher — dias entre clique e receita>`

## Nomenclatura

Padrão esperado de nome de campanha:

```
<Canal> - <Tipo> - <Tema/Produto> - <Geo> - <Observação>
Ex.: Search - Use Case - Meeting Notes - BR - Exact
```

Padrão de ad group:

```
<Tema específico> [- <Match type> se separado por match]
Ex.: Meeting Transcription
```

Ao ler um nome de campanha, extraia sempre: **canal**, **tipo de campanha**, **tema** e **geo**. O tema é o que define se um termo de busca é on-theme — sem isso, a mineração de termos vira chute.

Se a conta não seguir um padrão, registre aqui o mapeamento real observado (nome → significado) na primeira auditoria, e sinalize a inconsistência como achado de `auditar-estrutura`.

### Marcadores comuns e o que significam
- `Brand` — tráfego de marca própria. Trate separadamente em toda análise de eficiência; misturar marca com não-marca distorce CPA e ROAS.
- `Competitor` — campanhas de concorrente. CPA naturalmente maior; não aplique o mesmo limiar.
- `Generic` / `Non-brand` — aquisição fria.
- `RMKT` / `RLSA` — remarketing.
- `PMax` — Performance Max.
- `Test` / `Exp` — campanha experimental; não otimize sem perguntar.

## KPIs e metas

| Segmento | KPI primário | Meta | Limite aceitável |
|---|---|---|---|
| Marca | `<CPA/ROAS>` | `<preencher>` | `<preencher>` |
| Não-marca | `<CPA/ROAS>` | `<preencher>` | `<preencher>` |
| Remarketing | `<CPA/ROAS>` | `<preencher>` | `<preencher>` |
| Conta (agregado) | `<CPA/ROAS>` | `<preencher>` | `<preencher>` |

- **Orçamento mensal alvo:** `<preencher>`
- **Sazonalidade conhecida:** `<preencher — meses fortes/fracos, eventos>`

## Conversões

- **Ações que contam como conversão principal:** `<preencher>`
- **Ações que são secundárias (observar, não otimizar):** `<preencher>`
- **Janela de atribuição:** `<preencher>`
- **Modelo de atribuição:** `<preencher>`
- **Há importação de conversão offline / CRM?** `<preencher>`

Regra: quando a conta tiver conversões secundárias contando na coluna "Conversions", **toda análise de CPA precisa dizer explicitamente quais ações estão sendo contadas.** Caso contrário, as conclusões não são comparáveis com o que o usuário vê no CRM.

## Limiares de decisão (defaults — ajuste por conta)

Estes são os números que evitam otimizar em cima de ruído:

- **Significância mínima para julgar uma keyword:** 100 cliques **ou** 3× o CPA alvo em gasto sem conversão.
- **Significância mínima para julgar um ad group:** 30 conversões no período, ou 1.000 cliques.
- **Gasto mínimo para um termo de busca entrar na análise:** 1 clique (mineração ampla) ou 0,5× o CPA alvo (mineração focada em desperdício).
- **Período padrão de análise:** últimos 30 dias; 90 dias para contas de baixo volume.
- **Período de aprendizado após mudança relevante:** 7–14 dias ou 30 conversões, o que vier depois.
- **Variação considerada ruído:** menos de 15% em métricas com base < 100 conversões.

## Vocabulário do negócio

Termos do setor que aparecem nas buscas e o que significam para esta conta — essencial para julgar relevância:

- **On-theme / qualificado:** `<preencher>`
- **Off-theme / desqualificado:** `<preencher>`
- **Concorrentes conhecidos:** `<preencher>`
- **Produtos/serviços que NÃO oferecemos** (fonte comum de desperdício): `<preencher>`
- **Sinônimos e variações que aceitamos:** `<preencher>`

## Preferências de entrega

- **Idioma dos relatórios:** português
- **Formato padrão dos entregáveis:** CSV pronto para Google Ads Editor, salvo em `outputs/`
- **Ferramenta de execução preferida:** `<Google Ads Editor | interface | API>`
- **Cadência:** `<diária | semanal | mensal — preencher>`
