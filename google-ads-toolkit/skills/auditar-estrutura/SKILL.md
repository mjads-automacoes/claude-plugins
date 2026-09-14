---
name: auditar-estrutura
description: Auditoria de estrutura da conta — nomenclatura, organizacao de campanhas e ad groups, match types, canibalizacao e duplicidade de keywords, cobertura de negativos, segmentacao e configuracoes de risco. Aciona em "auditar conta", "estrutura", "match type", "keywords duplicadas", "canibalizacao", "organizar campanhas", "conta nova".
version: 0.1.0
---

# Auditoria de Estrutura

Carregue `acesso-dados` e `convencoes-conta`. Esta é a skill de entrada para uma conta nova: rode antes de otimizar qualquer coisa, porque otimizar sobre estrutura errada desperdiça trabalho.

## Escopo

### 1. Configurações de conta e campanha (achados de risco)
Verifique e sinalize:
- **Rede de pesquisa com parceiros** e **Display expansion** ativados em campanhas de Search — costumam gastar mal.
- **Segmentação de localização**: "presença ou interesse" vs "presença" — a primeira traz tráfego fora da área.
- **Rotação de anúncios** em configuração não otimizada.
- **Idioma** incompatível com o público.
- **Programação de anúncios** inexistente quando o negócio só atende em horário comercial.
- **Ações de conversão**: quais contam como principais, duplicidade, contagem (uma vs todas), janela de atribuição.
- **Campanhas sem negativos**, campanhas sem extensões, ad groups sem anúncio ativo.
- **Orçamentos compartilhados** que mascaram limitação individual.
- **Campanhas ativas sem gasto** e **campanhas pausadas com orçamento alocado**.

### 2. Nomenclatura
Compare os nomes com o padrão de `convencoes-conta`. Liste as campanhas fora do padrão e proponha o nome corrigido. Se a conta não tem padrão nenhum, proponha um e mostre o antes/depois completo.

Nomenclatura não é cosmética: sem tema legível no nome, toda análise de relevância de termo de busca fica cega.

### 3. Organização
- Ad groups com **temas misturados** (keywords que não pertencem ao mesmo tema). Regra prática: se você não consegue escrever uma headline que sirva para todas as keywords do ad group, ele está misturado.
- Ad groups com **excesso de keywords** (> 20 costuma indicar mistura).
- Campanhas com **um único ad group** gigante.
- **Marca e não-marca na mesma campanha** — separe sempre; misturar distorce toda métrica agregada.
- Campanhas com orçamento irrisório que nunca sairão do aprendizado.

### 4. Keywords
- **Duplicadas** entre ad groups/campanhas (mesma keyword, mesmo match type) — canibalização direta.
- **Canibalização por sobreposição**: match amplo em um ad group capturando termos que pertencem a outro. Cruze com o relatório de termos de busca para evidenciar.
- **Distribuição de match types**: quanto do gasto está em amplo, frase e exato. Amplo dominante sem lance automatizado e sem negativos robustos é achado de alto risco.
- **Keywords com gasto e zero conversão** acima do limiar de `convencoes-conta`.
- **Keywords com Quality Score baixo** e qual componente está puxando para baixo.
- **Keywords pausadas que ainda têm histórico relevante** (candidatas a reativação).

### 5. Negativos
- Existe lista compartilhada? Está aplicada em todas as campanhas?
- Negativos que **bloqueiam tráfego bom** (conflito entre negativo e keyword ativa) — este é o achado mais perigoso e mais comum. Cruze cada negativo contra as keywords ativas e reporte todo conflito.
- Cobertura por tema: emprego, gratuito, acadêmico, concorrentes, DIY.

### 6. Cobertura
- Temas do negócio sem campanha correspondente (compare com o vocabulário de `convencoes-conta`).
- Geos atendidos sem cobertura.
- Ausência de remarketing/RLSA quando há volume.

## Entrega

1. **Placar**: nº de achados por severidade (Crítico / Alto / Médio / Baixo) e quanto de gasto mensal está exposto a achados críticos e altos.
2. **Top 10 achados por impacto financeiro**, cada um com: o que é, evidência numérica, ação recomendada, esforço e risco.
3. **Seções detalhadas** por escopo acima.
4. **Plano de correção em 3 ondas**: (1) risco imediato e dinheiro parado, (2) estrutura e keywords, (3) cobertura e expansão.
5. `outputs/auditoria-estrutura-YYYY-MM-DD.csv` — `Severity,Area,Entity Type,Entity,Finding,Evidence,Monthly Spend Affected,Recommended Action,Effort,Risk`

## Regras
- Todo achado precisa de evidência numérica; "poderia ser melhor" não é achado.
- Reestruturação é risco alto: nunca execute sem plano escrito, aprovação explícita e sem avisar que a conta reentra em aprendizado.
- Priorize sempre por gasto afetado, não por quantidade de achados.
- Conflito de negativo com keyword ativa é sempre Crítico.
