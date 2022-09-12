'''
script contating the main dataclasses that will be passed into sqlHandler
'''


from dataclasses import dataclass
from datetime import datetime


@dataclass
class Tweet:
    id: int
    text: str
    created_at: datetime
    author_id: int
    retweet_id: int # None if not a retweet
    reference_type: enum
    reply_to: int # None if doesn't reply
    source: enum

@dataclass
class Author:
    id: int
    name: str
    username: str
    creation_date: datetime
