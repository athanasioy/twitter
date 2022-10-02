import tkinter as tk


class TkView:
    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("600x400")

        self.button_frm = tk.Frame(self.root)
        self.button_frm.grid(row = 0 , column = 0)

        self.b_StartStream= tk.Button(self.button_frm, text = "Start Stream")
        self.b_EndStream= tk.Button(self.button_frm, text = "End Stream")
        self.b_PostRule= tk.Button(self.button_frm, text = "Post Rule")
        self.b_ClearRules= tk.Button(self.button_frm, text = "Clear All Rules")
        self.b_GetRules= tk.Button(self.button_frm, text = "Get All Rules")


        self.b_StartStream.grid(row = 1 , column = 0)
        self.b_EndStream.grid(row = 2, column = 0)
        self.b_PostRule.grid(row = 3, column = 0)
        self.b_ClearRules.grid(row = 4, column = 0)
        self.b_GetRules.grid(row = 5, column = 0)

        self.box_frm = tk.Frame(self.root)
        self.box_frm.grid(row = 0, column = 2)

        self.console = tk.Listbox(self.box_frm, height = 20, width = 35)
        self.console.grid(rowspan = 5)


        self.ent_rule = tk.Entry(self.button_frm, width = 50)
        self.ent_rule.grid(row= 0, column = 0)

    def start_main_loop(self):
        self.root.mainloop()

def main() -> None:
    view = TkView()
    view.start_main_loop()


if __name__ == "__main__":
    main()
