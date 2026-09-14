---
name: analise-segmentos
description: Analisa performance por dispositivo, localizacao, horario, dia da semana, rede e audiencia para encontrar desperdicio concentrado e propor ajustes de lance ou exclusoes. Aciona em "dispositivo", "mobile", "geo", "localizacao", "horario", "dia da semana", "audiencia", "onde estou perdendo dinheiro".
version: 0.1.0
---

# Análise por Segmento

Carregue `acesso-dados`, `convencoes-conta` e `analise-performance`.

Segmentação é onde aparece desperdício que o agregado esconde. Também é onde mais se otimiza em cima de ruído — por isso os limiares de volume valem integralmente aqui.

## Segmentos a analisar

| Segmento | O que procurar | Ação típica |
|---|---|---|
| **Dispositivo** | Mobile com CPA muito acima do desktop (ou vice-versa) | Ajuste de lance por dispositivo; investigar landing page mobile |
| **Localização** | Regiões fora da área atendida com gasto; cidades com CPA discrepante | Exclusão de geo; ajuste de lance por região |
| **Hora do dia** | Gasto fora do horário de atendimento sem conversão | Programação de anúncios; ajuste por horário |
| **Dia da semana** | Fim de semana com CPA muito pior | Ajuste por dia; ou aceitar se o volume compensa |
| **Rede** | Parceiros de pesquisa e Display com performance inferior | Desativar parceiros/expansão |
| **Audiência** | Segmentos em observação com performance destacada | Promover a segmentação; ajuste de lance |
| **Idade/gênero** (quando disponível) | Faixas com desperdício claro | Exclusão |

## Método

1. **Um segmento por vez.** Cruzar dois segmentos fatia o dado até virar ruído — só cruze quando cada célula tiver volume suficiente.
2. **Volume mínimo por célula**: 30 conversões ou 1.000 cliques. Abaixo disso, escreva "sem volume para conclusão" e não proponha ajuste.
3. **Compare contra a média da conta**, não contra a meta absoluta — o que importa é a diferença relativa entre segmentos.
4. **Quantifique o desperdício**: para cada segmento ruim, calcule quanto foi gasto e quantas conversões teria produzido no CPA médio. Isso transforma "mobile é pior" em "R$ 4.200/mês em mobile com CPA 2,1× a média".
5. **Cuidado com o mix**: um segmento pode parecer pior porque concentra tráfego não-marca. Cheque a composição antes de concluir.
6. **Cuidado com lance automatizado**: em estratégias automatizadas, ajustes por dispositivo/horário são ignorados ou têm efeito limitado (exceto exclusões com −100%). Diga isso explicitamente antes de propor ajustes; nesse caso, a alavanca correta é exclusão ou segmentação, não modificador.

## Entrega

1. **Tabela por segmento**: `Segmento | Custo | % do gasto | Cliques | Conv. | CPA | Índice vs média | Volume suficiente?`
2. **Desperdício quantificado** por segmento, em R$/mês.
3. **Ajustes propostos**: modificador ou exclusão, com o valor exato e a justificativa numérica.
4. **Ressalvas**: estratégia de lance em uso e o que isso limita; segmentos sem volume.
5. `outputs/analise-segmentos-YYYY-MM-DD.csv` — `Segment Type,Segment,Campaign,Cost,Clicks,Conversions,CPA,Index vs Account,Sufficient Volume,Recommended Action,Rationale`
6. Oferta de execução com aprovação explícita (exclusão de geo e desativação de rede são risco médio; mudança de programação é risco médio).

## Regras
- Nunca proponha ajuste de lance baseado em célula com menos de 30 conversões.
- Nunca exclua um geo sem confirmar com o usuário que a área não é atendida — pode ser região atendida com landing page ruim.
- Sempre reporte o percentual do gasto total que cada segmento representa; um segmento ruim com 0,5% do gasto não é prioridade.
