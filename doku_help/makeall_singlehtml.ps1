#$projekt aus build/htmlhelp ermitteln: Name der xxx.hhp-Datei $projekt=xxx
$projekt = "FotoAlbumHilfe"

Set-Location $PSScriptRoot #cd

# sphinx-build starten
# Aufruf syntax: sphinx-build [options] <sourcedir> <outputdir>
$cmd = "sphinx-build"
#Erzeuge htmlhelp aus Dateien im Verzeichnis 'source' Output ins Verz. 'build'
# $builder = 'htmlhelp'
$builder = 'singlehtml'
$sourcedir = 'source'
$outputdir = 'build'
$myargs = @('-M', $builder, $sourcedir, $outputdir)
# $myargs += '-E' # immer alle neu
Start-Process -FilePath $cmd $myargs  -Wait -NoNewWindow

# Html anzeigen

$cmd = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$url = "$PSScriptRoot/build/singlehtml/index.html"
Start-Process -FilePath $cmd $url