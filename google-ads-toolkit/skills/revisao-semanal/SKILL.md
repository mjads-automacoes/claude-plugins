---
name: revisao-semanal
description: Revisao semanal completa da conta — performance versus semana anterior e meta, higiene de termos de busca, orcamento e impression share, anuncios, segmentos, e uma lista priorizada de acoes para a semana. Aciona em "revisao semanal", "como foi a semana", "weekly", "relatorio da semana", "o que fazer essa semana".
version: 0.1.0
---

# Revisão Semanal

O ritual principal da conta. Carregue `acesso-dados`, `convencoes-conta`, `analise-performance`, `metodologia-termos-busca` e `metodologia-orcamento-lances`.

Período padrão: últimos 7 dias completos vs os 7 anteriores. Exclua o dia corrente.

## Roteiro

### 1. Placar
Conta inteira e por campanha: custo, impressões, cliques, CTR, CPC, conversões, taxa de conversão, CPA, valor de conversão, ROAS. Sempre com a variação absoluta e percentual contra a semana anterior, e contra a meta de `convencoes-conta`.

Separe **marca** e **não-marca** — o agregado sem essa separação não serve para decidir nada.

### 2. O que explica a variação
Aplique a decomposição de `analise-performance`. Uma frase por movimento relevante, com o número que a sustenta. Ignore variações dentro do ruído e diga que são ruído em vez de narrá-las.

### 3. Higiene de termos de busca
Passada rápida de `metodologia-termos-busca` nos termos não acionados da semana, ordenados por gasto. Reporte: gasto em termos não acionados, quanto é desperdício claro, os 5 piores. Se o volume justificar, indique rodar `/minerar-termos` completo.

### 4. Orçamento e impression share
Por campanha: IS, perdido por orçamento, perdido por rank. Identifique estranguladas dentro da meta (escalar) e limitadas mas ineficientes (corrigir). Aplique `metodologia-orcamento-lances`.

### 5. Anúncios
Ad groups com anúncio reprovado, ad group sem anúncio ativo, e os 3 ad groups com pior CTR relativo entre os de maior gasto. Detalhe fica para `/auditar-anuncios`.

### 6. Segmentos
Uma passada rápida em dispositivo e geo procurando desperdício concentrado. Só reporte o que tiver volume.

### 7. Alterações da semana
O que foi mexido, quando, e qual foi o efeito observável. Isto fecha o ciclo: toda mudança da semana anterior precisa ter sua leitura aqui. Inclua o resultado das mudanças que estavam em janela de observação.

### 8. Plano da semana
Lista priorizada por impacto em dinheiro. Cada item com: ação, motivo com número, impacto estimado, esforço, risco e a skill que executa.

Máximo de 5 itens. Mais que isso não é plano, é lista de desejos.

## Entrega

```
REVISÃO SEMANAL — <conta> — <período> vs <período anterior>

RESUMO EXECUTIVO
<3 a 5 linhas: o que aconteceu, por quê, e o que fazer>

PLACAR
<tabela conta + por campanha, com variação e vs meta>

MARCA vs NÃO-MARCA
<tabela>

O QUE EXPLICA
<decomposição>

HIGIENE DE TERMOS
<gasto não acionado, desperdício, top 5>

ORÇAMENTO E IMPRESSION SHARE
<tabela + leitura>

ANÚNCIOS E SEGMENTOS
<achados com volume suficiente>

EFEITO DAS MUDANÇAS DA SEMANA PASSADA
<o que foi feito, o que aconteceu>

PLANO DA SEMANA (máx. 5)
1. <ação> — <motivo com número> — impacto <R$> — risco <x> — /<skill>
```

Salve em `outputs/revisao-semanal-YYYY-MM-DD.md` e gere `outputs/metricas-semanais-YYYY-MM-DD.csv` com o placar.

## Regras
- Nunca reporte variação percentual sem a base absoluta.
- Nunca narre ruído como se fosse tendência.
- Toda ação proposta precisa apontar para a skill que a executa.
- Se uma campanha estiver em aprendizado, diga antes de comentar o resultado dela.
- O resumo executivo é a parte que será lida: escreva-o por último e com cuidado.
