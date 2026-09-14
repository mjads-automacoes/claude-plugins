"""
Servidor MCP para Google Ads.

Expoe as capacidades definidas em skills/acesso-dados/SKILL.md:
leitura via GAQL e mutacoes (desativadas por padrao).

Seguranca:
  - Escrita so funciona com GOOGLE_ADS_ALLOW_WRITE=true no .env.
  - Nenhuma ferramenta remove entidades; apenas pausa (reversivel).
  - Toda mutacao roda em validate_only quando dry_run=True (padrao).
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("google-ads")

MICROS = 1_000_000
ALLOW_WRITE = os.getenv("GOOGLE_ADS_ALLOW_WRITE", "false").lower() == "true"
DEFAULT_CUSTOMER_ID = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "")

_client = None


def get_client():
    """Cria o cliente da Google Ads API a partir das variaveis de ambiente."""
    global _client
    if _client is None:
        from google.ads.googleads.client import GoogleAdsClient

        required = [
            "GOOGLE_ADS_DEVELOPER_TOKEN",
            "GOOGLE_ADS_CLIENT_ID",
            "GOOGLE_ADS_CLIENT_SECRET",
            "GOOGLE_ADS_REFRESH_TOKEN",
        ]
        missing = [k for k in required if not os.getenv(k)]
        if missing:
            raise RuntimeError(
                "Faltam variaveis no .env: " + ", ".join(missing)
                + ". Veja mcp-server/README.md."
            )

        config: dict[str, Any] = {
            "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
            "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
            "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
            "use_proto_plus": True,
        }
        if os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"):
            config["login_customer_id"] = _clean_id(
                os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"]
            )
        _client = GoogleAdsClient.load_from_dict(config)
    return _client


def _clean_id(customer_id: str) -> str:
    """Remove hifens do customer ID (123-456-7890 -> 1234567890)."""
    return customer_id.replace("-", "").replace(" ", "").strip()


def _resolve_customer_id(customer_id: str | None) -> str:
    cid = customer_id or DEFAULT_CUSTOMER_ID
    if not cid:
        raise ValueError(
            "Nenhum customer_id informado e GOOGLE_ADS_CUSTOMER_ID nao esta no .env."
        )
    return _clean_id(cid)


def _flatten(obj: Any, prefix: str = "") -> dict[str, Any]:
    """Achata o dict aninhado da API em chaves com ponto."""
    out: dict[str, Any] = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                out.update(_flatten(value, new_prefix))
            else:
                out[new_prefix] = value
    else:
        out[prefix] = obj
    return out


def _humanize(row: dict[str, Any]) -> dict[str, Any]:
    """Converte micros em unidade monetaria, mantendo o campo original."""
    for key in list(row.keys()):
        if key.endswith("_micros") and isinstance(row[key], (int, float)):
            row[key.replace("_micros", "")] = round(row[key] / MICROS, 2)
    return row


def _run_query(customer_id: str, query: str, limit: int | None = None) -> list[dict]:
    client = get_client()
    service = client.get_service("GoogleAdsService")
    rows: list[dict] = []
    for batch in service.search_stream(customer_id=customer_id, query=query):
        for row in batch.results:
            record = _humanize(_flatten(type(row).to_dict(row)))
            rows.append(record)
            if limit and len(rows) >= limit:
                return rows
    return rows


def _require_write(action: str) -> None:
    if not ALLOW_WRITE:
        raise PermissionError(
            f"Escrita desativada. '{action}' foi bloqueado. "
            "Para habilitar, defina GOOGLE_ADS_ALLOW_WRITE=true no .env e reinicie o servidor."
        )


# ---------------------------------------------------------------- leitura


@mcp.tool()
def list_accounts() -> list[dict]:
    """Lista as contas acessiveis pelo MCC configurado (ID, nome, moeda, fuso)."""
    client = get_client()
    customer_service = client.get_service("CustomerService")
    resource_names = customer_service.list_accessible_customers().resource_names

    accounts = []
    for name in resource_names:
        cid = name.split("/")[-1]
        try:
            rows = _run_query(
                cid,
                """
                SELECT customer.id, customer.descriptive_name, customer.currency_code,
                       customer.time_zone, customer.manager, customer.test_account
                FROM customer LIMIT 1
                """,
            )
            accounts.extend(rows)
        except Exception as exc:  # conta sem permissao de leitura direta
            accounts.append({"customer.id": cid, "erro": str(exc)[:200]})
    return accounts


@mcp.tool()
def run_gaql(query: str, customer_id: str | None = None, limit: int = 1000) -> list[dict]:
    """Executa uma consulta GAQL arbitraria. Use para qualquer leitura nao coberta
    pelas ferramentas especificas. Campos *_micros vem tambem convertidos em moeda."""
    return _run_query(_resolve_customer_id(customer_id), query, limit)


@mcp.tool()
def get_campaigns(
    customer_id: str | None = None,
    date_range: str = "LAST_30_DAYS",
    include_paused: bool = False,
) -> list[dict]:
    """Campanhas com metricas, orcamento, estrategia de lance e impression share."""
    status = "" if include_paused else "AND campaign.status = 'ENABLED'"
    query = f"""
        SELECT campaign.id, campaign.name, campaign.status,
               campaign.advertising_channel_type, campaign.bidding_strategy_type,
               campaign_budget.amount_micros, campaign_budget.explicitly_shared,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.conversions_value, metrics.ctr,
               metrics.average_cpc, metrics.cost_per_conversion,
               metrics.search_impression_share,
               metrics.search_budget_lost_impression_share,
               metrics.search_rank_lost_impression_share
        FROM campaign
        WHERE segments.date DURING {date_range} {status}
        ORDER BY metrics.cost_micros DESC
    """
    return _run_query(_resolve_customer_id(customer_id), query)


@mcp.tool()
def get_search_terms(
    customer_id: str | None = None,
    date_range: str = "LAST_30_DAYS",
    min_clicks: int = 1,
    only_unactioned: bool = True,
    campaign_ids: list[str] | None = None,
    limit: int = 2000,
) -> list[dict]:
    """Termos de busca com a keyword que casou, campanha, ad group e metricas.
    Por padrao traz apenas termos nao acionados (status NONE), ordenados por gasto."""
    filters = [f"segments.date DURING {date_range}", f"metrics.clicks >= {min_clicks}"]
    if only_unactioned:
        filters.append("search_term_view.status = 'NONE'")
    if campaign_ids:
        ids = ", ".join(f"'{c}'" for c in campaign_ids)
        filters.append(f"campaign.id IN ({ids})")

    query = f"""
        SELECT search_term_view.search_term, search_term_view.status,
               segments.keyword.info.text, segments.keyword.info.match_type,
               campaign.id, campaign.name, ad_group.id, ad_group.name,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.conversions_value,
               metrics.ctr, metrics.average_cpc
        FROM search_term_view
        WHERE {' AND '.join(filters)}
        ORDER BY metrics.cost_micros DESC
    """
    return _run_query(_resolve_customer_id(customer_id), query, limit)


@mcp.tool()
def get_keywords(
    customer_id: str | None = None,
    date_range: str = "LAST_30_DAYS",
    limit: int = 2000,
) -> list[dict]:
    """Keywords ativas com Quality Score, componentes de qualidade e metricas."""
    query = f"""
        SELECT ad_group_criterion.criterion_id,
               ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
               ad_group_criterion.status,
               ad_group_criterion.quality_info.quality_score,
               ad_group_criterion.quality_info.creative_quality_score,
               ad_group_criterion.quality_info.post_click_quality_score,
               ad_group_criterion.quality_info.search_predicted_ctr,
               campaign.name, ad_group.id, ad_group.name,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.ctr, metrics.average_cpc
        FROM keyword_view
        WHERE segments.date DURING {date_range}
          AND ad_group_criterion.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
    """
    return _run_query(_resolve_customer_id(customer_id), query, limit)


@mcp.tool()
def get_negative_keywords(customer_id: str | None = None) -> list[dict]:
    """Negativos em nivel de campanha e de ad group. Use para checar conflitos
    antes de propor novos negativos."""
    cid = _resolve_customer_id(customer_id)
    campaign_negs = _run_query(
        cid,
        """
        SELECT campaign.id, campaign.name,
               campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
        FROM campaign_criterion
        WHERE campaign_criterion.negative = TRUE
          AND campaign_criterion.type = 'KEYWORD'
        """,
    )
    for row in campaign_negs:
        row["nivel"] = "campanha"

    adgroup_negs = _run_query(
        cid,
        """
        SELECT campaign.name, ad_group.id, ad_group.name,
               ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type
        FROM ad_group_criterion
        WHERE ad_group_criterion.negative = TRUE
          AND ad_group_criterion.type = 'KEYWORD'
        """,
    )
    for row in adgroup_negs:
        row["nivel"] = "ad_group"

    return campaign_negs + adgroup_negs


@mcp.tool()
def get_ads(customer_id: str | None = None, date_range: str = "LAST_30_DAYS") -> list[dict]:
    """Anuncios responsivos de pesquisa com headlines, descricoes, ad strength e metricas."""
    query = f"""
        SELECT ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad_strength,
               ad_group_ad.policy_summary.approval_status,
               ad_group_ad.ad.responsive_search_ad.headlines,
               ad_group_ad.ad.responsive_search_ad.descriptions,
               ad_group_ad.ad.responsive_search_ad.path1,
               ad_group_ad.ad.responsive_search_ad.path2,
               ad_group_ad.ad.final_urls,
               campaign.name, ad_group.id, ad_group.name,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.ctr
        FROM ad_group_ad
        WHERE segments.date DURING {date_range}
          AND ad_group_ad.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
    """
    return _run_query(_resolve_customer_id(customer_id), query)


@mcp.tool()
def get_impression_share_by_day(
    customer_id: str | None = None,
    date_range: str = "LAST_14_DAYS",
) -> list[dict]:
    """Impression share por campanha por dia: total, perdido por orcamento e perdido
    por rank. Base da analise de /otimizar-orcamento."""
    query = f"""
        SELECT campaign.id, campaign.name, segments.date,
               campaign_budget.amount_micros,
               metrics.search_impression_share,
               metrics.search_budget_lost_impression_share,
               metrics.search_rank_lost_impression_share,
               metrics.search_absolute_top_impression_share,
               metrics.impressions, metrics.clicks, metrics.cost_micros,
               metrics.conversions, metrics.conversions_value
        FROM campaign
        WHERE segments.date DURING {date_range}
          AND campaign.status = 'ENABLED'
        ORDER BY campaign.name, segments.date
    """
    return _run_query(_resolve_customer_id(customer_id), query)


@mcp.tool()
def get_metrics_by_segment(
    segment: str,
    customer_id: str | None = None,
    date_range: str = "LAST_30_DAYS",
) -> list[dict]:
    """Metricas segmentadas. segment: device, date, day_of_week, hour, network,
    geo ou conversion_action."""
    segment_map = {
        "device": "segments.device",
        "date": "segments.date",
        "day_of_week": "segments.day_of_week",
        "hour": "segments.hour",
        "network": "segments.ad_network_type",
        "conversion_action": "segments.conversion_action_name",
    }
    if segment == "geo":
        query = f"""
            SELECT campaign.name, geographic_view.country_criterion_id,
                   geographic_view.location_type,
                   metrics.impressions, metrics.clicks, metrics.cost_micros,
                   metrics.conversions, metrics.conversions_value
            FROM geographic_view
            WHERE segments.date DURING {date_range}
            ORDER BY metrics.cost_micros DESC
        """
    else:
        if segment not in segment_map:
            raise ValueError(
                f"Segmento invalido: {segment}. Use um de: "
                + ", ".join(list(segment_map) + ["geo"])
            )
        field = segment_map[segment]
        query = f"""
            SELECT campaign.name, {field},
                   metrics.impressions, metrics.clicks, metrics.cost_micros,
                   metrics.conversions, metrics.conversions_value, metrics.ctr
            FROM campaign
            WHERE segments.date DURING {date_range}
              AND campaign.status = 'ENABLED'
            ORDER BY metrics.cost_micros DESC
        """
    return _run_query(_resolve_customer_id(customer_id), query)


@mcp.tool()
def get_change_history(customer_id: str | None = None, days: int = 14) -> list[dict]:
    """Alteracoes recentes na conta. Primeira parada de /investigar-campanha:
    a causa mais comum de uma mudanca e outra mudanca."""
    from datetime import date, timedelta

    start = (date.today() - timedelta(days=days)).isoformat()
    end = date.today().isoformat()
    query = f"""
        SELECT change_event.change_date_time, change_event.change_resource_type,
               change_event.resource_change_operation, change_event.changed_fields,
               change_event.user_email, change_event.client_type,
               campaign.name, ad_group.name
        FROM change_event
        WHERE change_event.change_date_time >= '{start}'
          AND change_event.change_date_time <= '{end}'
        ORDER BY change_event.change_date_time DESC
        LIMIT 500
    """
    return _run_query(_resolve_customer_id(customer_id), query)


@mcp.tool()
def get_conversion_actions(customer_id: str | None = None) -> list[dict]:
    """Acoes de conversao: quais contam como principal, categoria e janela de atribuicao.
    Verifique isto antes de confiar em qualquer CPA."""
    query = """
        SELECT conversion_action.id, conversion_action.name,
               conversion_action.status, conversion_action.category,
               conversion_action.primary_for_goal,
               conversion_action.counting_type,
               conversion_action.click_through_lookback_window_days,
               conversion_action.view_through_lookback_window_days
        FROM conversion_action
        WHERE conversion_action.status != 'REMOVED'
    """
    return _run_query(_resolve_customer_id(customer_id), query)


# ---------------------------------------------------------------- escrita


@mcp.tool()
def add_negative_keywords(
    negatives: list[dict],
    customer_id: str | None = None,
    dry_run: bool = True,
) -> dict:
    """Adiciona palavras negativas.

    negatives: lista de {"text": str, "match_type": "EXACT"|"PHRASE"|"BROAD",
                         "ad_group_id": str} ou {"...", "campaign_id": str}
    dry_run=True valida na API sem gravar. Rode sempre com dry_run antes.
    """
    _require_write("add_negative_keywords")
    client = get_client()
    cid = _resolve_customer_id(customer_id)

    ag_ops, camp_ops = [], []
    for neg in negatives:
        match_type = neg.get("match_type", "EXACT").upper()
        if neg.get("ad_group_id"):
            op = client.get_type("AdGroupCriterionOperation")
            criterion = op.create
            criterion.ad_group = client.get_service("AdGroupService").ad_group_path(
                cid, neg["ad_group_id"]
            )
            criterion.negative = True
            criterion.keyword.text = neg["text"]
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum[match_type]
            ag_ops.append(op)
        elif neg.get("campaign_id"):
            op = client.get_type("CampaignCriterionOperation")
            criterion = op.create
            criterion.campaign = client.get_service("CampaignService").campaign_path(
                cid, neg["campaign_id"]
            )
            criterion.negative = True
            criterion.keyword.text = neg["text"]
            criterion.keyword.match_type = client.enums.KeywordMatchTypeEnum[match_type]
            camp_ops.append(op)
        else:
            raise ValueError(
                f"Negativo sem ad_group_id nem campaign_id: {neg.get('text')}"
            )

    results = {"aplicados": 0, "dry_run": dry_run, "detalhes": []}

    if ag_ops:
        resp = client.get_service("AdGroupCriterionService").mutate_ad_group_criteria(
            customer_id=cid, operations=ag_ops, validate_only=dry_run
        )
        results["aplicados"] += len(resp.results)
        results["detalhes"].append(f"ad_group: {len(resp.results)} negativos")
    if camp_ops:
        resp = client.get_service("CampaignCriterionService").mutate_campaign_criteria(
            customer_id=cid, operations=camp_ops, validate_only=dry_run
        )
        results["aplicados"] += len(resp.results)
        results["detalhes"].append(f"campanha: {len(resp.results)} negativos")

    if dry_run:
        results["aviso"] = "DRY RUN — nada foi gravado. Rode com dry_run=False para aplicar."
    return results


@mcp.tool()
def update_campaign_budget(
    campaign_id: str,
    new_daily_budget: float,
    customer_id: str | None = None,
    dry_run: bool = True,
) -> dict:
    """Altera o orcamento diario de uma campanha. Recusa variacao acima de 30%,
    que jogaria a campanha em reaprendizado."""
    _require_write("update_campaign_budget")
    client = get_client()
    cid = _resolve_customer_id(customer_id)

    current = _run_query(
        cid,
        f"""
        SELECT campaign.name, campaign_budget.id, campaign_budget.amount_micros,
               campaign_budget.explicitly_shared
        FROM campaign WHERE campaign.id = {campaign_id}
        """,
        limit=1,
    )
    if not current:
        raise ValueError(f"Campanha {campaign_id} nao encontrada.")

    row = current[0]
    old_value = row["campaign_budget.amount_micros"] / MICROS
    change_pct = ((new_daily_budget - old_value) / old_value) * 100 if old_value else 0

    if abs(change_pct) > 30:
        raise ValueError(
            f"Variacao de {change_pct:.1f}% excede o limite de 30%. "
            f"Atual R$ {old_value:.2f} -> proposto R$ {new_daily_budget:.2f}. "
            "Faca em etapas menores para nao reiniciar o aprendizado."
        )
    if row.get("campaign_budget.explicitly_shared"):
        raise ValueError(
            "Este orcamento e compartilhado: alterar afeta outras campanhas. "
            "Confirme com o usuario e ajuste pelo servico de orcamento diretamente."
        )

    op = client.get_type("CampaignBudgetOperation")
    budget = op.update
    budget.resource_name = client.get_service("CampaignBudgetService").campaign_budget_path(
        cid, row["campaign_budget.id"]
    )
    budget.amount_micros = int(new_daily_budget * MICROS)
    client.copy_from(op.update_mask, client.get_type("FieldMask")(paths=["amount_micros"]))

    resp = client.get_service("CampaignBudgetService").mutate_campaign_budgets(
        customer_id=cid, operations=[op], validate_only=dry_run
    )

    return {
        "campanha": row.get("campaign.name"),
        "de": round(old_value, 2),
        "para": new_daily_budget,
        "variacao_pct": round(change_pct, 1),
        "dry_run": dry_run,
        "aplicado": len(resp.results) > 0,
        "aviso": "DRY RUN — nada foi gravado." if dry_run else None,
    }


@mcp.tool()
def set_status(
    entity_type: str,
    entity_id: str,
    status: str,
    customer_id: str | None = None,
    ad_group_id: str | None = None,
    dry_run: bool = True,
) -> dict:
    """Pausa ou reativa uma entidade. entity_type: campaign, ad_group, keyword, ad.
    status: ENABLED ou PAUSED. Remocao nao e suportada de proposito — pausa e reversivel."""
    _require_write("set_status")
    if status.upper() not in ("ENABLED", "PAUSED"):
        raise ValueError("status deve ser ENABLED ou PAUSED. Remocao nao e suportada.")

    client = get_client()
    cid = _resolve_customer_id(customer_id)
    status_enum = status.upper()

    if entity_type == "campaign":
        op = client.get_type("CampaignOperation")
        entity = op.update
        entity.resource_name = client.get_service("CampaignService").campaign_path(cid, entity_id)
        entity.status = client.enums.CampaignStatusEnum[status_enum]
        service, method = client.get_service("CampaignService"), "mutate_campaigns"
    elif entity_type == "ad_group":
        op = client.get_type("AdGroupOperation")
        entity = op.update
        entity.resource_name = client.get_service("AdGroupService").ad_group_path(cid, entity_id)
        entity.status = client.enums.AdGroupStatusEnum[status_enum]
        service, method = client.get_service("AdGroupService"), "mutate_ad_groups"
    elif entity_type == "keyword":
        if not ad_group_id:
            raise ValueError("keyword exige ad_group_id.")
        op = client.get_type("AdGroupCriterionOperation")
        entity = op.update
        entity.resource_name = client.get_service(
            "AdGroupCriterionService"
        ).ad_group_criterion_path(cid, ad_group_id, entity_id)
        entity.status = client.enums.AdGroupCriterionStatusEnum[status_enum]
        service, method = client.get_service("AdGroupCriterionService"), "mutate_ad_group_criteria"
    elif entity_type == "ad":
        if not ad_group_id:
            raise ValueError("ad exige ad_group_id.")
        op = client.get_type("AdGroupAdOperation")
        entity = op.update
        entity.resource_name = client.get_service("AdGroupAdService").ad_group_ad_path(
            cid, ad_group_id, entity_id
        )
        entity.status = client.enums.AdGroupAdStatusEnum[status_enum]
        service, method = client.get_service("AdGroupAdService"), "mutate_ad_group_ads"
    else:
        raise ValueError("entity_type deve ser campaign, ad_group, keyword ou ad.")

    client.copy_from(op.update_mask, client.get_type("FieldMask")(paths=["status"]))
    resp = getattr(service, method)(customer_id=cid, operations=[op], validate_only=dry_run)

    return {
        "entidade": f"{entity_type}:{entity_id}",
        "novo_status": status_enum,
        "dry_run": dry_run,
        "aplicado": len(resp.results) > 0,
        "aviso": "DRY RUN — nada foi gravado." if dry_run else None,
    }


@mcp.tool()
def write_status() -> dict:
    """Informa se a escrita esta habilitada e qual conta esta configurada por padrao."""
    return {
        "escrita_habilitada": ALLOW_WRITE,
        "customer_id_padrao": DEFAULT_CUSTOMER_ID or "nao configurado",
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID", "nao configurado"),
        "observacao": (
            "Escrita desativada: apenas leitura disponivel."
            if not ALLOW_WRITE
            else "Escrita ativa. Toda mutacao ainda exige aprovacao explicita do usuario."
        ),
    }


if __name__ == "__main__":
    mcp.run()
