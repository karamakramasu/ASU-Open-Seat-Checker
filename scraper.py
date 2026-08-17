import requests
from bs4 import BeautifulSoup
import os
import time

# GitHub will inject your secret webhook URL here
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK")

# The page we are scraping
COURSE_URL = "https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&catalogNbr=471&honors=F&promod=F&searchType=all&subject=CSE&term=2267#detailsOpen=85434-104223"

def check_seat():
    # Fetch the webpage
    response = requests.get(COURSE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # NOTE: We need to inspect your specific university website 
    # to know exactly what text or HTML tag to look for here!
    # For example, if it says "Seats: 1":
    if "Seats: 0" not in response.text: 
        return True
    return False

if __name__ == "__main__":
    if check_seat():
        # THE SPAM LOOP - sends 5 messages every time the script runs
        for i in range(5):
            data = {
                "content": "@everyone 🚨 SEAT OPEN! Go register NOW! 🚨\n" + COURSE_URL
            }
            requests.post(WEBHOOK_URL, json=data)
            time.sleep(2) # Wait 2 seconds between messages to avoid Discord rate limits
        print("Seat found! Spam sent.")
    else:
        print("No seats open yet.")
