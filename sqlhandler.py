import pyodbc
from tweet_dataclass import Tweet,Author
from datetime import datetime
from dataclasses import fields


class sqlHandler:
    def __init__(self, conn_string:str) -> None:
        self.connection = pyodbc.connect(conn_string) # Creates a connection with DB server
        self.cursor = self.connection.cursor()

    def insert_users(self, author: Author):
        """
        Inserts a user into the authors table.
        """
        #something like ...
        self.cursor.execute("INSERT INTO Authors () values (?,?...)",params)
        pass
    def insert_tweets(self, tweet: Tweet):
        """
        Inserts a tweet into the Tweets Table.
        Before inserting, it checks if the author exists into the authors table
        """
        fields_to_insert = '('
        for field in fields(tweet):
            fields_to_insert += field.name + ','
        fields_to_insert = fields_to_insert[:-1]+')'
        print(fields_to_insert)
        # sql_text = "INSERT INTO Tweets (id)"

    def check_if_author_exists(self, author: Author):
        """
        Returns None if author doesn't exist
        """
        pass

    def close_connection(self) -> None:
        self.connection.close()

# Just testing code
# Ignore
def main():
    conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=ATHANANTONIS;DATABASE=Tweeterdb;Trusted_connection=yes'
    sql_handler = sqlHandler(conn_string)

    test_tweet = Tweet(id = -1,
                       author_id = 999,
                       created_at = datetime.now(),
                       text = "This is a test tweet",
                       retweet_id = 123,
                       reference_type = 1,
                       reply_to = 232323,
                       source = 1)
    sql_handler.insert_tweets(test_tweet)

    sql_handler.close_connection()

if __name__ == "__main__":
    main()
