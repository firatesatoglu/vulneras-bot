# VulneraS BOT
A Telegram BOT for automated start Acunetix, Nessus scanner. VulneraS is a Telegram bot designed to automate the startup of Acunetix and Nessus scanners. This bot provides users with direct access to initiate and manage security scanning tasks from their Telegram accounts, aiming to streamline the process of security assessment.

### Telegram Bot Token

To set the Telegram bot token, create an environment variable named `TELEGRAM_BOT_TOKEN` and assign your bot token as its value.

### Token For Subdomain Scanner 

For the subdomain scanner, you no need to get API key for all of them, but some of them need API key. You can get API keys from their websites and set them in the .env file. Need to API keys for the following services: shodan, whoxml, sslmate, binaryedge, hunterhow, securitytrails, bevigil

# Usage - ETU

    /help - This help message
    /target - Add target domain
    /createreport - Create report
    /downloadreport - Download report
    /listtargets - List all targets
    /listreports - List all reports

  ![image](https://github.com/firatesatoglu/vulneras-bot/assets/60032785/1d72aa68-6d18-4eac-aaf7-eec445b35ab0)
