# working test
# app = Application().start("notepad.exe")
#
# app.UntitledNotepad.menu_select("Help->About Notepad")
# app.AboutNotepad.OK.click()
# app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces = True)

from pywinauto import Desktop, Application, mouse, findwindows
import subprocess
import time
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.keyboard import send_keys
from pywinauto import backend
from pyuac import main_requires_admin

userid='PLitv001 /n'
password='Rtbd100{%}'


app = Application().start("notepad.exe")

app.UntitledNotepad.Edit.type_keys(password + "%%", with_spaces = True)
