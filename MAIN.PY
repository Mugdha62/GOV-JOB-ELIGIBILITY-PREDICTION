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

#Data Transformations and Feature Engineering.(took help from gemini to create functions and logic to translate and solve errors marathi to english AND PASTED marathi words which i could not type)

# https://gemini.google.com/share/ef4d1e80ae11

#The Transformation PipelineThe raw scraped data requires extensive cleaning to be useful for machine learning:

#Multilingual Standardisation: Marathi numerals (०-९) are translated to English (0-9) to allow for numerical analysis.

#Regex Feature Extraction: Custom regular expressions identify age ranges and educational requirements from unstructured strings.

#Label Engineering: Data is categorised into standard classes such as 'Graduate', '10th', and 'Post Graduate' for model training.

def extract_age(text):
    text = str(text)
    # // Convert Marathi numbers to English
    text = text.translate(str.maketrans("०१२३४५६७८९", "0123456789"))

    # //Check for range patterns (e.g., 18 to 38)
    match = re.search(r'(\d{2})\s*(?:ते|to|-)\s*(\d{2})', text, re.I)
    if match:
        return f"{match.group(1)}-{match.group(2)}"

    # // Check for "between" pattern
    match = re.search(r'between\s*(\d{2})\s*(\d{2})', text, re.I)
    if match:
        return f"{match.group(1)}-{match.group(2)}"

    # //Fallback if no match is found 
    return "Not Specified"

def extract_labels(text):
    gender = 'General'
    if re.search(r'महिला|स्त्री|female', text, re.I): gender = 'Female'
    elif re.search(r'पुरुष|male', text, re.I): gender = 'Male'

    age = extract_age(text)

    qual = 'Other'
    if re.search(r'पदव्युत्तर|M.A.|M.Sc.|MBA|Post Graduate', text, re.I): qual = 'Post Graduate'
    elif re.search(r'पदवी|Graduate|B.A.|B.Sc.|B.E.|Degree', text, re.I): qual = 'Graduate'
    elif re.search(r'डिप्लोमा|Diploma|ITI', text, re.I): qual = 'Diploma/ITI'
    elif re.search(r'१० वी|10th|SSC' , text, re.I): qual = '10th'
    return pd.Series([gender, age, qual])
df[['Gender','Age','Qualification']] = df['title'].apply(extract_labels)
df = df[df['Qualification'] != 'Other'].copy()



#Feature Extraction: TF-IDF Vectorization
#Feature Extraction: Data is vectorized using TF-IDF to convert text into numerical format for the SVM classification model.
#took help from scikit learn documentation for understanding and implementing concept
# link: https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html

X = df["title"]
y = df[["Qualification", "Age", "Gender"]]
df = df[df["Gender"] !="Unknown"]
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1,2),
    lowercase=False
)
X_vec = vectorizer.fit_transform(X)

# Split dataset into training and testing sets using train_test_split
# used gemini   link : https://gemini.google.com/share/b1b20c9758f4

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)


# Selected useful columns for prediction machine learning
# https://gemini.google.com/share/81ef49a3dbe8
valid_cols = []
for col in ["Qualification", "Age","Gender"]:
    if df[col].nunique() > 1:
        valid_cols.append(col)
        print("using colums:", valid_cols)
        y = df[valid_cols]

# svm model trained for multiclass output

svm_model = MultiOutputClassifier(SVC(kernel='linear'))
svm_model.fit(X_train, y_train[valid_cols])



