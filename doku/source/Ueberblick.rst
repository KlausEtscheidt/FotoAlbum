====================================
Überblick über die Software-Struktur
====================================

Ziel des Programms
==================

Ziel ist es aus Scans von Seiten eines Foto-Albums 
die einzelnen Fotos zu extrahieren.

Ablauf
======

Per Drag and Drop oder Menüauswahl wird ein Verzeichnis definiert,
welches Scans im Tiff-Format enthält.

Alle Dateinamen werden in einer Liste abgelegt (Modul Seiten)
und für jedes Tiff wird ein Objekt der Klasse Seite angelegt.

Das erste Tiff (erste Seite) wird angezeigt, über Buttons kann 
auf die nächste oder vorhergehende Seite positioniert werden.

Per Mausklick wird ein Rahmen aufgezogen, der ein Foto grob umgibt.

Mit dieser Info werden jetzt nacheinander die Umgebungen 
der linken oberen, der rechten oberen und der rechten unteren Ecke
dieses Rahmen vergrößert angezeigt.

Per Mausklick definiert der Benutzer die exakte Lage der jeweiligen Foto-Ecke.

Hieraus ergibt sich die exakte Lage eines Fotos.

Das Foto wird noch mal angezeigt und der Anwender kann den Beschnitt noch mal verkleinern
oder vergrößern.

Abschließend werden ein Kontrollbild als (jpg) und das beschnittene Foto als Tiff gespeichert.
Das Kontrollbild zeigt auch etwas von der Umgebung des beschnittenes Fotos 
und den eingezeichneten Beschnitt-Rahmen.

Die ermittelten Daten können als Toml-Dateien gespeichert uns aus diesem gelesen werden.

Software-Struktur
=================

Das Hauptprogramm liegt in FotoAlbum.pyw