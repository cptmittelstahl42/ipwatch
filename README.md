# IPWatch

## Motivation
Viele Internetanschlüsse nutzen dynamische öffentliche IPv4-Adressen. Bei meinem Telekom-Glasfaseranschluss kann die Adresse monatelang unverändert bleiben und dann ohne Vorwarnung wechseln.

Für Dienste wie VPN-Zugänge, DNS-Einträge und Portweiterleitungen ist ein solcher Wechsel relevant. Oft bemerke ich die Änderung erst dann, wenn eine Verbindung nicht mehr funktioniert.

## Lösung
IPWatch überprüft in regelmäßigen Abständen die öffentliche IPv4-Adresse und vergleicht sie mit der zuletzt bekannten Adresse.

## Funktionen

- Ermittlung der öffentlichen IPv4-Adresse
- Vergleich mit der zuletzt bekannten Adresse
- E-Mail-Benachrichtigung bei Änderungen
- Ausführliches Logging
- Logrotation
- Ausführung per Cron

## Verzeichnisstruktur

```text
ipwatch/
├── ipwatch.py
├── data/
│   └── last_ip.txt
└── logs/
    └── ipwatch.log
```

## Konfiguration

Die Konfiguration erfolgt direkt im Python-Skript.

```python
SMTP_SERVER = "smtp.smarthost.de"
SMTP_PORT = 587

SMTP_USER = "monitor@example.de"
SMTP_PASSWORD = "password"

SMTP_USE_TLS = True
SMTP_USE_SSL = False

MAIL_FROM = "monitor@example.de"
MAIL_TO = "admin@example.de"
```

## Installation

Debian:

```bash
apt update
apt install python3 python3-requests
```

## Testlauf

```bash
python3 ipwatch.py
```

## Cronjob

Stündliche Ausführung:

```cron
0 * * * * /usr/bin/python3 /opt/ipwatch/ipwatch.py
```

## Logging

Alle Ereignisse werden in `logs/ipwatch.log` protokolliert.

Beispiel:

```text
2026-10-16 15:41:52 [INFO] Aktuelle IP: 8.8.8.8
2026-10-16 15:41:52 [INFO] Letzte IP: 1.1.1.1
2026-10-16 15:41:52 [WARNING] IP-Wechsel erkannt: 1.1.1.1 -> 8.8.8.8
2026-10-16 15:41:52 [INFO] Benachrichtigungsmail erfolgreich versendet.
```

## Test einer IP-Änderung

```bash
echo "1.1.1.1" > data/last_ip.txt
python3 ipwatch.py
```

Dadurch wird eine Änderung simuliert und der Mailversand ausgelöst.

## Lizenz
Dieses Projekt steht unter der GNU General Public License v3.0 (GPLv3).

Copyright (c) 2026 Tim Böttcher [cptmittelstahl42]

Details siehe Datei LICENSE.
