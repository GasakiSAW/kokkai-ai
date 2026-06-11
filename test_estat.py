import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

APP_ID = os.getenv("ESTAT_APP_ID")

url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList"

params = {
    "appId": APP_ID,
    "searchWord": "消費者物価指数",
    "limit": 5
}

response = requests.get(url, params=params)

print("status:", response.status_code)
print(response.text[:1000])
