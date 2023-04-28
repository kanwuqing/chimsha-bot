import ttkbootstrap as tk
from tkinter import Listbox
import pystray
from PIL import Image
from thefuzz import process
import keyboard
import threading
import os
import time


class Entry(tk.Entry):
    def __init__(self, master, placeholder, **kw):
        super().__init__(master, **kw)
 
        self.placeholder = placeholder
        self._is_password = True if placeholder == "password" else False
 
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
 
        self._state = 'placeholder'
        self.insert(0, self.placeholder)
 
    def on_focus_in(self, event):
        if self._is_password:
          self.configure(show='*')
 
        if self._state == 'placeholder':
            self._state = ''
            self.delete('0', 'end')
 
    def on_focus_out(self, event):
        if not self.get():
          if self._is_password:
            self.configure(show='')
 
          self._state = 'placeholder'
          self.insert(0, self.placeholder)

class App(tk.Window):

    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 300
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2))
        self.overrideredirect(True)
        self.attributes('-topmost', 1)
        self.title("Chimsha")
        self._style = tk.Style('solar')
        self.search_entry = Entry(self, placeholder='Hi, Chimsha!')
        self.search_entry.pack()
        self.bind('<KeyPress>', self.load)
        self.bind('<FocusOut>', self.focus_out)
        keyboard.add_hotkey('ctrl+q', self.showhide)
        self.protocol('WM_DELETE_WINDOW', self.on_exit)
        self.bind("<Escape>", self.on_exit)
        self.bind("<B1-Motion>", self.mouse_motion)  # Hold the left mouse button and drag events
        self.bind("<Button-1>", self.mouse_press)  # The left mouse button press event, long calculate by only once
        self.x, self.y = 0, 0
        self.main_window()
        self.hide()

    def load(self, event):
            try:
                loading = self.search_entry.get()
            except:
                ...
            else:
                if loading in ['', None]:
                    return
                # print(process.extract(loading, __COMMAND__, limit=len(__COMMAND__), scorer=fuzz.token_sort_ratio))
                try:
                    self.res.destroy()
                except:
                    ...
                data = process.extract(loading, __COMMAND__, limit=5)
                self.res = Listbox(self)
                for i in data:
                    if i[1] >= 50:
                        self.res.insert(tk.END, str(i[2]))
                self.res.pack()

    def empty(self):
        for widget in self.winfo_children():
            widget.destroy()


    def main_window(self):
        self.empty()
        self.search_entry = Entry(self, placeholder='Hi, Chimsha!')
        self.search_entry.pack()

    def mouse_motion(self, event):
        # Positive offset represent the mouse is moving to the lower right corner, negative moving to the upper left corner
        offset_x, offset_y = event.x - self.x, event.y - self.y  
        new_x = self.winfo_x() + offset_x
        new_y = self.winfo_y() + offset_y
        new_geometry = f"+{new_x}+{new_y}"
        self.geometry(new_geometry)

    def mouse_press(self, event):
        _ = time.time()
        self.x, self.y = event.x, event.y

    def showhide(self):
        if self.state() == 'normal':
            self.update()
            self.withdraw()
            self.empty()
        else:
            self.update()
            self.main_window()
            self.deiconify()
            self.focus_force()
            self.search_entry.focus_set()
    
    def show(self):
        if self.state() == 'normal':
            pass
        else:
            self.update()
            self.main_window()
            self.deiconify()
            self.focus_force()
            self.search_entry.focus_set()
    
    def hide(self):
        if self.state() == 'normal':
            self.update()
            self.withdraw()
            self.empty()
        else:
            pass

    def focus_out(self, event):
        if event.widget == self:
            self.update()
            self.withdraw()
            self.empty()
    
    def on_exit(self, event=None):
        self.withdraw()
        self.empty()

def quit_window():
    icon.stop()
    app.destroy()

def init():
    # softwares = get_window_software(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + get_window_software(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + get_window_software(winreg.HKEY_CURRENT_USER, 0)
    commands = {}
    # for software in softwares:
        # if software['DisplayIcon']:
            # commands[software['name']] = software['DisplayIcon']
    return commands

if __name__ == "__main__":
    __BASEDIR__ = os.path.join('C:\\Users', os.getlogin(), 'Documents\\chimsha')
    if not os.path.isdir(__BASEDIR__):
        os.mkdir(__BASEDIR__)
    __COMMAND__ = init()
    # print(__COMMAND__)
    app = App()
    menu = (pystray.MenuItem('主窗口', lambda: app.show()), pystray.MenuItem('退出', lambda: quit_window()))
    image = Image.open("static/favicon.ico")
    icon = pystray.Icon("name", image, "Chimsha\nTest", menu)
    threading.Thread(target=icon.run, daemon=True).start()
    app.mainloop()