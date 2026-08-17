import requests
from bs4 import BeautifulSoup
import os
import time
import re

# GitHub will inject your secret webhook URL here
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

# The page we are scraping
COURSE_URL = "https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&catalogNbr=471&honors=F&promod=F&searchType=all&subject=CSE&term=2267#detailsOpen=85434-104223"

def check_seat():
    # Fetch the webpage with a user-agent so ASU doesn't block it
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(COURSE_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Strip away HTML to search the visible text
    page_text = soup.get_text(separator=" ", strip=True)
    
    # Search for the exact phrase and capture the number
    match = re.search(r'Non Reserved Available Seats:\s*(\d+)', page_text)
    
    if match:
        seats = int(match.group(1))
        return seats
    
    # Return 0 if the text isn't found
    return 0

if __name__ == "__main__":
    seats_open = check_seat()

    if seats_open > 0:
        # THE SPAM LOOP - sends 5 messages every time the script runs
        for i in range(5):
            data = {
                "content": f"@everyone 🚨 SEAT OPEN! There are **{seats_open}** seats available! Go register NOW! 🚨\n{COURSE_URL}"
            }
            requests.post(WEBHOOK_URL, json=data)
            time.sleep(2) # Wait 2 seconds between messages to avoid Discord rate limits
        print(f"Seat found! {seats_open} open. Spam sent.")
    else:
        print("No seats open yet.")
