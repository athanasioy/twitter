"""
Script Responsible for generating tweet stream
"""
import tweepy
from config import config
from tweet_dataclass import Tweet, Author
import json
import requests

class ReponseHandler:
    """ Class used to handle the response from TwitterStream class"""
    @staticmethod
    def extract_data(response: requests.Response) -> Tweet:
        """We will fix things later"""
        response = json.loads(response.decode())
        print(json.dumps(response,sort_keys = True,indent =4 ))
        id = response.get("data").get("id")
        text = response.get("data").get("text")
        created_at = response.get("data").get("created_at")
        author_id = response.get("data").get("author_id")
        retweet_id = response.get("referenced_tweets")
        if retweet_id is not None:
            retweet_id = retweet_id[0].get("id")
        answers_to = response.get("includes").get("tweets")
        if answers_to is not None:
            answers_to = answers_to[0].get("id")
        source = response.get("data").get("source") # need to covert to enum

        return Tweet(id = id,
                     text = text,
                     created_at = created_at,
                     author_id = author_id,
                     retweet_id = retweet_id,
                     reply_to = answers_to
                     )

class TwitterStream(tweepy.StreamingClient):


    def on_data(self, data):
        self.responseHanlder = ReponseHandler()
        print(self.responseHanlder.extract_data(data))


def main() -> None:
    expansions = ['author_id',
                 'in_reply_to_user_id',
                 'referenced_tweets.id',
                 'referenced_tweets.id.author_id',
                 'attachments.media_keys']

    tweet_fields = ['text', 'in_reply_to_user_id', 'created_at', 'source']

    rule = '"Νεα Δημοκρατία" OR ΔΕΘ'
    tag = 'Current News'
    streaming_client = TwitterStream(config.get("bearer_token")) # Set up stream
    streaming_client.add_rules(tweepy.StreamRule(rule,tag))
    print(streaming_client.get_rules())
    streaming_client.filter(expansions = expansions, tweet_fields = tweet_fields)

if __name__ == "__main__":
    main()
