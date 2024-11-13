import os
from dotenv import load_dotenv
import requests
import pandas as pd
import json

# Load environment variables
load_dotenv()

class quiver:
    def __init__(self):
        self.token = os.getenv("QUIVER_API_TOKEN")  # Load API token from .env
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

    def senate_trading(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/senatetrading" if not ticker else f"https://api.quiverquant.com/beta/historical/senatetrading/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        df["Date"] = pd.to_datetime(df["Date"])
        return df

    def house_trading(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/housetrading" if not ticker else f"https://api.quiverquant.com/beta/historical/housetrading/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        df["Date"] = pd.to_datetime(df["Date"])
        return df

    def offexchange(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/offexchange" if not ticker else f"https://api.quiverquant.com/beta/historical/offexchange/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        if not df.empty and "Date" in df:
            df["Date"] = pd.to_datetime(df["Date"])
        return df

    def gov_contracts(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/govcontractsall" if not ticker else f"https://api.quiverquant.com/beta/historical/govcontractsall/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        return df

    def lobbying(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/lobbying" if not ticker else f"https://api.quiverquant.com/beta/historical/lobbying/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        df["Date"] = pd.to_datetime(df["Date"])
        return df

    def insiders(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/insiders" if not ticker else f"https://api.quiverquant.com/beta/live/insiders?ticker={ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        return df

    def wikipedia(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/wikipedia" if not ticker else f"https://api.quiverquant.com/beta/historical/wikipedia/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        return df

    def wallstreetbets(self, ticker=""):
        """Fetch WallStreetBets data."""
        url = f"https://api.quiverquant.com/beta/live/wallstreetbets" if not ticker else f"https://api.quiverquant.com/beta/historical/wallstreetbets/{ticker}"
        print(f"Fetching data from: {url}")
        
        r = requests.get(url, headers=self.headers)
        try:
            data = r.json()
        except json.JSONDecodeError:
            raise ValueError("Failed to decode JSON from the API response.")
        
        # Check if the response is a valid list of records
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data)
        else:
            # Return an empty DataFrame with appropriate columns if no data
            df = pd.DataFrame([], columns=["Date", "Ticker", "Mentions"])  # Adjust columns as needed
        
        return df


    def twitter(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/twitter" if not ticker else f"https://api.quiverquant.com/beta/historical/twitter/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        return df

    def spacs(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/spacs" if not ticker else f"https://api.quiverquant.com/beta/historical/spacs/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        return df

    def flights(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/flights" if not ticker else f"https://api.quiverquant.com/beta/historical/flights/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        return df

    def political_beta(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/politicalbeta" if not ticker else f"https://api.quiverquant.com/beta/historical/politicalbeta/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        return df

    def patents(self, ticker=""):
        url = f"https://api.quiverquant.com/beta/live/allpatents" if not ticker else f"https://api.quiverquant.com/beta/historical/allpatents/{ticker}"
        r = requests.get(url, headers=self.headers)
        df = pd.DataFrame(r.json())
        df["Date"] = pd.to_datetime(df["Date"])
        return df

    def sec13F(self, ticker="", date="", owner="", period=""):
        url = "https://api.quiverquant.com/beta/live/sec13f"
        params = {}
        if ticker: params["ticker"] = ticker
        if date: params["date"] = date
        if owner: params["owner"] = owner
        if period: params["period"] = period
        r = requests.get(url, headers=self.headers, params=params)
        df = pd.DataFrame(r.json())
        df["Date"] = pd.to_datetime(df["Date"], unit="ms")
        return df
