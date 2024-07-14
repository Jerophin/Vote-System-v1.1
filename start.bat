@echo off
set script="block chain.py"
set python_exe="C:\Users\Jerop\AppData\Local\Microsoft\WindowsApps\python.exe"
set vbs_file="%temp%\getadmin.vbs"

echo Set UAC = CreateObject^("Shell.Application"^) > %vbs_file%
echo UAC.ShellExecute %python_exe%, %script%, "", "runas", 1 >> %vbs_file%
cscript //nologo %vbs_file%
del %vbs_file%
