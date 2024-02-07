$pyfiles =  Get-ChildItem -Filter *.py
Set-Location $PSScriptRoot

$myargs = $pyfiles
$myargs += "--extension-pkg-whitelist=wx"
#$myargs += "--msg-template=`"{path}:{line}:{column}: {msg_id}: ({symbol}) {msg}`""
# $myargs += "--init-hook=`"import sys; sys.path=[r'" + C:\Users\Klaus\Documents\_m\FotoAlbum + "']+sys.path`" "
$myargs += "--init-hook=`"import sys; sys.path=[r'" + $PSScriptRoot + "']+sys.path`" "
Start-Process -FilePath "pylint" -ArgumentList $myargs -Wait -NoNewWindow
