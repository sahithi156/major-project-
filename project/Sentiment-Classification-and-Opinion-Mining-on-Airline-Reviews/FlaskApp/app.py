from flask import render_template, Flask, request,url_for

import pickle
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

from sentimentanalyzer import getSentiment
from service import getAirlinesSentiment

app = Flask(__name__)


nltk.download("stopwords")

ps = PorterStemmer()

def load_pkl(fname):
    with open(fname, 'rb') as f:
        obj = pickle.load(f)
    return obj

model =load_pkl("xgb.pkl")

def preprocess_post(post):
    p_post = re.sub('[^a-zA-Z]', ' ',post)
    p_post = p_post.lower().split()
    p_post = [ps.stem(word) for word in p_post if word not in stopwords.words('english')]
    p_post = ' '.join(p_post)
    return p_post

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tpredict')
@app.route('/', methods = ['GET','POST'])
def page2():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        airlines=request.form['airlines']
        sentiment=getAirlinesSentiment(airlines)
        topic = request.form['tweet']
        result = getSentiment(topic)
        if(result=="Positive"):
            topic = "Positive Tweet - Hope you will fly with us again"
        elif(result=="Negative"):
            topic = "Negative Tweet - Sorry about that"
        else:
            topic = "Neutral Tweet"
        return render_template('index.html',ypred = topic,sentiment=sentiment)
        

if __name__ == '__main__':
    app.run(host = 'localhost', debug = True , threaded = False)
    
