---
name: seguranca-aprovacoes
description: Protocolo obrigatorio antes de qualquer alteracao na conta Google Ads. Define classificacao de risco, formato do preview, aprovacao explicita, execucao em lotes, verificacao pos-mutacao e registro de alteracoes. Carregue antes de executar qualquer mutacao. Aciona em "aplicar", "adicionar negativos", "mudar orcamento", "pausar", "executar", "subir alteracoes".
version: 0.1.0
---

# Protocolo de Segurança e Aprovação

Regra central: **nada é alterado na conta sem um "sim" explícito do usuário para aquele lote específico.** Nunca interprete uma pergunta analítica ("vale a pena aumentar o orçamento?") como autorização para executar.

## Classificação de risco

| Nível | Ações | Exigência |
|---|---|---|
| **Baixo** | Adicionar negativos exatos, criar labels, adicionar keywords pausadas | Preview + sim para o lote |
| **Médio** | Adicionar keywords ativas, ajustar orçamento ≤ 20%, pausar keyword individual, editar RSA existente | Preview item a item + sim + plano de reversão |
| **Alto** | Trocar estratégia de lance, alterar tCPA/tROAS, orçamento > 20%, pausar campanha ou ad group, negativos amplos/phrase em nível de conta, mexer em PMax | Preview + justificativa + impacto estimado + sim + janela de observação definida |
| **Proibido sem pedido direto e inequívoco** | Remover (não pausar) qualquer entidade, apagar listas de negativos, alterar conversões e atribuição, mexer em faturamento, alterar acesso de usuários | Recusar por padrão e explicar o risco |

Escalone um nível quando: a conta for nova para você, o gasto diário da campanha for alto em relação à conta, ou o período analisado tiver menos de 7 dias ou menos de 30 conversões.

## Formato obrigatório do preview

Antes de executar, apresente sempre:

```
ALTERAÇÕES PROPOSTAS — <conta> — <data>
Risco: <baixo|médio|alto>   Itens: <n>   Impacto estimado: <gasto/mês afetado>

1. <entidade> · <ação> · <de> → <para>
   Por quê: <razão em uma linha, ancorada em dado>
   Reverter: <como desfazer>
...

Confirma a execução destes <n> itens? Responda "sim" para executar ou indique quais remover.
```

Regras do preview:
- **Sempre mostre o estado atual e o estado futuro.** "Aumentar orçamento" não é preview; "R$ 6.800 → R$ 8.160/dia" é.
- **Toda linha tem um porquê ancorado em número.** Se você não consegue citar o dado, a alteração não deve estar na lista.
- Se houver mais de 25 itens, agrupe por campanha/ad group e mostre o resumo por grupo + os 10 de maior impacto, com o restante em arquivo anexo.
- Some o impacto: quanto de gasto mensal está sob essas mudanças.

## Execução

1. Execute **um lote por vez**, na ordem de menor para maior risco.
2. Confirme cada lote antes do próximo quando houver risco médio ou alto.
3. Se qualquer item do lote falhar, **pare**, reporte o que passou e o que falhou, e não prossiga para o próximo lote sem nova instrução.
4. Nunca "conserte" silenciosamente um erro de API com uma ação diferente da aprovada.

## Verificação pós-mutação

Depois de executar, sempre:
- Releia as entidades alteradas na conta e confirme o novo estado (não confie no retorno da chamada).
- Reporte: `<n> aplicados · <n> falharam · <n> ignorados`.
- Grave um registro em `outputs/historico-alteracoes-YYYY-MM-DD.csv` com colunas: `timestamp, conta, entidade, tipo_entidade, acao, valor_anterior, valor_novo, motivo, aprovado_por, resultado`.
- Defina a janela de observação: o que olhar, quando, e qual sinal indicaria reverter.

## Reversão

Toda proposta de risco médio ou alto precisa de um caminho de reversão declarado **antes** da execução. Em caso de reversão, use o `historico-alteracoes` como fonte dos valores anteriores. Prefira sempre pausar em vez de remover — pausado é reversível, removido nem sempre.

## Limites que nunca devem ser cruzados sem pedido explícito e específico

- Não alterar mais de uma alavanca de uma vez na mesma campanha (orçamento **e** lance **e** estrutura), porque isso destrói a leitura do resultado.
- Não aplicar mudanças de lance/orçamento em campanha que teve alteração estrutural nos últimos 7 dias sem sinalizar o ruído.
- Não adicionar negativos em nível de conta a partir de uma análise de campanha única.
- Não mexer em campanha que está em período de aprendizado sem dizer explicitamente que ela está aprendendo e o que isso implica.
