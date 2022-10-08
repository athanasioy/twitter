import tkinter as tk
from tweet_stream import TwitterStream
from sqlhandler import sqlHandler
from config import config
import configparser

class TkView:
    def __init__(self):

        self.root = tk.Tk()

    def generate_UI(self, controller):
        self.frm_buttons = tk.Frame(self.root)
        self.frm_buttons.grid(row = 0 , column = 0)

        self.btn_StartStream= tk.Button(self.frm_buttons, text = "Start Stream", width = 15)
        self.btn_EndStream= tk.Button(self.frm_buttons, text = "End Stream", width = 15)
        self.btn_PostRule= tk.Button(self.frm_buttons, text = "Post Rule", width = 15)
        self.btn_ClearRules= tk.Button(self.frm_buttons, text = "Clear All Rules", width = 15, command = controller.clear_rules)
        self.btn_GetRules= tk.Button(self.frm_buttons, text = "Get All Rules", width = 15, command = controller.fetch_rules)


        self.btn_StartStream.grid(row = 2 , column = 0, sticky = tk.W)
        self.btn_EndStream.grid(row = 3, column = 0, sticky = tk.W)
        self.btn_PostRule.grid(row = 4, column = 0, sticky = tk.W)
        self.btn_ClearRules.grid(row = 5, column = 0, sticky = tk.W)
        self.btn_GetRules.grid(row = 6, column = 0, sticky = tk.W)

        self.frm_console = tk.Frame(self.root)
        self.frm_console.grid(row = 0, column = 1)

        self.lst_console = tk.Listbox(self.frm_console, height = 10, width = 35)
        self.lst_console.grid()

        self.lbl_rules = tk.Label(self.frm_buttons, text = "Rules to Add")
        self.lbl_rules.grid(row = 0, column = 0, sticky = tk.W)
        self.ent_rule = tk.Entry(self.frm_buttons, width = 30)
        self.ent_rule.grid(row= 1, column = 0)

    def start_main_loop(self):
        self.root.mainloop()

    def add_item_to_list(self, item: list):
        self.lst_console.insert(tk.END, item)

    def clear_list(self):
        self.lst_console.delete(0, tk.END)


class Controller:

    def __init__(self, tweetStream: TwitterStream, view: TkView):
        self.TwitterStream = tweetStream
        self.view = view

    def fetch_rules(self):
        rules = self.TwitterStream.get_rules()
        for rule in rules.data:
            self.view.add_item_to_list(rule)

    def start(self):
        self.view.generate_UI(self)
        self.view.start_main_loop()

    def clear_rules(self):
        self.view.clear_list()

def main() -> None:
    conn_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=ATHANANTONIS;DATABASE=Tweeterdb;Trusted_connection=yes'
    sql_handler = sqlHandler(conn_string)
    FIELD_MAPPING = configparser.ConfigParser()
    FIELD_MAPPING.read('sql_config.ini')
    sql_handler.set_field_mapper(FIELD_MAPPING)

    expansions = ['author_id',
                 'in_reply_to_user_id',
                 'referenced_tweets.id',
                 'referenced_tweets.id.author_id',
                 'attachments.media_keys']

    tweet_fields = ['text', 'in_reply_to_user_id', 'created_at', 'source']


    # Create streaming_client
    streaming_client = TwitterStream(bearer_token = config.get("bearer_token"),
                                     sql_handler = sql_handler) # Set up stream

    c = Controller(streaming_client, TkView())
    c.start()


if __name__ == "__main__":
    main()
