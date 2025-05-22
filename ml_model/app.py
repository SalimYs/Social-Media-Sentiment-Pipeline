import os
import logging
import joblib
from flask import Flask, request, jsonify
from dotenv import load\_dotenv

logging.basicConfig(level=logging.INFO)
load\_dotenv()
app=Flask(**name**)
model=joblib.load('model.pkl')
vec=joblib.load('vectorizer.pkl')

@app.route('/predict',methods=\['POST'])
def predict():
text=request.json.get('text','')
proc=' '.join(\[w for w in text.lower().split() if w\.isalpha()])
vect=vec.transform(\[proc])
res=model.predict(vect)\[0]
return jsonify({'sentiment'\:res})

@app.route('/health')
def health():
return jsonify({'status':'ok'})

if **name**=='**main**':
app.run(host='0.0.0.0',port=5000)

