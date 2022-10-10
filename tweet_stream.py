"""
Script Responsible for generating tweet stream
"""
import tweepy
import json
import configparser
from sqlhandler import sqlHandler
from config import config
from responseHandler import StreamReponseHandler
from sqlhandler import dataclassHandler


class TwitterStream(tweepy.StreamingClient):

    def __init__(self, bearer_token: str, dataclassHandler: dataclassHandler, daemon: bool = False):
        self.dataclassHandler = dataclassHandler
        self.responseHanlder = StreamReponseHandler()
        super().__init__(bearer_token, daemon = daemon)


    def on_data(self, data):
        tweet = self.responseHanlder.extract_tweet_data(data)
        print(tweet)
        author = self.responseHanlder.extract_author_data(data)
        print(author)
        self.dataclassHandler.handle_dataclass(tweet)
        self.dataclassHandler.handle_dataclass(author)

    def clear_rules(self) -> None:
        """
        Clears all posted rules from stream
        """
        posted_rules = self.get_rules()
        ids = [rule.id for rule in posted_rules.data]
        print(ids)
        self.delete_rules(ids)

def main() -> None:
    #Define Stream Parameters
    expansions = ['author_id',
                 'in_reply_to_user_id',
                 'referenced_tweets.id',
                 'referenced_tweets.id.author_id',
                 'attachments.media_keys']

    tweet_fields = ['text', 'in_reply_to_user_id', 'created_at', 'source']

    # Define Stream Rules
    rule = '#πανεπιστημιακη_αστυνομια OR #ΝΔ OR #ΣΥΡΙΖΑ OR #Τσίπρας OR #ΤΣΙΠΡΑΣ OR Νοτοπούλου OR #ΑΠΘ OR Τσιπρας OR Τσίπρας OR #antireport OR Μητσοτάκης OR Μητσοτακης'
    tag = 'Current News2'

    # Intiliaze sqlHandler
    conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=ATHANANTONIS;DATABASE=Tweeterdb;Trusted_connection=yes'
    sql_handler = sqlHandler(conn_string)
    FIELD_MAPPING = configparser.ConfigParser()
    FIELD_MAPPING.read('sql_config.ini')
    sql_handler.set_field_mapper(FIELD_MAPPING)

    # Create streaming_client
    streaming_client = TwitterStream(bearer_token = config.get("bearer_token"),
                                     dataclassHandler = sql_handler, daemon = True) # Set up stream
    # Add rule
    streaming_client.add_rules(tweepy.StreamRule(value = rule, tag = tag))
    print(streaming_client.get_rules())
    streaming_client.clear_rules()
    # Run Stream
    #streaming_client.filter(expansions = expansions, tweet_fields = tweet_fields)

if __name__ == "__main__":
    main()
