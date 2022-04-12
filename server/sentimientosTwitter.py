import re 
import io
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 
from googletrans import Translator


class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = 'de0TW93rk1iLWTs4bRZjyHFWU'
		consumer_secret = 'Tgbr2RoK0eg1CMbtbOXLz9Uq8odFiaXheR8OajJDPj5xmoj3i9'
		access_token = '633890208-PTMijlkIcke1yqNqkvpYIqpIda5an0ozboBxX0Gx'
		access_token_secret = 'xORyhr9z142pRoWaeU1QQp8qqzt80aDYsxMxKJutbgszd'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		temp =' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])(\w+:\/\/\S+)", " ", tweet).split()) 
		if temp [0:2]=="RT":
			temp=temp[5:]
		
		if(temp.find("https")!=-1):
			temp=temp[:temp.find("https")]
		
		return temp

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) 
		# set sentiment 
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count, lang= "en", result_type="popular", tweet_mode="extended") 
			translator = Translator()
			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# saving text of tweet 
				# parsed_tweet['text'] = translator.translate(self.clean_tweet(tweet.full_text),src="en",dest="es").text 
				parsed_tweet['text'] = self.clean_tweet(tweet.full_text)
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.full_text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

def scrappingTwitter(pelicula): 
	# creating object of TwitterClient Class 
	api = TwitterClient() 
		# calling function to get tweets 
	tweets = api.get_tweets(query = pelicula , count = 200) 
	salida={}
	salida[pelicula]=[{}]
	# picking positive an negative tweets from tweets 
	ptweets = [tweet["text"] for tweet in tweets if tweet['sentiment'] == 'positive'] 
	ntweets = [tweet["text"] for tweet in tweets if tweet['sentiment'] == 'negative'] 
	neutweets = [tweet["text"] for tweet in tweets if tweet['sentiment'] == 'neutral'] 

	salida[pelicula][0]["PorcentajeTweetsPositivos"]=100*len(ptweets)/len(tweets)		 
	salida[pelicula][0]["PorcentajeTweetsNegativos"]=100*len(ntweets)/len(tweets)
	salida[pelicula][0]["PorcentajeTweetsNeutros"]=100*len( neutweets )/len(tweets)
	salida[pelicula][0]["TweetsBuenos"]=ptweets
	salida[pelicula][0]["TweetsMaloss"]=ntweets
	salida[pelicula][0]["TweetsNeutros"]=neutweets
	return salida

