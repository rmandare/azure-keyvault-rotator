"""Rotate Azure Key Vault secrets older than a threshold."""

import os
import sys
import secrets
import string
import argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient

load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument("--vault", required=True, help="Key Vault name")
parser.add_argument("--age-days", type=int, default=90, help="Rotate secrets older than this")
parser.add_argument("--dry-run", action="store_true", help="Preview without changes")
args = parser.parse_args()

credential = ClientSecretCredential(
    tenant_id=os.getenv("AZURE_TENANT_ID"),
    client_id=os.getenv("AZURE_CLIENT_ID"),
    client_secret=os.getenv("AZURE_CLIENT_SECRET"),
)

vault_url = f"https://{args.vault}.vault.azure.net"
client = SecretClient(vault_url=vault_url, credential=credential)


def generate_secret(length=32):
    """Generate a cryptographically secure random secret."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def main():
    cutoff = datetime.now(timezone.utc) - timedelta(days=args.age_days)
    rotated = 0

    for secret_props in client.list_properties_of_secrets():
        if secret_props.created_on and secret_props.created_on < cutoff:
            age = (datetime.now(timezone.utc) - secret_props.created_on).days
            print(f"[{age}d old] {secret_props.name}")

            if not args.dry_run:
                new_value = generate_secret()
                client.set_secret(secret_props.name, new_value)
                rotated += 1

    action = "Would rotate" if args.dry_run else "Rotated"
    print(f"\n{action} {rotated} secrets.")


if __name__ == "__main__":
    main()
