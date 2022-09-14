'''
script contating the main dataclasses that will be passed into sqlHandler
'''


from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

class reference_type(Enum):
    retweet = 1
    replied_to = 2


class tweet_source(Enum):
    android = 1
    ipad = 2
    web_app = 3

@dataclass
class Tweet:
    id: int
    text: str
    created_at: datetime
    author_id: int
    retweet_id: int = None # None if not a retweet
    reference_type: reference_type = None
    reply_to: int = None # None if doesn't reply
    source: tweet_source = None

@dataclass
class Author:
    id: int
    name: str
    username: str
    creation_date: datetime
