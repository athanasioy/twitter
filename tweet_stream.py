"""
Script Responsible for generating tweet stream
"""
import tweepy
from config import config
from tweet_dataclass import Tweet, Author, tweet_source, reference_type
import json
import requests


class ReponseHandler:

    def __init__(self) -> None:
        # We are hard-coding enums because they will not change frequently
        self.source_enum_mapper = {"Twitter for Android": tweet_source.Android,
                                   "Twitter Web App": tweet_source.Web_App,
                                   "Twitter for iPhone": tweet_source.iPhone,
                                   "Twitter for iPad": tweet_source.iPad}

        self.reference_type_enum = {"retweeted": reference_type.retweet,
                                    "replied_to": reference_type.replied_to,
                                    "quoted": reference_type.quoted}
    def source_enum_mapper(self, value: str) -> Enum:
        return self.source_enum_mapper.get(value)

    def reference_type_enum_mapper(self, value: str) -> Enum:
        return self.source_enum_mapper.get(value)

class StreamReponseHandler(ResponseHanlder):
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
        source = response.get("data").get("source") # need to covert to enum

        retweet_id = response.get("data").get("referenced_tweets")

        if retweet_id is not None:
            retweet_id = retweet_id[0].get("id") # Get reply_tweet_id

            answers_to = response.get("includes").get("tweets")
            answers_to = answers_to[0].get("author_id") # get the author id of the reply
            reference_type = response.get("data").get("referenced_tweets")
            reference_type = reference_type[0].get("type") # need to convert to enum


        return Tweet(id = id,
                     text = text,
                     created_at = created_at,
                     author_id = author_id,
                     retweet_id = retweet_id,
                     reply_to = answers_to
                     )

class TwitterStream(tweepy.StreamingClient):


    def on_data(self, data):
        self.responseHanlder = StreamReponseHandler()
        print(self.responseHanlder.extract_data(data))


def main() -> None:
    expansions = ['author_id',
                 'in_reply_to_user_id',
                 'referenced_tweets.id',
                 'referenced_tweets.id.author_id',
                 'attachments.media_keys']

    tweet_fields = ['text', 'in_reply_to_user_id', 'created_at', 'source']

    rule = '#πανεπιστημιακη_αστυνομια OR #ΝΔ'
    tag = 'Current News'

    streaming_client = TwitterStream(config.get("bearer_token")) # Set up stream
    streaming_client.delete_rules(['1570102941805150212', '1570843677123018753'])
    streaming_client.add_rules(tweepy.StreamRule(rule,tag))
    print(streaming_client.get_rules())
    streaming_client.filter(expansions = expansions, tweet_fields = tweet_fields)

if __name__ == "__main__":
    main()
