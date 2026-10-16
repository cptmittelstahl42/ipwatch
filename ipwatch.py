#!/usr/bin/env python3

"""
IPWatch - Überwachung der oeffentlichen IPv4-Adresse.
Versendet bei einer Aenderung eine E-Mail.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import requests
import smtplib
from email.message import EmailMessage

# Konfiguration

SMTP_SERVER = "smtp.smarthost.com"
SMTP_PORT = 587
SMTP_USER = "irgendwas@domain.tld"
SMTP_PASSWORD = "Passwort"

SMTP_USE_TLS = True
SMTP_USE_SSL = False

MAIL_FROM = "from@mail.com"
MAIL_TO = "to@mail.com"

IP_API_URL = "https://api.ipify.org"

DATA_FILE = Path("./data/last_ip.txt")
LOG_FILE = Path("./logs/ipwatch.log")

# Logging

LOG_FILE.parent.mkdir(exist_ok=True)
DATA_FILE.parent.mkdir(exist_ok=True)

logger = logging.getLogger("ipwatch")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=1024 * 1024,
    backupCount=5
)

handler.setFormatter(
    logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )
)

logger.addHandler(handler)

# Funktionen

def get_public_ip():
    """Ermittelt die oeffentliche IPv4-Adresse."""

    response = requests.get(IP_API_URL, timeout=10)
    response.raise_for_status()
    return response.text.strip()

def get_stored_ip():
    """Liest die gespeicherte IP-Adresse."""

    if not DATA_FILE.exists():
        logger.info("Keine gespeicherte IP gefunden.")
        return ""

    return DATA_FILE.read_text().strip()

def save_ip(ip):
    """Speichert die aktuelle IP-Adresse."""

    DATA_FILE.write_text(ip)
    logger.info(f"IP gespeichert: {ip}")

def send_mail(old_ip, new_ip):
    """Versendet die Benachrichtigung."""

    msg = EmailMessage()

    msg["From"] = MAIL_FROM
    msg["To"] = MAIL_TO
    msg["Subject"] = f"IP-Adresse geaendert ({new_ip})"

    msg.set_content(
        f"""Die oeffentliche IP-Adresse hat sich geaendert.

Alt: {old_ip}
Neu: {new_ip}
"""
    )

    if SMTP_USE_SSL:

        with smtplib.SMTP_SSL(
            SMTP_SERVER,
            SMTP_PORT
        ) as smtp:

            smtp.login(
                SMTP_USER,
                SMTP_PASSWORD
            )

            smtp.send_message(msg)

    else:

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        ) as smtp:

            if SMTP_USE_TLS:
                smtp.starttls()

            smtp.login(
                SMTP_USER,
                SMTP_PASSWORD
            )

            smtp.send_message(msg)

def main():
    """Haupteinstiegspunkt."""

    logger.info("Skript gestartet")

    try:

        current_ip = get_public_ip()
        old_ip = get_stored_ip()

        logger.info(f"Aktuelle IP: {current_ip}")
        logger.info(f"Letzte IP: {old_ip}")

        if not old_ip:
            save_ip(current_ip)
            logger.info("Erstinitialisierung abgeschlossen.")
            return

        if current_ip == old_ip:
            logger.info("Keine Aenderung festgestellt.")
            return

        logger.warning(
            f"IP-Wechsel erkannt: {old_ip} -> {current_ip}"
        )

        send_mail(old_ip, current_ip)

        logger.info(
            "Benachrichtigungsmail erfolgreich versendet."
        )

        save_ip(current_ip)

    except Exception as ex:

        logger.exception(
            f"Fehler waehrend der Verarbeitung: {ex}"
        )

if __name__ == "__main__":
    main()
