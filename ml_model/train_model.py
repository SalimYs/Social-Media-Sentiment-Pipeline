import os
import logging
import nltk
import joblib
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word\_tokenize
from sklearn.feature\_extraction.text import TfidfVectorizer
from sklearn.linear\_model import LogisticRegression
from sklearn.model\_selection import train\_test\_split
from sklearn.metrics import classification\_report

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(**name**)

nltk.download('punkt')
nltk.download('stopwords')

def preprocess(text):
tokens = \[w for w in word\_tokenize(text.lower()) if w\.isalpha() and w not in stopwords.words('english')]
return ' '.join(tokens)

data = pd.DataFrame({'text':\[], 'sentiment':\[]})

# load your dataset here

X = TfidfVectorizer(max\_features=1000).fit\_transform(data\['text'].apply(preprocess))
y = data\['sentiment']
X\_train,X\_test,y\_train,y\_test = train\_test\_split(X,y,test\_size=0.2,random\_state=42)
model = LogisticRegression(max\_iter=1000).fit(X\_train,y\_train)
pred = model.predict(X\_test)
logger.info(classification\_report(y\_test,pred))
joblib.dump(model,'model.pkl')
joblib.dump(TfidfVectorizer(max\_features=1000),'vectorizer.pkl')

