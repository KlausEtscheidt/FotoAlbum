Zweck
------

Dient zum Extrahieren einzelner Fotos aus Scan's kompletter Seiten eines Foto-Albums.

Der Ablauf wird vom Programm vorgegeben.

Gesamtablauf
-------------
Zuerst wird ein Verzeichnis mit tif-dateien des Scans eingelesen.

Die erste Seite (Datei) wird angezeigt.

Es folgt die Definition der Lage eines oder mehrere Fotos.

Die Seite kann durch Klick auf einen Button gewechselt werden.
Dies kann erfolgen, wenn alle Fotos definiert wurden, aber auch vorher.
Die Defition der Fotos bleibt beim Wechsel erhalten 
und wird durch rote, durchkreuzte Rahmen auf der Seite markiert.

Fotodefinition
---------------

Durch den ersten Klick ins Bild wird die linke obere Ecke eines Rahmens definiert.
Der zweite Klick definiert die rechte untere Ecke.
Dieser Rahmen muss das zu extrahierende Foto grob umgeben.

Anstatt einem Klick mit der linken Maustaste kann auch die Leertaste gedrückt werden.
Die Mausposition kann mit den Pfeil-Tasten geändert werden.

Der Rahmen dient zur Grobdefinition der Lage des Fotos auf der Seite.
Es wird ein vergrößerter Ausschnitt der Seite gezeigt, 
der die linke oberen Ecke des Rahmens umgibt.

In diesem Ausschnitt wird die linke obere Ecke des Fotos per Mausklick exakt definiert.

Analog wird die rechte obere Ecke des Fotos angewählt.
Aus diesen beiden Ecken ergeben sich der Nullpunkt (links oben),
die Drehlage und die Breite (Abstand beider Ecken) des Fotos.

Die dritte Ecke, rechts unten, wird ebenso definiert.
Aus dem Abstand zwischen zweiter und dritter Ecke wird die Höhe des Fotos berechnet.

Mit diesen Informationen kann das Foto aus der Seite ausgeschnitten werden.
Falls das Foto auf der Seite verdreht lag, kann diese Drehung korrigiert werden.

Dieser korrigierte Bildausschnitt wird mit einem umgebenden Rand dargestellt.
Es wird ein rotes Rechteck angezeigt, welches durch Ecke 1 geht 
und die ermittelte Breite und Höhe hat.
Der Anwender kann dieses Rechteck verkleinern oder vergrößern (Strg-'+' oder Strd-'-')
und so eine letzte Korrektur des Bildausschnitts vornehmen.

Durch Mausklick oder Leertaste wird diese Korrektur abgeschlossen
und das so definierte Foto wird in einem eigenen Tiff im Unterverzeichnis *zerlegt* gespeichert.

Weiterhin wird ein Kontrollbild als JPG gespeichert. 
Dieses enthält einen etwas größeren Ausschnitt und den finalen roten Rahmen,
der das Tiff defineirt.

Der gesamte Ablauf kann durch drücken von 'ESC' abgebrochen werden.
Das Programm erwartet dann eine neue Definiton eines Fotos.
Alternativ kann der Anwender die Seite wechseln.

Foto löschen
--------------

Die definierten Fotos werden auf den Seiten durch Rahmen mit diagonalen Linien markiert.
Durch Drücken der Taste 'e' (entfernen) wird die Definition des Fotos, 
in dem der Cursor steht, gelöscht. Evtl bereits exportierte Fotos bleiben erhalten.
Das Foto kann neu definiert und neu exportiert werden.

.. tastenbelegung:

Tastenbelegung
---------------

.. _ohne-strg:

ohne Strg:
...........

num +: zoomt das Bild um Faktor 2
num -: zoomt das Bild um Faktor 0.5

Pfeiltasten: verschieben den Cursor

e: entfernt eine Definition eines Fotos von einer Seite

ESC: Bricht die Definition eines Fotos ab

Leer-Taste: wie Mausklick (geht auf nächsten Bearbeitungsschritt mit akt Cursorposition)

.. _mit-strg:

mit Strg:
...........

num +: vergrößert den Rahmen zur Definition eines Fotos um 5 Pixel
num -: verkleinert den Rahmen zur Definition eines Fotos um 5 Pixel

Pfeiltasten: verschieben das Bild
