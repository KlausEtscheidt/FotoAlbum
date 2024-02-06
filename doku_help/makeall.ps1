#$projekt aus build/htmlhelp ermitteln: Name der xxx.hhp-Datei $projekt=xxx
$projekt = "fotoalbumhilfedoc"
Set-Location $PSScriptRoot
$cmd = $PSScriptRoot + "\MakeHelp.bat"
Start-Process -FilePath $cmd  $projekt -Wait #-NoNewWindow
Start-Process ".\$projekt.chm" -Wait #-NoNewWindow