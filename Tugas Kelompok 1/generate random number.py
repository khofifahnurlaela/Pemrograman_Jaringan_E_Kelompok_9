import tkinter as tk
import random

class Window:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.text = tk.StringVar()
        self.text.set(random.randint(1, 10))
        self.ranNumLabel = tk.Label(self.frame, textvariable = self.text)
        self.genButton = tk.Button(self.frame, text = 'Generate Random Number', command = self.genRanNum)
        self.ranNumLabel.grid(row = 0)
        self.genButton.grid(row = 1)
        self.frame.grid()

    def genRanNum(self):
        self.text.set(random.randint(1, 10))
        # when text is updated, the Label associated with it also updated

def main():
    root = tk.Tk(className = ' Random Number Generator')
    app = Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()