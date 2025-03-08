import os
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

# Fetch environment variables
twilio_sid = os.getenv("TWILIO_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")
recipient_phone_number = os.getenv("RECIPIENT_PHONE_NUMBER")

# URL to check for apartments
url = "https://bostad.stockholm.se/bostad?s=59.28272&n=59.42622&w=17.88025&e=18.22151&sort=annonserad-fran-desc&maxHyra=8000&kanAnmalaIntresse=1"

def get_apartments():
    """Scrapes the website for new apartments."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Assuming listings are contained in specific tags (you may need to inspect the page and modify this)
    apartments = soup.find_all("div", class_="listing-card")

    return apartments

def send_sms(message):
    """Sends an SMS using Twilio."""
    client = Client(twilio_sid, twilio_auth_token)

    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )

    print(f"Message sent! ID: {message.sid}")

def main():
    apartments = get_apartments()

    if apartments:
        # If new apartments are found, send an SMS alert
        send_sms(f"Found {len(apartments)} new apartments under 8000 SEK!")
    else:
        print("No new apartments found.")

if __name__ == "__main__":
    main()
