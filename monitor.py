import os
import requests
import smtplib

from email.message import EmailMessage

URL = "https://www.hetzner.com/_resources/app/data/app/live_data_sb.json"

# Example criteria
MAX_PRICE = 100.00

response = requests.get(URL, timeout=30)
response.raise_for_status()

data = response.json()

print("******************* running alert check ******************* ")

matches = []

for server in data.get("server", []):
    try:        
        for server in data:
            print(server)
            
            storage = (
                server
                .get("Hardware", {})
                .get("Storage", {})
                .get("Details", {})
            )

            nvme_total = sum(storage.get("nvme", []))            
            print('The NVME Total is: ' + str(nvme_total))                        

            if nvme_total >= 1000:
                matches.append(server)

    except Exception:
        continue

if not matches:
    print("No matches found")
    raise SystemExit(0)

message_body = "Hetzner Server Found"

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