"""
Script Responsible for generating tweet stream
"""
import tweepy
from sqlhandler import sqlHandler
from config import config
from responseHandler import StreamReponseHandler


class TwitterStream(tweepy.StreamingClient):

    def __init__(self, bearer_token: str, sql_handler: sqlHandler):
        self.sql_handler = sql_handler
        self.responseHanlder = StreamReponseHandler()
        super().__init__(bearer_token)


    def on_data(self, data):

        tweet = self.responseHanlder.extract_tweet_data(data)
        print(tweet)
        author = self.responseHanlder.extract_author_data(data)
        print(author)
        self.sql_handler.insert_dataclass(tweet, table_name = "Tweets")
        self.sql_handler.insert_dataclass(author, table_name = "Authors")


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
    FIELD_MAPPING = {"Tweets":{"id": "id",
                                "author_id": "author_id",
                                "created_at": "created_at",
                                "text": "tweet_text",
                                "retweet_id": "referenced_tweet",
                                "reference_type": "reference_type",
                                "reply_to": "AnswersTo",
                                "source": "source",
                                "has_media": "has_media",
                                "media_type": "media_type"},
                     "Authors":{"id": "id",
                                "name": "name",
                                "username": "username",
                                "creation_date": "creation_date"}}

    sql_handler.set_field_mapper(FIELD_MAPPING)

    # Create streaming_client
    streaming_client = TwitterStream(bearer_token = config.get("bearer_token"),
                                     sql_handler = sql_handler) # Set up stream
    # Add rule
    streaming_client.add_rules(tweepy.StreamRule(value = rule, tag = tag))
    print(streaming_client.get_rules())
    # Run Stream
    streaming_client.filter(expansions = expansions, tweet_fields = tweet_fields)

if __name__ == "__main__":
    main()
