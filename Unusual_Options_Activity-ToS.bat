SET logfile="D:\Dropbox\Toolkit\Python\Unusual_Options_Activity-ToS\batch.log"
@echo off
@echo Starting Script at %date% %time% >> %logfile%
"D:\Dropbox\Toolkit\Python\Unusual_Options_Activity-ToS\venv\Scripts\python.exe" "D:\Dropbox\Toolkit\Python\Unusual_Options_Activity-ToS\main.py"
@echo finished at %date% %time% >> %logfile%