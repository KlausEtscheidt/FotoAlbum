SET projekt=%1
echo make %projekt%
call make htmlhelp
echo compile
rem Name albumzerlegendoc entsteht aus conf.py project = 'Album zerlegen' durch anhängen von doc
rem Korrekten Namen "xxx.hhp" im build-Verzeichnis htmlhelp ermitteln 
rem aus make htmlhelp entsteht Album_Zerlegendoc.hhp als Eingabe für hhc.exe
@REM "C:\Program Files (x86)\HTML Help Workshop\hhc.exe" build\htmlhelp\albumzerlegendoc.hhp
"C:\Program Files (x86)\HTML Help Workshop\hhc.exe" build\htmlhelp\%projekt%.hhp
echo moving
rem hhc.exe erzeugt albumzerlegendoc.chm
copy /Y build\htmlhelp\%projekt%.chm .
rem move /Y build\htmlhelp\albumzerlegendoc.chm ..\..\Hilfe
pause