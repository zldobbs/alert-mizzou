# imports
import os
from flask import Flask, render_template, request, url_for
import twitter, json, config

# initiatilization
app = Flask(__name__)
# pull the config files from os
twitter_api = twitter.Api(consumer_key = config.twit['consumer_key'],
                          consumer_secret = config.twit['consumer_secret'],
                          access_token_key = config.twit['access_token_key'],
                          access_token_secret = config.twit['access_token_secret'])

# get the tweets
def get_tweets(username, num):
    try:
        tweets = twitter_api.GetUserTimeline(screen_name=username, count=num)
    except twitter.error.TwitterError:
        tweets = twitter_api.GetUserTimeline(screen_name='realDonaldTrump', count=10)
    return [{   'tweet': t.text,
                'created_at': t.created_at,
                'username': t.user.name,
                'screenname': t.user.screen_name,
                'headshot_url': t.user.profile_image_url}
            for t in tweets]

# post message to groupme, not doing right now...
# def send_message(msg):
#     url = 'https://api.groupme.com/v3/bots/post'
#     values = {
#             'bot_id' : '83b8d1283d546c425282df1754',
#             'text'   : msg
#     }
#     data = urllib.urlencode(values)
#     data = data.encode('json')
#     request = Request(url, urlencode(data).encode())
#     json = urlopen(request).read().decode()
#     return None

# render home page with tweets
@app.route('/', methods=['GET'])
def page():
    # testing page with Donnie
    # send_message('hello!')
    username = '@realDonaldTrump'
    amount = 10
    if request.args.get('username'):
        username = request.args.get('username')
    if request.args.get('amount'):
        amount = request.args.get('amount')
    return render_template('page.html', tweets=get_tweets(username, amount))

# route for groupme bot, disabled for now
# @app.route('/botRequest', methods=['POST'])
# def request_received():
#     data = request.get_json(force=True)
#     if data['text'] == 'donnie!':
#         msg = 'Build that wall!'
#         send_message(msg)
#     return "ok", 200
