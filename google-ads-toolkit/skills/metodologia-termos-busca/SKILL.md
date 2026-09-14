---
name: metodologia-termos-busca
description: Metodologia de avaliacao de termos de busca — como decidir negativar, manter ou promover um termo com base em relevancia ao tema da campanha, nao apenas em contagem de conversoes. Define taxonomia de motivos, escolha de match type do negativo e nivel de aplicacao. Aciona em "termos de pesquisa", "palavras negativas", "search terms", "minerar", "gasto desperdicado", "queries irrelevantes", "oportunidade de keyword".
version: 0.1.0
---

# Metodologia de Mineração de Termos de Busca

O objetivo **não é** "zero conversões = ruim". O objetivo é **relevância ao tema da campanha**. Um termo on-theme sem conversão pode ser problema de anúncio, landing page ou volume — negativá-lo esconde o problema real. Um termo off-theme com conversão pode ser uma conversão acidental que está contaminando o aprendizado do lance.

## Abordagem central

1. **Filtre para termos não acionados** — apenas `status = NONE` (ainda não adicionado como keyword nem como negativo). Termos já tratados só poluem a lista.
2. **Ordene por gasto decrescente** — priorize onde o dinheiro está indo. Um termo com 200 cliques a R$ 0,10 importa menos que um com 20 cliques a R$ 5,00.
3. **Cruze três coisas em cada candidato:**
   - o **termo de busca** (o que a pessoa digitou)
   - a **keyword que casou** (o que disparou o anúncio)
   - a **campanha + ad group** (em que tema aquilo vive)

   A pergunta é sempre: *este termo pertence a este tema?*

O cruzamento é o que separa esta metodologia de uma planilha ordenada por custo. Sem olhar a keyword que casou, você não enxerga *por que* o termo entrou — e é isso que define qual negativo resolve o problema sem colateral.

## Avaliação de relevância

Toda avaliação cai em uma de quatro caixas:

### 1. Negativo claro
O termo não tem nada a ver com o que o ad group vende, ou sinaliza intenção errada. Negativar é seguro e imediato.

### 2. Negativo por intenção
O termo é topicamente próximo, mas a intenção não é de compra/contratação. Exemplos: pesquisa acadêmica, vaga de emprego, tutorial, "como fazer manualmente", download gratuito. Negativar, mas registrar o motivo — volume alto aqui costuma indicar que o match type está largo demais.

### 3. Realocação (não é negativo puro)
O termo é relevante para o negócio, mas está no ad group **errado**. A ação correta é dupla: negativar no ad group atual **e** adicionar como keyword no ad group certo. Nunca apenas negativar, ou você perde tráfego bom.

### 4. Manter
On-theme para este ad group. Mantenha mesmo com zero conversões — a relevância manda mais que a contagem de conversões isolada. Se o gasto for alto e a conversão zero, isso vira um achado para `investigar-campanha` (anúncio, landing page, oferta), não um negativo.

### Caso especial: promover a keyword
Termo on-theme com desempenho **acima** da média do ad group (CPA melhor ou taxa de conversão maior, com volume mínimo). Vale adicionar como keyword exata para ganhar controle de lance e anúncio dedicado. Regra de corte: pelo menos 2 conversões, ou volume de cliques ≥ 30 com CTR acima da média do ad group.

## Taxonomia de motivos (use exatamente estes rótulos)

Todo termo negativado recebe **um** motivo. A consistência aqui é o que permite o relatório por categoria.

| Rótulo | Significado |
|---|---|
| `intencao_errada` | Busca não é comercial: informacional, tutorial, "grátis", "como fazer" |
| `intencao_emprego` | Vaga, salário, carreira, "trabalhar em" |
| `pesquisa_academica` | Estudo, artigo, definição, "o que é" |
| `marca_concorrente` | Nome de concorrente — navegacional, não comparativo |
| `produto_nao_ofertado` | Produto/serviço adjacente que não vendemos |
| `fora_do_tema` | Topicamente sem relação com o ad group |
| `ad_group_errado` | Relevante ao negócio, mas pertence a outro ad group (gera também uma adição) |
| `generico_demais` | Muito amplo para o ad group; não dá para inferir intenção |
| `geo_fora_de_area` | Localidade fora da área atendida |
| `publico_errado` | Segmento que não compramos (ex.: revenda, estudante, DIY) |
| `desenvolvedor_tecnico` | Intenção de código/integração quando não vendemos para dev |
| `comparador` | "X vs Y", "alternativa a", quando essa é intenção que não convertemos |

Quando um termo caberia em dois rótulos, escolha o **mais específico** — `intencao_emprego` antes de `intencao_errada`.

## Escolha do match type do negativo

Esta decisão é onde mais se erra. Regra:

- **Negativo exato** — padrão. Use quando o termo específico é o problema. Zero risco de colateral.
- **Negativo de frase** — use quando um **token recorrente** está causando desperdício em muitos termos (ex.: "grátis", "vaga", "curso"). Exige que você tenha visto o padrão em pelo menos 3 termos distintos.
- **Negativo amplo** — raro; só para tokens inequivocamente ruins em qualquer contexto.

Antes de propor qualquer negativo de frase ou amplo, **verifique colateral**: rode o token contra a lista de keywords ativas e contra os termos que convertem. Se ele aparece em algo que converte, rebaixe para exato. Declare essa verificação no relatório.

## Nível de aplicação

- **Ad group** — quando o termo é ruim *para aquele tema* mas bom em outro (caso 3).
- **Campanha** — quando é ruim para toda a campanha.
- **Lista compartilhada de negativos** — quando é ruim para a conta inteira (ex.: "vaga", "grátis", concorrentes). Use listas temáticas: `NEG - Emprego`, `NEG - Gratuito`, `NEG - Concorrentes`, `NEG - Academico`.

Nunca aplique em nível de conta a partir de uma análise de campanha única.

## Padrões a procurar além de termo a termo

Ao terminar a passada linha a linha, suba um nível e procure:

1. **Tokens recorrentes** — qual palavra aparece em mais termos negativados? Isso vira negativo de frase ou lista compartilhada.
2. **Keyword vazando** — qual keyword está casando com mais termos ruins? Candidata a restringir o match type ou a receber negativos no ad group.
3. **Ad group com má mira** — se mais de 30% do gasto em termos não acionados de um ad group é off-theme, o problema é estrutural, não de negativos.
4. **Termos duplicados entre ad groups** — canibalização; vira achado de `auditar-estrutura`.
5. **Concentração** — quanto do desperdício total está nos 10 primeiros termos? Se for a maior parte, a ação é curta e de alto impacto.

## Performance Max

PMax não expõe termos individuais em `search_term_view`. Use `campaign_search_term_insight`, que agrupa por categoria. Consequências:
- A análise é por **categoria**, não por termo.
- Negativos em PMax dependem do nível de acesso da conta (lista de negativos em nível de campanha/conta).
- Não prometa granularidade que a API não entrega: diga explicitamente que PMax é analisado por categoria.

## O que nunca fazer

- Negativar em massa por "zero conversões" sem olhar relevância.
- Propor negativo de frase sem checar colateral.
- Negativar um termo de marca própria.
- Negativar termo que já converteu, sem sinalizar explicitamente e pedir confirmação.
- Tratar termo com 1 clique e R$ 0,40 como prioridade — ordene por dinheiro.
