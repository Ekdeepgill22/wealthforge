from crewai.tools import BaseTool
import requests
import os

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

class MyCustomTool(BaseTool):
    name: str = "Alpha Vantage Stock Tool"
    description: str = (
        "Fetches stock market data"
    )

    def _run(self, symbol: str, function:str = "TIME_SERIES_INTRADAY", interval: str="5min") -> dict:
        # Implementation goes here
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        url = f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&apikey={api_key}" 

        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return{"error": "failed to fetch the response {response.status.code}"}      
    
