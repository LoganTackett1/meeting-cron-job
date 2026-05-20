import requests
from datetime import datetime
import os


def send_discord_message(message, discord_webhook_url):
    payload = {
        "content": message
    }

    response = requests.post(
        discord_webhook_url,
        json=payload,
        timeout=30
    )

    if response.status_code not in (200, 204):
        print(f"Discord message failed: {response.status_code}")
        print(response.text)


def main():
    url = os.environ.get("URL")
    discord_webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")

    if not url:
        print("Missing URL environment variable")
        return

    if not discord_webhook_url:
        print("Missing DISCORD_WEBHOOK_URL environment variable")
        return

    try:
        response = requests.get(url, timeout=30)

        print("=" * 80)
        print(f"Timestamp: {datetime.utcnow().isoformat()}Z")
        print(f"Status Code: {response.status_code}")

        try:
            data = response.json()

            for day in data.get("days", []):
                date = day.get("date")
                available_times = day.get("spots", [])

                if len(available_times) > 0:
                    message = (
                        f"Available times found!\n"
                        f"Date: {date}\n"
                        f"Times: {', '.join(available_times)}"
                    )

                    print(message)

                    send_discord_message(
                        message,
                        discord_webhook_url
                    )

        except Exception:
            print(response.text)

    except Exception as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    main()