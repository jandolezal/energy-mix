# Energetický mix

Twitter bot [@energetickymix](https://twitter.com/energetickymix) tvítující energetický mix elektřiny vyrobené v Česku za předešlou hodinu z dat [Entsoe](https://transparency.entsoe.eu/).

![Screenshot of the bot status](images/status.png)

Za každé procento podílu na výrobě jeden emoji. 

🏭 uhlí

🔥 zemní plyn

🛢️ ropa

☢️ jádro

☀️ slunce

💨 vítr

💧 voda

🌿 biomasa

🗑️ odpad

♻️ ostatní OZE

Status ve 14:?? pokrývá elektřinu vyrobenou v čase 13:00-14:00. Případný výpadek je způsobený identickou výrobou (z hlediska zaokrouhleného podílu). Twitter API nedovolí duplicitní tweet v řadě.

## Použití

### GitHub Action

[![energy-mix](https://github.com/jandolezal/energy-mix/actions/workflows/energy-mix.yml/badge.svg?branch=main)](https://github.com/jandolezal/energy-mix/actions/workflows/energy-mix.yml)

Běží jako [GitHub Action](https://docs.github.com/en/actions/guides/building-and-testing-python) dle nastavení v `.github/workflows`. Je třeba pro repozitář [nastavit](https://docs.github.com/en/actions/reference/encrypted-secrets#creating-encrypted-secrets-for-a-repository) tokeny pro komunikaci s Entsoe a Twitter API.

### Lokálně

Předpokladem jsou údaje potřebné pro dotazy na Entsoe a Twitter API uložené v souboru `.env` v kořenovém adresáři.

Pomocí `pip` instalovat z místního adresáře `energy-mix` v rámci virtuálního prostředí.

```
python3 -m venv venv
source venv/bin/activate
pip install .
crontab -e
```

Nastavit cronjob `07 6-18 * * * /path/to/energy-mix`
