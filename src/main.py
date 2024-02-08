#!/usr/bin/env python

from feed import Feed
import tweepy, feedparser, sqlite3, time

DATABASE = '../database/se_entries.db'

# Feed(Name, XML, Hashtags)
FEEDS = [ Feed('Ethereum Stack Exchange', 'https://ethereum.stackexchange.com/feeds', '#ethereum') ]

# Define the net max length of the text portion of a tweet
TWEET_MAX_LENGTH = 140
TWEET_URL_LENGTH = 23
TWEET_NET_LENGTH = TWEET_MAX_LENGTH - TWEET_URL_LENGTH

# Twitter Account Keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

def init_twitter():
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)
	return api

def post_tweet(api):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS SEContent (`url`, `title`, `dateAdded`)')

    for feed in FEEDS:
        parsed_feed = feedparser.parse(feed.get_url())

        for entry in parsed_feed.entries:

			c.execute('SELECT * FROM SEContent WHERE url=?', (entry.link,))
			if not c.fetchall():

				data = (entry.link, entry.title, time.strftime("%Y-%m-%d %H:%M:%S", entry.updated_parsed))
				c.execute('INSERT INTO SEContent (`url`, `title`, `dateAdded`) VALUES (?,?,?)', data)

				tweet_body = entry.title.encode('utf-8')

				if len(tweet_body) > 106:
					tweet_body = tweet_body[:106]

				hashtag_length = TWEET_NET_LENGTH - len(tweet_body) - 2

				question_tags = ''
				new_hashtag = ''
				next_tag = ''

				for item in entry.tags:
					next_tag = ' #' + item.term.replace('-', '')
					new_hashtag = feed.get_hashtag() + question_tags + next_tag
					if len(new_hashtag) <= hashtag_length:
						question_tags = question_tags + next_tag

				tweet_url = entry.link.encode('utf-8')
				tweet_hashtag = feed.get_hashtag() + question_tags
				tweet_text = "%s %s %s" % (tweet_body, tweet_url, tweet_hashtag)
				print " ", time.strftime("%c"), "-", tweet_text
				api.update_status(tweet_text)

        conn.commit()
        conn.close()

if __name__ == '__main__':
	api = init_twitter()
	post_tweet(api)
