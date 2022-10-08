import tkinter as tk
from tweet_stream import TwitterStream

class TkView:
    def __init__(self):

        self.root = tk.Tk()
#        self.root.geometry("600x400")

        self.frm_buttons = tk.Frame(self.root)
        self.frm_buttons.grid(row = 0 , column = 0)

        self.btn_StartStream= tk.Button(self.frm_buttons, text = "Start Stream", width = 15)
        self.btn_EndStream= tk.Button(self.frm_buttons, text = "End Stream", width = 15)
        self.btn_PostRule= tk.Button(self.frm_buttons, text = "Post Rule", width = 15)
        self.btn_ClearRules= tk.Button(self.frm_buttons, text = "Clear All Rules", width = 15)
        self.btn_GetRules= tk.Button(self.frm_buttons, text = "Get All Rules", width = 15)


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

class Controller:

    def __init__(self, tweetStream: TwitterStream, view: TkView):
        self.TwitterStream = tweetStream
        self.view = view


def main() -> None:
    view = TkView()
    view.start_main_loop()


if __name__ == "__main__":
    main()
