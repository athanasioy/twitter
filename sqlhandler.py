import pyodbc
from tweet_dataclasses import Tweet,Author


class sqlHandler:
    def __init__(self, conn_string:str) -> None:
        self.connection = pyodb.connect(conn_string) # Creates a connection with DB server
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
        pass

    def check_if_author_exists(self, author: Author):
        """
        Returns None if author doesn't exist
        """
        pass


# Just testing code
# Ignore
def main():
    conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=ATHANANTONIS;DATABASE=Tweeterdb;Trusted_connection=yes'
    conn = pyodbc.connect(conn_string)

    cursor = conn.cursor()
    results = cursor.execute("SELECT * FROM Authors")

    print(results.fetchall())

    conn.close()

if __name__ == "__main__":
    main()
