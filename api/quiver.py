import os
from dotenv import load_dotenv
import requests
import pandas as pd

# Load .env variables
load_dotenv()

class quiver:
    def __init__(self):
        self.token = os.getenv("QUIVER_API_TOKEN")  # Load API token from environment variables
        self.headers = {
            'accept': 'application/json',
            'Authorization': "Token " + self.token
        }
    
    def congress_trading(self, ticker="", politician=False, recent=True):
        url_start = 'https://api.quiverquant.com/beta/live/congresstrading' if recent else 'https://api.quiverquant.com/beta/bulk/congresstrading'
        if politician:
            ticker = ticker.replace(" ", "%20")
            url = f"{url_start}?representative={ticker}"
        elif ticker:
            url = f"{url_start}/{ticker}"
        else:
            url = url_start

        print(f"Fetching data from: {url}")
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        df["ReportDate"] = pd.to_datetime(df["ReportDate"])
        df["TransactionDate"] = pd.to_datetime(df["TransactionDate"])
        return df
    
    # Add other methods as needed, e.g., senate_trading, lobbying, etc.
