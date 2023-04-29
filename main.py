import os
from app import *

if __name__ == '__main__':
    _basedir_ = os.path.join('C:\\Users', os.getlogin(), 'Documents\\chimsha')
    if not os.path.isdir(_basedir_):
        os.mkdir(_basedir_)
    app = App()
    app.mainloop()