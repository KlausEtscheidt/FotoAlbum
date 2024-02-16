#$projekt aus build/htmlhelp ermitteln: Name der xxx.hhp-Datei $projekt=xxx
$projekt = "FotoAlbumHilfe"
$window_title = "FotoAlbumHilfe 1.0 Dokumentation"

Set-Location $PSScriptRoot #cd

# sphinx-build starten
# Aufruf syntax: sphinx-build [options] <sourcedir> <outputdir>
$cmd = "sphinx-build"
#Erzeuge htmlhelp aus Dateien im Verzeichnis 'source' Output ins Verz. 'build'
$builder = 'htmlhelp'
# $builder = 'singlehtml'
$sourcedir = 'source'
$outputdir = 'build'
$myargs = @('-M', $builder, $sourcedir, $outputdir)
# $myargs += '-E' # immer alle neu
Start-Process -FilePath $cmd $myargs  -Wait -NoNewWindow

# hilfe compilieren
# @REM "C:\Program Files (x86)\HTML Help Workshop\hhc.exe" build\htmlhelp\albumzerlegendoc.hhp
$cmd = "C:\Program Files (x86)\HTML Help Workshop\hhc.exe"
$hh_path = "build\htmlhelp\" + $projekt + ".hhp" # Eingabe für hhc
$chm_path = "build\htmlhelp\" + $projekt + ".chm" # WIrd von hhc erzeugt
Start-Process -FilePath $cmd $hh_path -Wait -NoNewWindow

# Evtl laufende hh.exe killen
# Hole alle Prozesse
$Prozesse = Get-Process -ErrorAction Stop
# Filter über Fenster-Titel
$hh_Prozess = $Prozesse | Where-Object {$_.MainWindowTitle -eq $window_title}
# Wenn gefunden killen (geht auch wenn mehrfach offen, also $hh_Id.count > 1 )
if ($hh_Prozess.count -gt 0) {
    $hh_Id = $hh_Prozess.Id
    Stop-Process -Id $hh_Id
    # Wait-Process -Id $hh_Id
}

# Warte bis alle Prozesse gekilled (Wait-Process funktioniert anscheinend nicht immer)
$msg = '.'
while ($hh_Prozess.count -gt 0) {
    $Prozesse = Get-Process -ErrorAction Stop
    $hh_Prozess = $Prozesse | Where-Object {$_.MainWindowTitle -eq $window_title}
    Write-Host $msg
    $msg += '.'
}

# chm verschieben
Move-Item -Path $chm_path -Destination '.' -Force

# chm anzeigen
Start-Process ".\$projekt.chm" -Wait #-NoNewWindow