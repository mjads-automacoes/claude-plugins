"""
Gera o refresh token do Google Ads uma unica vez.

Uso:
    1. Preencha GOOGLE_ADS_CLIENT_ID e GOOGLE_ADS_CLIENT_SECRET no .env
    2. python gerar_refresh_token.py
    3. Autorize no navegador com a conta Google que tem acesso ao MCC
    4. Copie o token exibido para GOOGLE_ADS_REFRESH_TOKEN no .env

O token nao expira enquanto o acesso nao for revogado. Guarde-o como senha:
nunca cole em conversa, issue, print ou repositorio.
"""

import os

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/adwords"]

load_dotenv()

client_id = os.getenv("GOOGLE_ADS_CLIENT_ID")
client_secret = os.getenv("GOOGLE_ADS_CLIENT_SECRET")

if not client_id or not client_secret:
    raise SystemExit(
        "Preencha GOOGLE_ADS_CLIENT_ID e GOOGLE_ADS_CLIENT_SECRET no .env primeiro."
    )

flow = InstalledAppFlow.from_client_config(
    {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    },
    scopes=SCOPES,
)

credentials = flow.run_local_server(port=0, prompt="consent")

print("\n" + "=" * 60)
print("Refresh token gerado. Copie a linha abaixo para o seu .env:\n")
print(f"GOOGLE_ADS_REFRESH_TOKEN={credentials.refresh_token}")
print("=" * 60)
print("\nNao compartilhe este valor com ninguem, nem cole em conversa.")
