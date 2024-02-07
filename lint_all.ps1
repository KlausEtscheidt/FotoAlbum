$pyfiles =  Get-ChildItem -Filter *.py
Set-Location $PSScriptRoot
# foreach ($pyfile in $pyfiles) {
#     'linte ' + $pyfile.Name
#     Start-Process pylint $pyfile -Wait #-NoNewWindowli  
# }
# $names = ''
# foreach ($pyfile in $pyfiles) {
#     $names = $names + ' ' + $pyfile.Name
# }
# Start-Process pylint $names --output="lint.txt" --extension-pkg-whitelist=wx --output-format=parseable --init-hook="sys.path=[r'C:\Users\Etscheidt\Documents\pyth\FotoAlbum']+sys.path" -Wait -NoNewWindow

$myargs = $pyfiles
# $myargs += "--output=`"lint.txt`""
$myargs += "--extension-pkg-whitelist=wx"
# $myargs += "--output-format=json:lint.txt,colorized"
# $myargs += "--output-format=json:lint.txt,parseable"
$myargs += "--msg-template=`"{path}:{line}:{column}: {msg_id}: ({symbol}) {msg}`""
# $myargs += "--msg-template=`"{path}:{line}:{column}: {msg_id}: {symbol}`""
$myargs += "--init-hook=`"sys.path=[r'C:\Users\Etscheidt\Documents\pyth\FotoAlbum']+sys.path`" "
Start-Process -FilePath "pylint" -ArgumentList $myargs -Wait -NoNewWindow
#--output="lint.txt" --extension-pkg-whitelist=wx --output-format=parseable --init-hook="sys.path=[r'C:\Users\Etscheidt\Documents\pyth\FotoAlbum']+sys.path" -Wait -NoNewWindow

# Start-Process pylint $names --output="lint.txt" --extension-pkg-whitelist=wx -Wait #-NoNewWindow
# Start-Process -FilePath $cmd  $projekt -Wait #-NoNewWindow