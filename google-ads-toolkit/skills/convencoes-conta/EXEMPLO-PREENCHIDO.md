# EXEMPLO PREENCHIDO — não é uma conta real

> Este arquivo existe apenas como **referência de formato**. Os dados abaixo são fictícios,
> de uma empresa inventada, para mostrar o nível de detalhe que o `SKILL.md` precisa.
> Nenhuma skill lê este arquivo. Copie o padrão para `SKILL.md` com os dados reais.

---

## Identificação

- **Conta / Customer ID:** Clínica Vitale — 123-456-7890
- **MCC:** não aplicável
- **Moeda:** BRL
- **Fuso horário da conta:** America/Sao_Paulo
- **Modelo de negócio:** geração de leads
- **O que é vendido:** consultas e procedimentos de odontologia estética — clareamento, lentes de contato dental, implante
- **Ticket médio / valor de um lead:** ticket médio R$ 4.800; ~18% dos leads fecham → lead vale ~R$ 864
- **Ciclo de venda:** 12 a 30 dias entre o clique e o fechamento

## Nomenclatura

```
Search - Servico - Lentes de Contato Dental - SP Capital - Exact
Search - Marca - Clinica Vitale - SP Capital - Todas
PMax  - Geral - SP Capital
```

Ad groups nomeados pelo tema específico: `Lentes de Contato Dental`, `Facetas de Porcelana`, `Clareamento a Laser`.

Marcadores em uso: `Marca`, `Servico`, `Concorrente`, `RMKT`, `PMax`.

## KPIs e metas

| Segmento | KPI primário | Meta | Limite aceitável |
|---|---|---|---|
| Marca | CPA | R$ 45 | R$ 70 |
| Não-marca | CPA | R$ 180 | R$ 260 |
| Remarketing | CPA | R$ 90 | R$ 140 |
| Conta (agregado) | CPA | R$ 150 | R$ 220 |

- **Orçamento mensal alvo:** R$ 42.000
- **Sazonalidade conhecida:** dezembro e janeiro fracos (férias); março, abril, setembro e outubro fortes; pico antes de datas de casamento e formatura

## Conversões

- **Ações principais:** `Formulário - Agendamento`, `WhatsApp - Clique com contato iniciado`, `Ligação > 60s`
- **Ações secundárias (observar, não otimizar):** `Visualizou preços`, `Scroll 75%`
- **Janela de atribuição:** 30 dias de clique, 1 dia de visualização
- **Modelo de atribuição:** baseado em dados
- **Conversão offline / CRM:** sim — RD Station importa `Lead Qualificado` e `Venda Fechada` com 7 dias de atraso

> Atenção recorrente desta conta: o CRM mostra ~30% menos leads que o Google Ads, porque
> `WhatsApp - Clique` conta o clique e não a conversa iniciada. Declarar essa diferença
> em todo relatório para o cliente.

## Limiares de decisão

- **Julgar keyword:** 80 cliques, ou R$ 540 de gasto sem conversão (3× o CPA alvo de não-marca)
- **Julgar ad group:** 25 conversões no período
- **Gasto mínimo para termo entrar na análise:** 1 clique
- **Período padrão:** últimos 30 dias
- **Aprendizado após mudança:** 14 dias
- **Ruído:** variação menor que 15% com base abaixo de 100 conversões

## Vocabulário do negócio

- **On-theme / qualificado:** buscas por procedimento estético dental com intenção de contratar — "lente de contato dental preço", "quanto custa faceta", "dentista estética SP", "clareamento a laser perto de mim"
- **Off-theme / desqualificado:** ortodontia, aparelho, canal, extração, urgência odontológica, odontologia pelo SUS ou convênio
- **Concorrentes conhecidos:** Sorriso Perfeito, OdontoArt, Clínica Bellagio, Smile Design SP
- **Serviços que NÃO oferecemos:** aparelho ortodôntico, tratamento de canal, cirurgia bucomaxilo, atendimento por convênio, atendimento infantil
- **Sinônimos aceitos:** "lente de contato dental" = "faceta" = "laminado cerâmico"; "clareamento" = "branqueamento"

> As duas linhas acima — o que não vendemos e os concorrentes — são as que mais geram
> negativos em `/minerar-termos`. Vale caprichar nelas.

## Preferências de entrega

- **Idioma:** português
- **Formato padrão:** CSV para Google Ads Editor em `outputs/`
- **Execução preferida:** Google Ads Editor para lotes grandes; API para ajustes pontuais
- **Cadência:** `/checagem-diaria` toda manhã, `/revisao-semanal` segunda-feira, `/relatorio-mensal` no dia 3
