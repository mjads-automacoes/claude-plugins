---
name: expandir-palavras-chave
description: Encontra novas keywords a partir de termos de busca que performam, lacunas de cobertura tematica e variacoes de match type, e define em qual ad group cada uma entra com qual lance. Aciona em "novas keywords", "expandir", "crescer", "cobertura de palavras", "adicionar palavras-chave", "oportunidades".
version: 0.1.0
---

# Expansão de Keywords

Carregue `acesso-dados`, `convencoes-conta` e `metodologia-termos-busca`.

Expansão só faz sentido depois que o desperdício está controlado. Se `minerar-termos` ainda não rodou nesta conta, diga isso e sugira a ordem correta.

## Fontes de oportunidade (nesta ordem de confiança)

### 1. Termos de busca que já performam
A fonte mais confiável, porque é dado da própria conta. Critério para promover a keyword exata:
- ≥ 2 conversões no período, **ou**
- ≥ 30 cliques com CTR acima da média do ad group e CPA dentro da meta.

Promover dá controle de lance e permite anúncio dedicado. Para cada promoção, defina: ad group de destino, match type (exato por padrão), lance inicial (o CPC médio atual do termo) e se precisa de anúncio específico.

### 2. Termos on-theme no ad group errado
Saída da etapa de Realocação de `minerar-termos`: adicionar no ad group certo **e** negativar no errado. Sempre as duas ações juntas.

### 3. Lacunas temáticas
Compare o vocabulário do negócio de `convencoes-conta` com os temas cobertos por ad groups existentes. Temas do negócio sem cobertura viram propostas de novo ad group (e às vezes de nova campanha).

### 4. Variações estruturais
Para keywords que já performam bem: variações de match type (exata que merece frase), singular/plural, sinônimos do setor, modificadores comerciais ("preço", "contratar", "software de"), variações regionais e erros de digitação frequentes.

### 5. Concorrentes e comparação
Só se a conta já tem campanha de concorrente ou se o usuário autorizar. CPA naturalmente pior; use limiar próprio.

## Regras de adição

- **Nunca adicione keyword que já existe** na conta em qualquer ad group — cheque duplicidade antes. Duplicata é canibalização.
- **Nunca adicione keyword cujo tema conflita com um negativo existente** — cheque conflito antes e reporte.
- **Uma keyword, um ad group.** Se duas keywords exigem anúncios diferentes, são dois ad groups.
- **Match amplo só com lance automatizado e negativos robustos.** Caso contrário, exato e frase.
- **Ad group novo precisa de anúncio novo.** Nunca proponha ad group sem propor o RSA correspondente (chame `auditar-anuncios` para gerar).
- Lance inicial: para keywords promovidas, use o CPC médio histórico do termo; para keywords novas sem histórico, use o CPC médio do ad group de destino.

## Entrega

1. **Resumo**: nº de oportunidades, volume/gasto que elas já representam hoje (no caso de termos promovidos), receita ou conversões estimadas.
2. **Tabela priorizada**: `Keyword sugerida | Match | Ad Group destino | Origem | Cliques/Conv. históricas | CPA histórico | Lance sugerido | Confiança`.
3. **Lacunas temáticas** com proposta de estrutura (campanha/ad group/keywords/anúncio).
4. `outputs/expansao-palavras-chave-YYYY-MM-DD.csv` — formato de importação do Editor:
```
Campaign,Ad Group,Keyword,Match Type,Max CPC,Source,Historical Clicks,Historical Conversions,Historical CPA,Rationale,Confidence
```
5. **Ações acopladas**: lista dos negativos que precisam ser criados junto (casos de realocação).
6. Oferta de execução com aprovação explícita.

## Regras de honestidade
- Distinga claramente oportunidade **com dado da conta** (alta confiança) de oportunidade **por inferência temática** (baixa confiança). Rotule cada linha.
- Não estime volume de busca sem fonte; se não houver dado de planejador, diga que a estimativa não está disponível.
- Não proponha centenas de keywords: proponha as que você consegue justificar. Lista longa sem justificativa é ruído caro.
