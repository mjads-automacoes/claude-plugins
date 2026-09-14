---
name: auditar-anuncios
description: Audita anuncios responsivos de pesquisa e assets por ad group — cobertura de headlines, alinhamento com keywords, fixacao, extensoes e performance relativa — e entrega copy nova pronta para upload. Aciona em "auditar anuncios", "revisar copy", "meus RSAs", "ad strength", "melhorar anuncio", "escrever headlines".
version: 0.1.0
---

# Auditar Anúncios

Carregue `acesso-dados`, `convencoes-conta` e `principios-anuncios`.

## Argumentos
`$ARGUMENTS` pode conter campanha, ad group ou foco ("só os de pior CTR", "reescreva os fracos"). Padrão: campanhas ativas de Search, últimos 30 dias.

## Passos

### 1. Puxar anúncios e contexto
Para cada ad group ativo: RSAs com headlines, descrições, paths, URL final, pinning, ad strength, status; métricas por anúncio (impressões, cliques, CTR, conversões, CPA, custo); keywords do ad group; extensões/assets em nível de campanha e ad group.

### 2. Auditar cobertura
Aplique o checklist de `principios-anuncios` em cada ad group. Registre cada achado com **severidade**:

| Severidade | Exemplos |
|---|---|
| **Crítico** | Ad group sem anúncio ativo; URL quebrada; promoção vencida no texto; anúncio reprovado |
| **Alto** | < 8 headlines; apenas 1 RSA no ad group; keyword do tema ausente das headlines; fixação total |
| **Médio** | < 12 headlines; < 4 descrições; headlines redundantes; faltam sitelinks/callouts; sem CTA |
| **Baixo** | Paths não usados; falta snippet estruturado; oportunidade de prova/número |

### 3. Auditar alinhamento
Para cada ad group, verifique a cadeia keyword → headline → landing page. Liste os ad groups onde a keyword principal não aparece em nenhuma headline — costuma ser o achado de maior impacto em CTR e Quality Score. Se não for possível verificar a landing page, marque como "não verificado" em vez de assumir.

### 4. Auditar performance relativa
Compare anúncios **dentro do mesmo ad group**, mesmo período. Só declare vencedor/perdedor com ≥ 100 cliques por anúncio; abaixo disso, escreva "sem volume". Nunca use Ad strength como métrica de performance — apenas como checklist de cobertura.

### 5. Propor copy
Para cada ad group com achado Crítico ou Alto, escreva um RSA completo:
- 12–15 headlines distribuídas pelas funções da tabela de `principios-anuncios`
- 4 descrições
- 2 paths
- contagem de caracteres ao lado de cada linha
- indicação do que fixar (e por quê) — por padrão, nada

Escreva em português natural, com benefício concreto e número quando existir. Não invente prova social, preço, prazo ou garantia: onde faltar informação, use `<placeholder>` e peça o dado ao usuário.

### 6. Entregar

1. **Resumo**: ad groups auditados, achados por severidade, gasto que está por trás dos ad groups com achado crítico/alto.
2. **Tabela de achados**: `Campanha | Ad Group | Severidade | Achado | Gasto 30d | Ação recomendada`, ordenada por gasto.
3. **Copy proposta** por ad group prioritário.
4. **Arquivos**:
   - `outputs/auditoria-anuncios-YYYY-MM-DD.csv` — `Campaign,Ad Group,Ad ID,Severity,Finding,Detail,Spend,CTR,CPA,Recommended Action`
   - `outputs/anuncios-novos-YYYY-MM-DD.csv` — formato de importação do Google Ads Editor: `Campaign,Ad Group,Headline 1..15,Description 1..4,Path 1,Path 2,Final URL`
5. **Oferta de execução** com aprovação explícita (criar RSA é risco médio; nunca pause o anúncio antigo antes do novo acumular volume).

## Regras
- Respeite os limites de caracteres e sempre mostre a contagem.
- Uma variável por teste; não substitua o anúncio vencedor.
- Nunca prometa o que a landing page não entrega.
- Ad group com um único RSA nunca deve ter esse RSA pausado — adicione o novo ao lado.
