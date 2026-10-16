### IPWatch

Motivation
Viele Internetanschlüsse nutzen dynamische öffentliche IPv4-Adressen. Bei meinem Telekom-Glasfaseranschluss kann die Adresse monatelang unverändert bleiben und dann ohne Vorwarnung wechseln.

Für Dienste wie VPN-Zugänge, DNS-Einträge und Portweiterleitungen ist ein solcher Wechsel relevant. Oft bemerke ich die Änderung erst dann, wenn eine Verbindung nicht mehr funktioniert.

Lösung
IPWatch überprüft in regelmäßigen Abständen die öffentliche IPv4-Adresse und vergleicht sie mit der zuletzt bekannten Adresse.

Wird eine Änderung erkannt:

die neue Adresse wird gespeichert
eine Benachrichtigungs-E-Mail wird versendet
das Ereignis wird protokolliert
Alle Aktionen werden in einer Logdatei festgehalten. Dadurch lässt sich auch nachträglich nachvollziehen, wann eine Adressänderung stattgefunden hat oder warum ein Versand fehlgeschlagen ist.

Funktionen
Ermittlung der öffentlichen IPv4-Adresse über eine öffentliche API
Vergleich mit der zuletzt bekannten Adresse
Benachrichtigung per SMTP
Unterstützung für TLS und SSL
ausführliche Protokollierung
automatische Logrotation
geeignet für die Ausführung per Cron
Verzeichnisstruktur
ipwatch/
    ipwatch.py
        data/
            last_ip.txt
        logs/
            ipwatch.log

    
Konfiguration
Die Konfiguration erfolgt direkt im Kopf der Datei ipwatch.py.

Beispiel:

SMTP_SERVER = "smtp.strato.de"
SMTP_PORT = 587

SMTP_USER = "monitor@example.de"
SMTP_PASSWORD = "password"

SMTP_USE_TLS = True
SMTP_USE_SSL = False

MAIL_FROM = "monitor@example.de"
MAIL_TO = "admin@example.de"
Installation
Debian:

apt update
apt install python3 python3-requests
Alternativ:

pip install requests
Ausführung
Manueller Testlauf:

python3 ipwatch.py
Automatische Ausführung
Beispiel: stündliche Prüfung per Cron.

0 * * * * /usr/bin/python3 /opt/ipwatch/ipwatch.py
Logging
Das Skript schreibt alle Ereignisse in:

logs/ipwatch.log
Protokolliert werden unter anderem:

Start und Ende eines Laufs
ermittelte öffentliche IP-Adresse
letzte bekannte IP-Adresse
erkannte Änderungen
erfolgreicher Mailversand
Fehler bei API-Aufrufen oder SMTP-Verbindungen
Beispiel:

2026-10-16 15:41:52 [INFO] Aktuelle IP: 217.231.80.252
2026-10-16 15:41:52 [INFO] Letzte IP: 1.1.1.1
2026-10-16 15:41:52 [WARNING] IP-Wechsel erkannt: 1.1.1.1 -> 217.231.80.252
2026-10-16 15:41:52 [INFO] Benachrichtigungsmail erfolgreich versendet.
Test einer Adressänderung
Zum Test kann die gespeicherte IP-Adresse manuell verändert werden:

echo "1.1.1.1" > data/last_ip.txt
Anschließend:

python3 ipwatch.py
Das Skript erkennt die Abweichung und löst die Benachrichtigung aus.
