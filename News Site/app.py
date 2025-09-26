from flask import Flask, render_template, url_for,request
import requests 
from config import NEWS_API_KEY


#Create a flask app
app = Flask(__name__)


#Homepage
@app.route("/")
def index():
    query = request.args.get("query", "latest")
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url) 
    news_data = response.json() 
    
    articles = news_data.get('articles',[])

    return render_template("index.html", articles=articles)



if __name__ == "__main__":
    app.run(debug=True) 