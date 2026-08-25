# Azure Key Vault Secret Rotator

Rotates secrets in Azure Key Vault based on age. Runs weekly as a cron job.

Automatically expires secrets older than 90 days and creates new versions.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # fill in credentials
python rotate.py --vault my-keyvault --dry-run
python rotate.py --vault my-keyvault
```

## How it works

- Lists all secrets in the target Key Vault
- Identifies secrets older than the threshold (default 90 days)
- Generates a new version with a fresh random value
- Logs rotation events to stdout

## TODO

- [ ] Move service principal creds to managed identity
- [ ] Add Slack notification on rotation
- [ ] Support certificate rotation too
- [ ] Exclude secrets tagged `no-auto-rotate`
