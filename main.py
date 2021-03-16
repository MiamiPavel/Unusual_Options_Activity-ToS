#pywinauto manual, https://readthedocs.org/projects/airelil-pywinauto/downloads/pdf/latest/

# working test
# app = Application().start("notepad.exe")
#
# app.UntitledNotepad.menu_select("Help->About Notepad")
# app.AboutNotepad.OK.click()
# app.UntitledNotepad.Edit.type_keys("pywinauto Works!", with_spaces = True)

from pywinauto import Desktop, Application, mouse, findwindows
import pywinauto
import subprocess
import time
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.keyboard import send_keys
from pywinauto import backend
from pyuac import main_requires_admin

# @main_requires_admin
# def main():
#     print("Admin UAC enabled")
#
# if __name__ == "__main__":
#     main()

app = Application(backend='uia').start(r"C:\Program Files\thinkorswim\thinkorswim.exe")

time.sleep(15)

TOS_app=app.window(title="Logon to thinkorswim")

userid='PLitv001 /n'
password='Rtbd200{%}'

top_window = app.window(title_re="Logon to thinkorswim", visible_only=False)
wrp= TOS_app.wrapper_object()
wrp.click_input()
time.sleep(2)
wrp.type_keys(password)
time.sleep(2)
send_keys('{VK_RETURN}')
time.sleep(0.5)
send_keys('{VK_RETURN}')

time.sleep(15)

#menu select not working. Hotkey does. ^ symbol is hold control down. % is alt key. + is shift key.
send_keys('^4')


# The ThinkOrSwim app is like a webapplet. You can't select individual elements.

# time.sleep(1)
#
# TOS_app=app.window(title="Paper@thinkorswim *")
#
# pane = UIAWrapper(TOS_app.element_info)
# TOS_app.print_control_identifiers()

# send_keys('{VK_RETURN}')
# #TOS_app.menu_select("Scan")
# TOS_app.menu_select("Analyze")

# Going to click screen coordinates instead

#!!! Dont forget to filter out stocks that have earnings coming. It could just be a run up.
# On paper accounts, TD doesn't allow Studies filter that has ability to filter these out.
# I didn't want to have this work on the Live Account

# Scan button click
coordinate1 = 1890
coordinate2 = 300
pywinauto.mouse.move(coords=(coordinate1, coordinate2))
pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
time.sleep(1)

# dropdown button click
coordinate1 = 1896
coordinate2 = 63
pywinauto.mouse.move(coords=(coordinate1, coordinate2))
pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
time.sleep(1)

# dropdown "Export" button click
coordinate1 = 1896
coordinate2 = 234
pywinauto.mouse.move(coords=(coordinate1, coordinate2))
pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
time.sleep(1)

# dropdown "CSV" button click
coordinate1 = 1664
coordinate2 = 235
pywinauto.mouse.move(coords=(coordinate1, coordinate2))
pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
time.sleep(1)

# path where to save
time.sleep(2)
send_keys("D:\\Trash\\unusual_options_output.csv")
time.sleep(1)
send_keys('{VK_RETURN}')

# Close ToS
coordinate1 = 1897
coordinate2 = 16
pywinauto.mouse.move(coords=(coordinate1, coordinate2))
pywinauto.mouse.click(button='left', coords=(coordinate1, coordinate2))
time.sleep(1)
send_keys('{VK_RETURN}')





