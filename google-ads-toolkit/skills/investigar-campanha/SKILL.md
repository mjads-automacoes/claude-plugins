---
name: investigar-campanha
description: Diagnostico de causa raiz quando uma campanha muda de comportamento — queda de conversoes, alta de CPA, perda de volume ou gasto fora do esperado. Percorre rastreamento, historico de alteracoes, decomposicao de metricas e segmentacoes ate isolar a causa. Aciona em "por que caiu", "o que houve com a campanha", "CPA disparou", "parou de converter", "investigar".
version: 0.1.0
---

# Investigar Campanha

Carregue `acesso-dados`, `convencoes-conta` e `analise-performance`.

## Argumentos
`$ARGUMENTS` deve conter a campanha e, idealmente, o sintoma e quando começou. Se não vier o sintoma, pergunte antes de gastar consultas: *o que mudou, e desde quando você notou?*

## Roteiro de investigação

Siga **nesta ordem** e reporte o resultado de cada etapa, inclusive as que descartaram hipóteses.

### 1. Enquadrar
Defina o período "antes" e o período "depois" com o mesmo tamanho e mesma composição de dias da semana. Puxe a série diária da campanha (custo, impressões, cliques, CTR, CPC, conversões, taxa de conversão, CPA, valor) e identifique visualmente **o dia da virada**. Uma quebra abrupta e uma erosão gradual têm causas diferentes.

### 2. O dado é real?
- Conversões caíram a zero ou quase? Suspeite de rastreamento antes de qualquer coisa: ações de conversão ativas, contagem, mudanças recentes no site/tag.
- O período recente está incompleto pela janela de atribuição? Se sim, diga quanto do "efeito" pode ser artefato.
- Alguma ação de conversão foi adicionada/removida da coluna principal?

### 3. Alguém mexeu?
Consulte o histórico de alterações cobrindo de 14 dias antes da virada até hoje. Liste toda alteração relevante com data e tipo, e cruze com o dia da virada. Mudanças de orçamento, alvo, estratégia de lance, keywords, anúncios e segmentação são as suspeitas primárias.

### 4. Decompor
Aplique a decomposição de `analise-performance`: o CPA subiu por CPC ou por taxa de conversão? O volume caiu por impressões ou por CTR? Mostre a conta explicitamente, com os dois períodos lado a lado.

### 5. Localizar
Desça o funil até achar onde a variação está concentrada: campanha → ad group → keyword → termo de busca. Reporte quanto da variação total cada nível explica. Em geral poucas entidades explicam a maior parte.

### 6. Mix
Cheque marca vs não-marca, dispositivo, geo, hora/dia da semana e rede. Uma métrica agregada piora sem nenhuma parte piorar quando o peso entre as partes muda — verifique isso antes de concluir.

### 7. Competição e entrega
- `search_impression_share`, perdido por orçamento e por rank, antes e depois.
- Quality Score e componentes, antes e depois.
- Se o IS caiu e o rank_lost subiu: pressão de leilão ou queda de qualidade.
- Se o IS caiu e o budget_lost subiu: restrição de orçamento (ou o CPC subiu e o mesmo orçamento compra menos).

### 8. Externo
Só depois de esgotar o interno: sazonalidade (compare ano contra ano), feriados, mudanças de mercado. Nunca comece por aqui — é a hipótese preguiçosa.

## Entrega

```
INVESTIGAÇÃO — <campanha> — <período>

SINTOMA
<uma frase com número>

CAUSA RAIZ
<causa isolada, com a evidência que a sustenta>
Confiança: <alta | média | baixa>

O QUE FOI DESCARTADO
- <hipótese> — descartada porque <evidência>

CADEIA DE EVIDÊNCIA
<tabela antes vs depois com as métricas decompostas>

AÇÕES RECOMENDADAS (por impacto)
1. <ação> — impacto estimado, risco, reversão
...

OBSERVAR
<métrica, prazo, e o que indicaria que a hipótese estava errada>
```

Se a causa **não** foi isolada, diga isso na seção CAUSA RAIZ, liste as hipóteses sobreviventes e, para cada uma, o dado que faltaria para decidir. Não invente uma causa para fechar o relatório.

## Regras
- Nunca proponha ação corretiva antes de isolar a causa.
- Nunca atribua a "sazonalidade" ou "concorrência" sem evidência comparativa.
- Se a campanha estiver em aprendizado, diga isso antes de qualquer conclusão.
- Se a variação estiver dentro do ruído estatístico, a resposta correta é "não houve mudança significativa" — e essa é uma resposta válida e útil.
