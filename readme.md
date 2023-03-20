## Tweeter API Data

## Summary
A pet project which utilizes Twitter API.
A UI is built to easily view, post and delete rules of Twitter's filter endpoint.
The filter endpoint generates relevant tweets given the filter's rule in real time.

The tweets are scraped and inserted into a local SQL Database.

## How to Run

1. Code expects a `config` dictionary in config.py inside the TwitterScrapper folder. The Dictionary should have a `bearer_token` as key (this assumes a Twitter API Account).
2. A connection string set up in databaseHandler\sql_config.ini
3. run main.py

## Data
### Rules
We post relevant to our research to the Twitter's Filter endpoit.
### Tweet Data Saving
**For Tweets**
We will save
- Tweet ID
- Tweet Text
- Tweet creation data
- Author ID
- Retweet ID (referenced_tweets.id)
- AnswersTo (in_reply_to_user_id)
- Source

**For Users**
- User ID
- name
- Username
- Creation Date

### Workflow

- Scrap Tweets
- Before Inserting, check if author exists in the Authors Table
- If Exists, proceed with inserting the tweet
- If doesn't exists, insert author and proceed with inserting the tweet
