# Energetický mix

Twitter bot [@energymixcz](https://twitter.com/energymixcz) tvítující energetický mix elektřiny vyrobené v Česku za předešlou hodinu z dat [Entsoe](https://transparency.entsoe.eu/).

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

Překvapivě neexistuje emoji pro uhlí...

## Použití

Předpokladem jsou údaje potřebné pro dotazy na Entsoe a Twitter API uložené v souboru `.env` v kořenovém adresáři.

Pomocí `pip` instalovat z místního adresáře `energy-mix` v rámci virtuálního prostředí (zdá se, že cronjob nepodporuje spouštění s možností `-m`, e.g. `python -m bot.main`).

```
python -m venv venv
source venv/bin/activate
pip install --use-feature=in-tree-build .
crontab -e
```

Insert cronjob: `07 6-18 * * * /path/to/installed/endpoint/energy-mix/`

TODO: Ověřit, zda ostatní OZE je výhradně bioplyn a nejspíš změnit emoji a zpřehlednit konfiguraci.
