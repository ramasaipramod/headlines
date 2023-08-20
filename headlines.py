from flask import Flask
from flask import render_template
from flask import request
import feedparser

app = Flask(__name__)

FEED_XML = RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
 'cnn': 'http://rss.cnn.com/rss/edition.rss',
 'fox': 'http://feeds.foxnews.com/foxnews/latest',
 'iol': 'http://www.iol.co.za/cmlink/1.640'}

@app.route('/',methods=['GET','POST'])
def get_news():
    query = request.form.get('publication')
    if not query or query.lower() not in FEED_XML:
        publication='bbc'
    else:
        publication=query.lower()
    feed = feedparser.parse(FEED_XML[publication])
    return render_template('home.html',articles=feed['entries'],channel=publication)

if __name__=='__main__':
    app.run(port=5000,debug=True)