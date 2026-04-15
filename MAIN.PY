#Extraction Layer: Uses BeautifulSoup to parse paginated HTML data .
#Instructor guided me with the logic for web scraping from www.maharashtrasarkarinaukri.com

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    "User-Agent": "Mozilla/5.0"
}
all_jobs = []
for page in range(1,101):
  if page == 1:
    url = "https://www.maharashtrasarkarinaukri.com/"
  else:
    url = f"https://www.maharashtrasarkarinaukri.com/page/{page}/"
    print("Scraping page:", page)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
      print("Stopped at page:", page)
      break

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    for link in links:
      title = link.get_text(strip=True)
      href = link.get("href")
      if title and href:
        all_jobs.append({"title": title, "link": href})

    time.sleep(0.2)


# Created DataFrame from collected job data and removed duplicates

df = pd.DataFrame(all_jobs).drop_duplicates()
print("Total jobs collected:", len(df))











