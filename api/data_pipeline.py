import pandas as pd
import logging
from quiver import quiver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("data_pipeline")

def fetch_data():
    client = quiver()
    
    # Fetch Tier 1 Trading Data
    logger.info("Fetching Congress Trading Data...")
    congress_data = client.congress_trading(recent=True)
    logger.info("Fetching Senate Trading Data...")
    senate_data = client.senate_trading()
    logger.info("Fetching House Trading Data...")
    house_data = client.house_trading()
    
    # Fetch Tier 1 Additional Data
    logger.info("Fetching Lobbying Data...")
    lobbying_data = client.lobbying()
    logger.info("Fetching Off-Exchange Data...")
    off_exchange_data = client.offexchange()
    logger.info("Fetching Government Contracts Data...")
    gov_contracts_data = client.gov_contracts()
    
    # Ensure all datasets have consistent datetime columns
    datasets = {
        "Congress Trading": congress_data.rename(columns={"ReportDate": "Date"}),
        "Senate Trading": senate_data.rename(columns={"Date": "Date"}),
        "House Trading": house_data.rename(columns={"Date": "Date"}),
        "Lobbying": lobbying_data.rename(columns={"Date": "Date"}),
        "Off-Exchange": off_exchange_data.rename(columns={"Date": "Date"}),
        "Government Contracts": gov_contracts_data.rename(columns={"Date": "Date"}),
    }
    
    # Convert all Date columns to datetime
    for name, data in datasets.items():
        datasets[name]['Date'] = pd.to_datetime(data['Date'])
        
    # Validate and merge datasets
    logger.info("Merging datasets...")
    combined_data = pd.DataFrame()
    for name, data in datasets.items():
        if data.empty:
            logger.warning(f"{name} dataset is empty.")
        else:
            if not combined_data.empty:
                combined_data = combined_data.merge(
                    data, 
                    on=["Ticker", "Date"], 
                    how="outer", 
                    suffixes=(None, f"_{name.replace(' ', '_')}")
                )
            else:
                combined_data = data
            logger.info(f"{name} data merged successfully.")
    
    # Sorting and handling missing data
    combined_data = combined_data.sort_values(by="Date").fillna(0)
    
    logger.info("Data fetch and merge complete.")
    return combined_data
