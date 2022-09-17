import pyodbc
from tweet_dataclass import Tweet,Author
from datetime import datetime
from dataclasses import fields


class sqlHandler:
    def __init__(self, conn_string:str) -> None:
        self.connection = pyodbc.connect(conn_string) # Creates a connection with DB server
        self.cursor = self.connection.cursor()

    def insert_users(self, author: Author) -> None:
        """
        Inserts a user into the authors table.
        """
        #something like ...
        self.cursor.execute("INSERT INTO Authors () values (?,?...)",params)
        pass

    def set_field_mapper(self,map_dict: dict) -> None:
        """Sets the field mapper dict into a class variable"""
        self.field_mapping = map_dict

    def insert_parameter_builder(self, tweet: Tweet) -> str:
        fields_to_insert = '('
        params = '('
        for field in fields(tweet):
            fields_to_insert += self.field_mapper("Tweets",field.name) + ', '
            params += '?' + ', '
        fields_to_insert = fields_to_insert[:-2]+')' # [:-2] gets rid of the last comma
        params = params[:-2]+')' # [:-2] gets rid of the last comma

        return (fields_to_insert,params)

    def insert_tweets(self, tweet: Tweet) -> None:
        """
        Inserts a tweet into the Tweets Table.
        """
        if self.check_row_existance(table_name="Tweets", id=tweet.id):
            print("Row already exists!")
            return
        
        sql_statement = "INSERT INTO Tweets "
        fields_to_insert, params = self.insert_parameter_builder(tweet)
        sql_statement += fields_to_insert + " VALUES" + params

        tweet_params = tuple(getattr(tweet,value.name) for value in fields(tweet))
        self.cursor.execute(sql_statement, tweet_params)
        self.cursor.commit()


    def field_mapper(self, table_name:str, field_name: str) -> str:
        """Gets as input the field name from the python dataclass
        and returns the field corresponding to the database table"""

        return self.field_mapping.get(table_name).get(field_name)

    def check_row_existance(self,table_name: str, id: str) -> bool:
        """
        Returns true if row exists
        """
        sql_statement = "SELECT count(*) FROM "
        sql_statement += table_name +" WHERE id = ?"
        self.cursor.execute(sql_statement,str(id))
        result = self.cursor.fetchone()
        return result[0] > 0

    def close_connection(self) -> None:
        self.connection.close()

# Just testing code
# Ignore
def main():
    conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=ATHANANTONIS;DATABASE=Tweeterdb;Trusted_connection=yes'
    sql_handler = sqlHandler(conn_string)
    FIELD_MAPPING = {"Tweets":{"id": "id",
                                "author_id": "author_id",
                                "created_at": "created_at",
                                "text": "tweet_text",
                                "retweet_id": "referenced_tweet",
                                "reference_type": "reference_type",
                                "reply_to": "AnswersTo",
                                "source": "source"}}

    sql_handler.set_field_mapper(FIELD_MAPPING)

    test_tweet = Tweet(id = -3,
                       author_id = 999,
                       created_at = datetime.now(),
                       text = "this is another test tweet",
                       retweet_id = 123,
                       reference_type = 1,
                       reply_to = 232323,
                       source = 1)
    sql_handler.insert_tweets(test_tweet)

    sql_handler.close_connection()

if __name__ == "__main__":
    main()
