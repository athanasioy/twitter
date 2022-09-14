"""
Script Responsible for generating tweet stream
"""
import tweepy
from config import config
from tweet_dataclass import Tweet, Author


class TwitterStream(tweepy.StreamingClient):

    def on_data(self, data):
        print(data)

    def add_rule(self,rule_text):
        self.add_rules(tweepy.StreamRule(rule_text))


def main() -> None:

    rule = '"Νεα Δημοκρατία" OR ΔΕΘ'

    streaming_client = TwitterStream(config.get("bearer_token")) # Set up stream
    streaming_client.add_rules(rule)
    streaming_client.filter()

if __name__ == "__main__":
    main()
