import json
import requests
from tweet_dataclass import Tweet, Author, tweet_source, reference_type, media_type
from typing import List

class ResponseHandler:

    def __init__(self) -> None:
        # We are hard-coding enums because they will not change frequently
        self.source_enum_mapper = {"Twitter for Android": tweet_source.Android.value,
                                   "Twitter Web App": tweet_source.Web_App.value,
                                   "Twitter for iPhone": tweet_source.iPhone.value,
                                   "Twitter for iPad": tweet_source.iPad.value}

        self.reference_type_mapper = {"retweeted": reference_type.retweet.value,
                                    "replied_to": reference_type.replied_to.value,
                                    "quoted": reference_type.quoted.value}

        self.media_type_mapper = {"video": media_type.video.value,
                                  "GIF": media_type.GIF.value,
                                  "photo": media_type.photo.value}


    def get_source_value(self, value: str) -> tweet_source:
        """
        Used to convert the source field from string to Enum.
        """
        return self.source_enum_mapper.get(value,tweet_source.Other.value)

    def get_referenceType_value(self, value: str) -> reference_type:
        """
        Used to convert the reference_type field from string to Enum.
        """
        return self.reference_type_mapper.get(value)

    def get_media_type_value(self, value: str) -> media_type:
        return self.media_type_mapper.get(value)

    @staticmethod
    def get_result_from_iter(response_list: List[dict], value: str) -> str:
        """
        Used to deal with nested structures in dictionaries where the value is a list.
        Problems occur when tried to reference items from non existent list
        Returns the value of a key-value pair inside a dictionary
        """
        if response_list is None:
            return None

        value = next((x[value] for x in response_list), None)

        return value
class StreamReponseHandler(ResponseHandler):
    """ Class used to handle the response from TwitterStream class"""

    def extract_tweet_data(self, response: requests.Response) -> Tweet:
        """We will fix things later"""

        answers_to: int = None
        reference_type: reference_type = None
        response = json.loads(response.decode())
        print(json.dumps(response,sort_keys = True,indent =4 ))

        id = response.get("data").get("id")
        text = response.get("data").get("text")
        created_at = response.get("data").get("created_at")
        author_id = response.get("data").get("author_id")
        source = response.get("data").get("source") # need to covert to enum
        source = self.get_source_value(source)

        # Set up referenced_tweet iterator
        referenced_tweets = response.get("data").get("referenced_tweets")

        retweet_id = self.get_result_from_iter(referenced_tweets, "id")
        reference_type = self.get_result_from_iter(referenced_tweets, "type")
        reference_type = self.get_referenceType_value(reference_type) # Convert to Enum

        # Set up includes iterator
        includes_tweets = response.get("includes").get("tweets")
        answers_to = self.get_result_from_iter(includes_tweets, "author_id")

        # Set up attachments iterator
        includes_media = response.get("includes").get("media")
        media = self.get_result_from_iter(includes_media, "type")
        media = self.get_media_type_value(media)

        has_media = False
        if media:
            has_media = True

        return Tweet(id = id,
                     text = text,
                     created_at = created_at,
                     author_id = author_id,
                     retweet_id = retweet_id,
                     reply_to = answers_to,
                     source = source,
                     reference_type = reference_type,
                     has_media = has_media,
                     media_type = media
                     )

    def extract_author_data(self, response: requests.Response) -> Author:
        """ Create an Author object from the twitter response"""
        response = json.loads(response.decode())

        author_id = response.get("data").get("author_id")
        username = response.get("includes").get("users") # Returns a List
        # Returns the first username with the author_id
        name = next((value['name'] for value in username if value['id'] == author_id), None)
        username = next((value['username'] for value in username if value['id'] == author_id), None)

        return Author(id = author_id,
                      name = name,
                      username = username)
