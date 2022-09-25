import json
import requests
from tweet_dataclass import Tweet, Author, tweet_source, reference_type

class ResponseHandler:

    def __init__(self) -> None:
        # We are hard-coding enums because they will not change frequently
        self.source_enum_mapper = {"Twitter for Android": tweet_source.Android.value,
                                   "Twitter Web App": tweet_source.Web_App.value,
                                   "Twitter for iPhone": tweet_source.iPhone.value,
                                   "Twitter for iPad": tweet_source.iPad.value}

        self.reference_type_enum = {"retweeted": reference_type.retweet.value,
                                    "replied_to": reference_type.replied_to.value,
                                    "quoted": reference_type.quoted.value}


    def get_source_value(self, value: str) -> tweet_source:
        """
        Used to convert the source field from string to Enum.
        """
        return self.source_enum_mapper.get(value,tweet_source.Other.value)

    def get_referenceType_value(self, value: str) -> reference_type:
        """
        Used to convert the reference_type field from string to Enum.
        """
        return self.reference_type_enum.get(value)

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

        retweet_id = response.get("data").get("referenced_tweets")

        if retweet_id is not None:
            retweet_id = retweet_id[0].get("id") # Get reply_tweet_id

            answers_to = response.get("includes").get("tweets")
            answers_to = answers_to[0].get("author_id") # get the author id of the reply
            reference_type = response.get("data").get("referenced_tweets")
            reference_type = reference_type[0].get("type") # need to convert to enum
            reference_type = self.get_referenceType_value(reference_type)

        has_media = response.get("includes").get("tweets")
        if has_media is not None:
            has_media = has_media[0].get("attachments").get("media_keys")

        if has_media is not None:
            has_media = True
        else:
            has_media = False

        return Tweet(id = id,
                     text = text,
                     created_at = created_at,
                     author_id = author_id,
                     retweet_id = retweet_id,
                     reply_to = answers_to,
                     source = source,
                     reference_type = reference_type,
                     has_media = has_media
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
