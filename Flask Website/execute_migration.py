import os


os.system('cmd /c"rmdir /Q /S migrations"')
os.system('cmd /c"del project\data.db"')
os.system('cmd /c"flask db init"')
os.system('cmd /c"flask db migrate"')
os.system('cmd /c"flask db upgrade"')