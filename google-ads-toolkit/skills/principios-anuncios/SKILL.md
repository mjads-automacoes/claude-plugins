---
name: principios-anuncios
description: Principios de escrita e avaliacao de anuncios responsivos de pesquisa (RSA) e assets de PMax — cobertura de headlines, alinhamento keyword-anuncio-landing page, diferenciacao, CTA, extensoes e leitura correta de Ad strength. Aciona em "anuncio", "RSA", "headline", "copy", "criativo", "ad strength", "descricao", "extensoes", "assets".
version: 0.1.0
---

# Princípios de Anúncio

## O que um bom RSA faz

Um anúncio existe para fazer três coisas, nesta ordem: **confirmar** que a pessoa está no lugar certo, **diferenciar** de quem aparece ao lado, e **dar o próximo passo**. Copy que não faz a primeira não adianta fazer as outras.

### Alinhamento (o eixo mais importante)
A cadeia precisa fechar: **termo de busca → keyword → headline → landing page**. Quebra em qualquer elo derruba CTR, Quality Score e taxa de conversão. Ao auditar um anúncio, sempre verifique:
- O tema do ad group aparece literalmente em pelo menos 2 headlines?
- A promessa do anúncio existe na landing page? (se a URL final não puder ser verificada, sinalize como não verificado)
- A oferta do anúncio é a mesma da página?

## Estrutura recomendada de RSA

**Headlines: use 12–15.** Nunca menos de 8. Distribua por função:

| Função | Quantidade | Conteúdo |
|---|---|---|
| Relevância ao tema | 3–4 | Contém a keyword/tema do ad group |
| Benefício / resultado | 3 | O que a pessoa ganha, não o que o produto tem |
| Diferenciação | 2–3 | Por que nós e não o concorrente |
| Prova / credibilidade | 1–2 | Números, clientes, garantia, avaliação |
| CTA | 1–2 | Ação explícita |
| Preço / oferta / condição | 1–2 | Quando aplicável |

**Descrições: 4.** Duas expandindo o benefício principal, uma com prova/objeção, uma com CTA + condição.

**Paths:** 2 caminhos, com o tema do ad group. `/{tema}/{acao}`.

### Fixação (pinning)
- Fixe **apenas** o que for obrigatório: marca, exigência legal, preço regulado.
- Fixar demais mata o teste de combinações e derruba Ad strength.
- Se fixar posição 1, tenha pelo menos 3 opções fixadas naquela posição.
- Fixação total (todas as posições) transforma o RSA em anúncio estático — só faça com justificativa explícita.

## Como ler Ad strength (e como não ler)

Ad strength mede **diversidade e quantidade de assets**, não qualidade persuasiva. Um anúncio "Excelente" pode vender mal e um "Bom" pode ser o melhor da conta.

Regra: use Ad strength como **checklist de cobertura**, nunca como métrica de performance. A métrica de performance é CTR, taxa de conversão e CPA — sempre comparados contra os outros anúncios do **mesmo ad group** e no mesmo período.

Sinalize Ad strength "Ruim"/"Médio" como *achado de cobertura*, e diga exatamente o que falta (headlines insuficientes, headlines repetitivas, falta de keyword, fixação excessiva).

## Checklist de auditoria de anúncio

Para cada ad group, verifique:

1. **Quantidade de anúncios**: ideal 2–3 RSAs ativos por ad group. Um só = sem teste. Mais de 3 = diluição de dados.
2. **Contagem de assets**: headlines ≥ 8 (ideal 12+), descrições = 4.
3. **Unicidade**: headlines que dizem a mesma coisa com palavras diferentes contam como uma. Sinalize redundância.
4. **Keyword nas headlines**: o tema do ad group aparece?
5. **Fixação**: há pinning desnecessário?
6. **CTA presente** em headline e descrição.
7. **Diferenciação**: existe algo que o concorrente não poderia copiar e colar? Se toda headline for genérica ("Qualidade e Confiança"), isso é um achado.
8. **Extensões/assets em nível de campanha**: sitelinks (≥ 4), callouts (≥ 4), snippets estruturados, chamada, formulário de lead, imagem. Faltantes são achado.
9. **URL final e tracking**: URLs quebradas ou inconsistentes entre anúncios do mesmo ad group.
10. **Consistência com a oferta atual**: promoção vencida no texto é erro grave e urgente.

## Regras de escrita

- **Escreva benefício, não característica.** "Transcrição em 2 minutos" vence "Tecnologia de transcrição avançada".
- **Número concreto vence adjetivo.** "Mais de 3.000 empresas" vence "Muitas empresas".
- **Uma ideia por headline.** Headline com duas ideias separadas por "e" perde força quando combinada com outras.
- **Respeite limites**: headline 30 caracteres, descrição 90, path 15. Conte sempre e mostre a contagem ao propor copy.
- **Sem superlativo não comprovável** ("o melhor do mercado") — além de fraco, pode ser reprovado.
- **Sem pontuação excessiva, caixa alta ou emoji** — risco de reprovação.
- **Português correto e natural.** Copy traduzida ao pé da letra é detectável e converte pior.
- **Não prometa o que a landing page não entrega.**

## Teste de anúncio

- Teste **uma variável por vez**: ângulo de benefício, ou prova, ou CTA — não os três.
- Rode até volume mínimo: 100 cliques por anúncio, ou 30 conversões no ad group.
- Compare anúncios apenas dentro do mesmo ad group e mesmo período.
- Nunca pause o anúncio perdedor antes do volume mínimo; variação inicial é ruído.
- Ao substituir, mantenha o vencedor e introduza **um** desafiante.

## Performance Max — assets

- Cada grupo de ativos precisa de: 3–5 headlines curtas, 5 longas, 5 descrições, ≥ 20 imagens em proporções variadas, ≥ 1 vídeo (se não fornecer, o Google gera um fraco automaticamente), logo.
- Avalie performance por ativo (Baixo/Bom/Melhor) e substitua os "Baixo" — mas só com volume suficiente.
- Temas de busca e sinais de audiência direcionam, não limitam; trate como orientação, não como segmentação rígida.
