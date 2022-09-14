## Tweeter API Data
### Rules
We first need to build some rules if we are to stream data

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
