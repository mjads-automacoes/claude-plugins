# Servidor MCP — Google Ads

Conecta o plugin à Google Ads API oficial. Implementa o contrato definido em
`skills/acesso-dados/SKILL.md`.

## Segurança em três camadas

1. **Escrita desligada por padrão.** Sem `GOOGLE_ADS_ALLOW_WRITE=true` no `.env`, as
   ferramentas de mutação recusam a execução.
2. **Dry run por padrão.** Toda mutação roda com `validate_only` até você passar
   `dry_run=False` explicitamente.
3. **Nada é removido.** Só existe pausar e reativar. Remoção nem sequer foi implementada,
   porque nem sempre é reversível.

Além disso, o servidor recusa por conta própria: variação de orçamento acima de 30% e
alteração de orçamento compartilhado.

Suas credenciais ficam no `.env` local. **Nunca cole o conteúdo do `.env` numa conversa.**

## Instalação

```bash
cd mcp-server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Configuração

### 1. Developer token
No **MCC** → Ferramentas e configurações → Configuração → **Central de API**.

Verifique o **nível de acesso**:
- `Test Account` — só consulta contas de teste. Conta real retorna erro.
- `Basic` ou `Standard` — consulta contas reais. É o que você precisa.

Se estiver em Test, solicite Basic pelo formulário da própria Central de API.

### 2. OAuth client
Google Cloud Console → APIs e serviços → Credenciais → Criar credenciais →
**ID do cliente OAuth** → tipo **App para computador**.

Ative também a **Google Ads API** na biblioteca de APIs do projeto.

### 3. Refresh token
```bash
cp .env.example .env
```
Preencha `GOOGLE_ADS_CLIENT_ID` e `GOOGLE_ADS_CLIENT_SECRET`, então:
```bash
python gerar_refresh_token.py
```
Autorize no navegador e copie o token para o `.env`.

### 4. IDs das contas
- `GOOGLE_ADS_LOGIN_CUSTOMER_ID` — o MCC, sem hífens
- `GOOGLE_ADS_CUSTOMER_ID` — a conta a gerenciar, sem hífens

## Registrar no Claude

Adicione ao arquivo de configuração de MCP do Claude Desktop
(`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "google-ads": {
      "command": "C:\\Users\\Maquina 01\\claude-plugins\\google-ads-toolkit\\mcp-server\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\Maquina 01\\claude-plugins\\google-ads-toolkit\\mcp-server\\server.py"]
    }
  }
}
```

Reinicie o Claude. Teste com: *"chame write_status"* — deve responder se a escrita está
habilitada e qual conta está configurada. Depois: *"liste minhas contas do Google Ads"*.

## Ferramentas

### Leitura
| Ferramenta | Para quê |
|---|---|
| `list_accounts` | Contas acessíveis pelo MCC |
| `run_gaql` | Qualquer consulta GAQL livre |
| `get_campaigns` | Campanhas com métricas, orçamento e IS |
| `get_search_terms` | Termos de busca não acionados, por gasto |
| `get_keywords` | Keywords com Quality Score e componentes |
| `get_negative_keywords` | Negativos existentes (checar conflitos) |
| `get_ads` | RSAs com headlines, ad strength e aprovação |
| `get_impression_share_by_day` | IS por campanha por dia |
| `get_metrics_by_segment` | device, date, day_of_week, hour, network, geo |
| `get_change_history` | Alterações recentes na conta |
| `get_conversion_actions` | Ações de conversão e atribuição |

### Escrita
| Ferramenta | Guarda-corpo |
|---|---|
| `add_negative_keywords` | Exige `ad_group_id` ou `campaign_id` explícito |
| `update_campaign_budget` | Recusa > 30%; recusa orçamento compartilhado |
| `set_status` | Só ENABLED/PAUSED; remoção não existe |
| `write_status` | Diagnóstico, sem efeito colateral |

## Ordem recomendada de teste

1. `GOOGLE_ADS_ALLOW_WRITE=false` — rode a semana inteira só lendo.
2. Valide os outputs do plugin contra o que você vê na interface do Google Ads.
3. Só então ligue a escrita, e comece pela mutação de menor risco: negativos exatos
   em nível de ad group, com `dry_run=True`.
4. Depois do primeiro dry run limpo, aplique de verdade um lote pequeno.

## Problemas comuns

| Erro | Causa |
|---|---|
| `DEVELOPER_TOKEN_NOT_APPROVED` | Token em nível Test tentando ler conta real |
| `USER_PERMISSION_DENIED` | Falta `GOOGLE_ADS_LOGIN_CUSTOMER_ID`, ou o usuário do OAuth não tem acesso à conta |
| `CUSTOMER_NOT_FOUND` | Customer ID com hífen, ou conta errada |
| `invalid_grant` | Refresh token revogado — gere outro |
| Servidor não aparece no Claude | Caminho do Python errado no JSON, ou faltou reiniciar |
