import tkinter as tk
from main import *

class EntryFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.wordSearch = WordSerach()
        self.wordSearch.startDB()
        self.wordSearch.createDB()

        self.frame = tk.Frame(self.parent)
        self.frame.pack(side=tk.LEFT)

        self.createEntry()

    def createEntry(self):
        self.label = tk.Label(self.frame, text='search word : ')
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self.frame)
        self.entry.pack(side=tk.LEFT)

        self.button = tk.Button(self.frame, text='Search')
        self.button.configure(command=self.searchWord)
        self.button.pack(side=tk.LEFT)

    def searchWord(self):
        word = self.entry.get()

        self.wordSearch.insertDB(word)

        data = self.wordSearch.readAllWord()
        [print(x) for x in data]

        win = ResultMean('aaaa')

class ResultMean(tk.Toplevel):
    def __init__(self, mean):
        super().__init__()
        self.title('Result')

        self.msg = tk.Message(self, text=mean)
        self.msg.pack()

if __name__ == '__main__':
    root = tk.Tk()

    frame = EntryFrame(root, width=200, height=300)
    frame.pack(side=tk.TOP)

    root.mainloop()
