import configparser
import UI
from tweet_stream import TwitterStream
from sqlhandler import sqlHandler
from config import config

def main() -> None:
    # Set up SqlHandler

    sql_config = configparser.ConfigParser()
    sql_config.read('sql_config.ini')

    conn_string = sql_config['connection_string']['conn_string']
    sql_handler = sqlHandler(conn_string)
    sql_handler.set_field_mapper(sql_config)

    # Set up TwitterStream

    streaming_client = TwitterStream(
                                     bearer_token = config.get("bearer_token"),
                                     sql_handler = sql_handler,
                                     daemon = True
                        ) # Set up stream

    # Set up Controller GUI
    Controller = UI.Controller(streaming_client, UI.TkView())
    Controller.start()


main()
