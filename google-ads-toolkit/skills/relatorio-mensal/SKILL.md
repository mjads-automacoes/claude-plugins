---
name: relatorio-mensal
description: Relatorio mensal para stakeholder ou cliente — resultado versus meta e versus mes anterior, evolucao, o que foi feito e o que gerou efeito, aprendizados e plano do proximo mes, opcionalmente publicado como artifact visual. Aciona em "relatorio mensal", "fechamento do mes", "relatorio para o cliente", "apresentacao de resultados".
version: 0.1.0
---

# Relatório Mensal

Carregue `acesso-dados`, `convencoes-conta` e `analise-performance`.

Público: quem paga a conta, não quem opera. Escreva em linguagem de negócio — dinheiro, leads, receita — e deixe jargão de plataforma para os anexos.

## Conteúdo

### 1. Resultado
Mês fechado vs mês anterior **e** vs mesmo mês do ano anterior (quando houver dado). Métricas: investimento, cliques, conversões, CPA, receita e ROAS quando aplicável.

Sempre contra a meta de `convencoes-conta`. Se bateu, diga por quanto; se não bateu, diga por quanto e por quê — sem rodeio.

### 2. Evolução
Série mensal dos últimos 6–12 meses das métricas principais, para dar contexto de tendência e sazonalidade. Uma tendência de 6 meses diz mais que uma variação de 30 dias.

### 3. Onde o dinheiro foi
Distribuição do investimento por campanha/tipo, com o resultado de cada uma. Separe marca e não-marca.

### 4. O que foi feito e o que deu resultado
Liste as mudanças relevantes do mês (do `historico-alteracoes`) e o efeito observado de cada uma. Este é o item que justifica a gestão — e o único jeito honesto de fazê-lo é comparar antes e depois com o dado.

Onde o efeito não pôde ser isolado, diga isso.

### 5. Aprendizados
2–4 conclusões que mudam a operação do próximo mês. Aprendizado real, não repetição de número.

### 6. Plano do próximo mês
3–5 iniciativas priorizadas, com objetivo, alavanca, investimento previsto e resultado esperado. Inclua as premissas.

### 7. Riscos e dependências
O que pode derrubar o plano: sazonalidade, orçamento, landing page, estoque, capacidade de atendimento dos leads, pendência de dado de conversão.

## Entrega

Salve `outputs/relatorio-mensal-YYYY-MM.md` e o CSV de apoio `outputs/metricas-mensais-YYYY-MM.csv`.

**Ofereça publicar como artifact visual** quando o relatório for para apresentar a alguém: uma página com o placar, os gráficos de evolução, a distribuição de investimento e o plano. Ofereça em uma linha; só construa se o usuário aceitar. Ao construir, siga as diretrizes de design de artifact e de visualização de dados disponíveis na sessão.

## Regras
- Nunca apresente só o que foi bem. Relatório que esconde o que piorou destrói confiança quando o dado aparece depois.
- Nunca atribua todo o resultado à gestão: separe efeito de sazonalidade, de investimento e de otimização, quando possível — e diga quando não for possível.
- Números de conversão devem bater com a fonte que o stakeholder usa (CRM, plataforma de e-commerce). Se houver divergência conhecida entre Google Ads e CRM, declare-a no topo do relatório em vez de deixar a pessoa descobrir sozinha.
- Sem jargão sem tradução: "impression share" vira "participação nas buscas disponíveis".
