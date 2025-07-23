import requests

url = "https://pubs.acs.org/doi/10.1021/acscatal.0c04525"

# Add headers to simulate a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Page accessed successfully!")
        print(response.text[:500])  # Print first 500 characters of the HTML
    elif response.status_code == 403:
        print("Access forbidden (403). The server refused the request.")
    else:
        print(f"Request returned status code: {response.status_code}")
except requests.RequestException as e:
    print(f"Request failed: {e}")
