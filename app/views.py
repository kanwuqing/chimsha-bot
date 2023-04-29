import ttkbootstrap as tk
import threading

class App(tk.Window):
    def __init__(self, title="ttkbootstrap", themename="solar", iconphoto='', size=None, position=None, minsize=None, maxsize=None, resizable=None, hdpi=True, scaling=None, transient=None, overrideredirect=False, alpha=1):
        super().__init__(title, themename, iconphoto, size, position, minsize, maxsize, resizable, hdpi, scaling, transient, overrideredirect, alpha)
        self.width = 800
        self.height = 300
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2))
        self.overrideredirect(True)
        self.attributes('-topmost', 1)
        self.title("Chimsha")
        self.bind('<FocusOut>', lambda event: self.thread_it(self.focus_out, event))
    
    def empty(self):
        for widget in self.winfo_children():
            widget.destroy()

    def focus_out(self, event):
        print(event)
        if event.widget == self:
            self.withdraw()
            self.empty()
        return

    @staticmethod
    def thread_it(func, *args):
        t = threading.Thread(target=func, args=args) 
        t.setDaemon(True)
        t.start() 