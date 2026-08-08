import os
import requests
import smtplib

from email.message import EmailMessage

URL = "https://www.hetzner.com/_resources/app/data/app/live_data_sb.json"

# Example criteria
MAX_PRICE = 90.00

response = requests.get(URL, timeout=30)
response.raise_for_status()

data = response.json()

matches = []

for server in data.get("server", []):
    try:
        price = float(server.get("price", 9999))

        if price <= MAX_PRICE:
            matches.append(server)

    except Exception:
        continue

if not matches:
    print("No matches found")
    raise SystemExit(0)

message_lines = []

for server in matches[:10]:
    message_lines.append(
        f"Price: €{server.get('price')} | "
        f"CPU: {server.get('cpu')} | "
        f"RAM: {server.get('ram')}"
    )

message_body = "\n".join(message_lines)

msg = EmailMessage()
msg["Subject"] = "Hetzner Auction Match"
msg["From"] = os.environ["SMTP_USERNAME"]
msg["To"] = os.environ["ALERT_EMAIL"]
msg.set_content(message_body)

with smtplib.SMTP(
    os.environ["SMTP_SERVER"],
    int(os.environ["SMTP_PORT"])
) as smtp:
    smtp.starttls()
    smtp.login(
        os.environ["SMTP_USERNAME"],
        os.environ["SMTP_PASSWORD"]
    )
    smtp.send_message(msg)

print("Alert sent.")