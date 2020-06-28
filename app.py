# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')



def find_keywords(corpus,top_N):
  vectorizer = TfidfVectorizer()
  vectors = vectorizer.fit_transform(corpus)
  names = vectorizer.get_feature_names()
  data = vectors.todense().tolist()
  # Create a dataframe with the results
  df = pd.DataFrame(data, columns=names)

  #nltk.download('stopwords')
  st = set(stopwords.words('english'))
  #remove all columns containing a stop word from the resultant dataframe. 
  df = df[filter(lambda x: x not in list(st) , df.columns)]
  keywords_ = []
  N = 10;
  #print(df)
  #print(len(N))
  for i in df.iterrows():
      #print('ok')
      k = (i[1].sort_values(ascending=False)[:N])
      #print('ok2')
      keywords_ = list(k.keys())

  #print(keywords_)
  return keywords_

def input_text(text,top_N):
  #text = input('Enter Your Text :')
  #top_N = int(input('Enter how many keywords you want to extract :'))
  text = text.replace('.',' ')
  text = re.sub(r'\s+',' ',re.sub(r'[^\w \s]','',text) ).lower()
  corpus = re.split('chapter \d+',text)
  keywords = find_keywords(corpus,top_N)
  #print(keywords)
  return keywords


# app
app = Flask(__name__)


# routes
@app.route("/",methods=['POST'])
def predict():
    
    data = request.get_json(force=True)
    print(data)
    text = data['text']
    N = int(data['top_N'])
    keywords = input_text(text,N)
    response = {
        'results':keywords
        }
    
    
    return jsonify(results=response)

if __name__ == '__main__':
    app.run(port = 5000)

    
