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


# Database Choice (MongoDB Atlas)(**TOOK HELP FROM GEMINI TO CONNECT MONGODB ATLAS AND SOLVE EROORS **)

# https://gemini.google.com/share/ef4d1e80ae11

# used gemini to solve error in code # https://gemini.google.com/share/3e62c3391fce

# The system uses MongoDB Atlas, a cloud-based NoSQL database, to store and manage job listings efficiently.

# Loading Process The pipeline converts the scraped data into a dictionary format and performs a full refresh of the collection to ensure data accuracy.

import pymongo
import pandas as pd

DB_USER = "dbUSER"
DB_PASSWORD = "TEs96WeyXwsYlzoW"

CONNECTION_STRING = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.1oirk6b.mongodb.net/?retryWrites=true&w=majority"

try:
    client = pymongo.MongoClient(CONNECTION_STRING)
    db = client['GovHireDB']
    collection = db['JobsCollection']

    if 'df' in locals() or 'df' in globals():
        job_data = df.to_dict('records')
        collection.delete_many({})
        collection.insert_many(job_data)
        print(f"Successfully loaded {len(job_data)} jobs to MongoDB Atlas.")
    else:
        print("Error: DataFrame 'df' is not defined.")

except Exception as e:
    
    print(f"An error occurred while connecting to MongoDB: {e}")

finally:
  
    client.close()
    
    
    #"Imported libraries including pandas, sklearn, seaborn, matplotlib, and gradio for ML model development and analysis"
    
import pandas as pd
import re
import gradio as gr
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.multioutput import MultiOutputClassifier