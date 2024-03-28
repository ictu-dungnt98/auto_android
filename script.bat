set "dataFile=device_id.txt"

set "list="

for /f "usebackq delims=" %%i in ("%dataFile%") do (
    REM Append each line to the list variable
    adb -s "%%i" shell screencap "/sdcard/%%i.png"
    adb -s "%%i" pull /sdcard/%%i.png
)

@REM adb -s %1 shell screencap /sdcard/%1.png
@REM adb -s %1 pull /sdcard/%1.png