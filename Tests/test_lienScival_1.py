import requests

API_KEY = "85c7f7feb66ebceade90364e20252d21"
AUTHOR_ID = "56216876600"
url = f"https://api.elsevier.com/analytics/scival/author/{AUTHOR_ID}"

headers = {
    "X-ELS-APIKey": API_KEY,
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)

print(f"Status Code: {response.status_code}")
print("Response:", response.text)
