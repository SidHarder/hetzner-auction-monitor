import os
import requests

from twilio.rest import Client

URL = "https://www.hetzner.com/_resources/app/data/app/live_data_sb.json"

response = requests.get(URL, timeout=30)
response.raise_for_status()

data = response.json()

matches = []

for server in data.get("server", []):

    price = float(server.get("price", 9999))

    # Example criteria
    if price <= 70:
        matches.append(server)

if not matches:
    print("No matches found")
    exit(0)

message_lines = []

for server in matches[:10]:

    message_lines.append(
        f"€{server.get('price')} | "
        f"{server.get('cpu')} | "
        f"{server.get('ram')}"
    )

message = "\n".join(message_lines)

client = Client(
    os.environ["TWILIO_ACCOUNT_SID"],
    os.environ["TWILIO_AUTH_TOKEN"]
)

client.messages.create(
    body=message,
    from_=os.environ["TWILIO_PHONE_NUMBER"],
    to=os.environ["YOUR_PHONE_NUMBER"]
)

print("SMS sent")
