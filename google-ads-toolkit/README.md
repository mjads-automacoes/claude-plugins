# Google Ads Toolkit

Plugin de gestão e otimização de campanhas Google Ads para Claude (Cowork / Code / Dispatch).

## Arquitetura

Três camadas. Skills de **conhecimento** contêm a metodologia e são carregadas pelo Claude automaticamente; skills de **operação** são os fluxos que você invoca; a camada de **infraestrutura** define acesso a dados e segurança.

```
INFRAESTRUTURA
├── acesso-dados ................... contrato de dados (MCP, API ou CSV) + padrões GAQL
├── seguranca-aprovacoes ........... risco, preview, aprovação, execução, reversão
└── convencoes-conta ............... contexto da conta (PERSONALIZE PRIMEIRO)

CONHECIMENTO (o Claude carrega sozinho)
├── metodologia-termos-busca ....... relevância, taxonomia, match type de negativo
├── metodologia-orcamento-lances ... IS por orçamento vs rank, tCPA/tROAS, aprendizado
├── principios-anuncios ............ RSA, cobertura, alinhamento, Ad strength
└── analise-performance ............ decomposição, causa raiz, significância

OPERAÇÃO (você invoca)
├── /minerar-termos ................ negativos + oportunidades → CSV para o Editor
├── /otimizar-orcamento ............ IS por dia → proposta de orçamento com projeção
├── /auditar-anuncios .............. auditoria de RSA + copy nova pronta para upload
├── /investigar-campanha ........... causa raiz de queda de conversão ou alta de CPA
├── /auditar-estrutura ............. conta inteira: config, nomenclatura, keywords, negativos
├── /expandir-palavras-chave ....... novas keywords com origem e confiança rotuladas
├── /analise-segmentos ............. dispositivo, geo, hora, dia, rede, audiência
├── /revisar-pmax .................. asset groups, sinais, exclusão de marca, canibalização
├── /checagem-diaria ............... anomalias; silencioso quando está tudo normal
├── /revisao-semanal ............... o ritual principal + plano de 5 ações
└── /relatorio-mensal .............. relatório de negócio, opcionalmente como artifact
```

## Princípios de design

1. **Agnóstico à fonte de dados.** Nenhuma skill de análise assume um MCP específico. `acesso-dados` resolve entre API conectada, leitura conectada ou CSV exportado. Trocar a conexão depois não exige reescrever nada.
2. **Nada é executado sem "sim".** Toda mutação passa por `seguranca-aprovacoes`: preview com estado atual → estado futuro, risco classificado, execução em lotes, verificação posterior e `historico-alteracoes`.
3. **Todo entregável é auditável.** Cada linha de CSV carrega o porquê. Você revisa a lógica e faz override antes de qualquer coisa chegar à conta.
4. **Relevância acima de contagem.** Termo on-theme sem conversão não é negativo; é um problema de anúncio ou página a investigar.
5. **Sem volume, sem conclusão.** Cada skill tem limiar de significância explícito, e "não há dado suficiente" é uma resposta aceitável.
6. **Uma alavanca por vez.** Não mexer em orçamento e lance na mesma campanha no mesmo movimento — caso contrário o resultado fica ilegível.

## Como começar

1. **Preencha `skills/convencoes-conta/SKILL.md`.** É o passo que transforma análise genérica em análise correta. Todos os `<preencher>` importam — especialmente KPI alvo, nomenclatura e vocabulário do negócio.
2. **Rode `/auditar-estrutura`** para o raio-x inicial da conta.
3. **Rode `/minerar-termos`** para o dinheiro parado mais óbvio.
4. **Estabeleça a cadência**: `/checagem-diaria` diário, `/revisao-semanal` semanal, `/relatorio-mensal` mensal.

## Conexão com o Google Ads

Ainda em aberto — o plugin funciona nos três modos descritos em `acesso-dados`:

- **A — MCP próprio**: servidor falando com a Google Ads API oficial (precisa de developer token, OAuth client e customer ID). Único modo com o loop completo de escrita.
- **B — MCP de terceiros**: mais rápido de instalar, limitado às ferramentas que o servidor expõe.
- **C — CSV exportado**: sem credencial nenhuma; você exporta, o plugin analisa e devolve CSVs prontos para o Editor.

As skills já estão escritas para os três. A decisão pode ser tomada depois sem retrabalho.

## Estrutura de saída

Todos os entregáveis vão para `outputs/`:

```
outputs/
├── termos-negativos-AAAA-MM-DD.csv .......... negativos prontos para o Editor
├── termos-oportunidades-AAAA-MM-DD.csv ...... keywords a promover/realocar
├── recomendacoes-orcamento-AAAA-MM-DD.csv ... proposta de orçamento com projeção
├── auditoria-anuncios-AAAA-MM-DD.csv ........ achados por ad group
├── anuncios-novos-AAAA-MM-DD.csv ............ RSAs prontos para importar
├── auditoria-estrutura-AAAA-MM-DD.csv ....... achados de conta por severidade
├── expansao-palavras-chave-AAAA-MM-DD.csv ... keywords novas com lance sugerido
├── analise-segmentos-AAAA-MM-DD.csv ......... desperdício por segmento
├── auditoria-pmax-AAAA-MM-DD.csv ............ achados de Performance Max
├── metricas-semanais-AAAA-MM-DD.csv ......... placar da semana
├── metricas-mensais-AAAA-MM.csv ............. placar do mês
├── revisao-semanal-AAAA-MM-DD.md
├── relatorio-mensal-AAAA-MM.md
└── historico-alteracoes-AAAA-MM-DD.csv ...... tudo que foi executado na conta
```

## Premissas assumidas na v0.1.0

Estas foram escolhas padrão feitas na construção; ajuste em `convencoes-conta` conforme a conta real:

- Campanhas de Search e Performance Max
- KPI duplo: CPA para geração de leads, ROAS para e-commerce — a skill detecta qual usar pelo que estiver preenchido
- Toda mutação exige aprovação explícita (sem autonomia parcial)
- Outputs em português, CSVs no formato do Google Ads Editor
- Limiares de significância genéricos de mercado (100 cliques para keyword, 30 conversões para lance)
