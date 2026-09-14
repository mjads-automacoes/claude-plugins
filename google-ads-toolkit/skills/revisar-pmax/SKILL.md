---
name: revisar-pmax
description: Revisao de campanhas Performance Max — grupos de ativos, performance por asset, temas de busca, sinais de audiencia, exclusoes de marca, canibalizacao com Search e insights de categoria de busca. Aciona em "PMax", "Performance Max", "grupo de ativos", "asset group", "temas de busca", "canibalizacao PMax".
version: 0.1.0
---

# Revisão de Performance Max

Carregue `acesso-dados`, `convencoes-conta`, `principios-anuncios` e `metodologia-orcamento-lances`.

PMax dá menos controle e menos visibilidade. A gestão acontece em quatro alavancas: **ativos**, **sinais**, **exclusões** e **dados de conversão**. Nunca prometa granularidade de Search aqui.

## O que revisar

### 1. Grupos de ativos
Para cada asset group, verifique cobertura conforme `principios-anuncios`: headlines curtas (3–5), longas (5), descrições (5), imagens (≥ 20 em proporções variadas), vídeo (≥ 1 — se não fornecer, o Google gera um fraco), logo.

Reporte a performance por ativo (Baixo / Bom / Melhor) e proponha substituição dos "Baixo" **apenas** com volume suficiente. Asset group com "Anúncio incompleto" é achado Alto.

### 2. Temas de busca e sinais de audiência
- Os temas de busca refletem os temas reais do negócio de `convencoes-conta`?
- Os sinais de audiência estão preenchidos (dados próprios, público personalizado, interesses)?
- Lembre: sinais **direcionam**, não limitam. Trate como orientação e diga isso ao usuário quando ele esperar segmentação rígida.

### 3. Insights de categoria de busca
Use `campaign_search_term_insight` para ver as categorias que geram tráfego. Procure categorias claramente off-theme e quantifique o gasto. A ação possível é negativo em nível de campanha/conta, conforme o acesso disponível.

### 4. Exclusão de marca
Verifique se há lista de exclusão de marca aplicada. Sem ela, PMax tende a canibalizar tráfego de marca e inflar artificialmente o resultado. Este é um achado Alto quando a conta tem campanha de marca em Search.

### 5. Canibalização com Search
Compare a evolução de impressões/cliques/conversões das campanhas de Search de mesmo tema desde o início do PMax. Se o Search caiu na mesma proporção em que o PMax cresceu, o ganho pode ser transferência, não incremento. Reporte como hipótese com o dado, não como conclusão definitiva — a atribuição entre campanhas é limitada.

### 6. Dados de conversão
PMax depende inteiramente da qualidade do sinal de conversão. Verifique: conversões principais corretas, valores de conversão realistas, ausência de conversões secundárias infladas (ex.: pageview contando como conversão). Sinal ruim = otimização ruim, e nenhuma alavanca criativa corrige isso.

### 7. Orçamento e alvo
Aplique `metodologia-orcamento-lances`. PMax precisa de volume para aprender: orçamento muito baixo mantém a campanha em aprendizado permanente. Sinalize quando o orçamento for insuficiente para o CPA alvo (regra prática: orçamento diário < 3× o CPA alvo é arriscado).

## Entrega

1. **Resumo por campanha PMax**: gasto, conversões, CPA/ROAS vs meta, status de aprendizado.
2. **Achados por severidade**, com gasto afetado.
3. **Tabela de asset groups**: cobertura de ativos, ativos "Baixo", achados.
4. **Categorias de busca off-theme** com gasto.
5. **Hipótese de canibalização** com o dado comparativo.
6. `outputs/auditoria-pmax-YYYY-MM-DD.csv` — `Campaign,Asset Group,Area,Severity,Finding,Evidence,Spend Affected,Recommended Action`
7. Oferta de execução com aprovação explícita — **toda mudança em PMax é risco alto** por causa do reaprendizado.

## Regras
- Não prometa termos de busca individuais em PMax.
- Não recomende pausar PMax sem análise de canibalização e sem plano de para onde o orçamento vai.
- Mudanças em asset group reiniciam aprendizado: agrupe as mudanças em um único movimento em vez de pingar alterações.
