from flask import Flask
from flask import render_template
from flask import request
import feedparser
import json
import urllib
from urllib.request import urlopen


app = Flask(__name__)

FEED_XML = {'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
 'CNN': 'http://rss.cnn.com/rss/edition.rss',
 'FOX': 'http://feeds.foxnews.com/foxnews/latest',
 'IOL': 'http://www.iol.co.za/cmlink/1.640'}

DEFAULTS = {'publication':'BBC',
            'city':'London,UK',
            'from_currency':'USD',
            'to_currency':'INR'}
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=944b5e07f7fedc2937f8c5731b5317f2'
CURRENCY_URL = 'https://openexchangerates.org//api/latest.json?app_id=6a34d4a80810464cbb3af49a8e23300f'

@app.route('/')
def home():
    publication = request.args.get('publication')
    if not publication:
        publication=DEFAULTS['publication']
    channel=publication
    print(channel)
    articles = get_news(publication)
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather,city_query,error = get_weather(city)
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULTS['from_currency']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['to_currency']
    rate,currencies = get_rate(currency_from,currency_to)

    return render_template('home.html',articles=articles,channel=channel,channels=FEED_XML.keys(),
                           rate=rate,currency_from=currency_from,currency_to=currency_to,currencies=currencies,
                           weather=weather,city=city_query,
                           error=error)

def get_news(query):
    if not query or query.upper() not in FEED_XML:
        publication=DEFAULTS['publication']
    else:
        publication = query.upper()
    feed = feedparser.parse(FEED_XML[publication])
    return feed['entries']

def get_weather(query):
    error=0
    weather = None
    try:
     url = WEATHER_URL.format(query)
     data = urlopen(url).read()
     parsed = json.loads(data.decode('utf8'))
     if parsed.get('weather'):
        weather = {"description":
         parsed["weather"][0]["description"],
        "temperature":parsed["main"]["temp"],
         "city":parsed["name"],
        }
     else:
        return (None,query,404)
    except:
        error=404
    return (weather,query,error)

def get_rate(frm,to):
    all_currency = urlopen(CURRENCY_URL).read()
    parsed = json.loads(all_currency.decode('utf8'))
    print(frm,to)
    frm_rate = parsed.get('rates', {}).get(frm.upper())
    to_rate = parsed.get('rates', {}).get(to.upper())
    if frm_rate is None or to_rate is None or frm_rate == 0:
        raise ValueError("Invalid exchange rate data.")
    parsed_rates = parsed['rates']
    currencies = parsed_rates.keys()
    return (to_rate/frm_rate,currencies)


if __name__=='__main__':
    app.run(port=5000,debug=True)




    
