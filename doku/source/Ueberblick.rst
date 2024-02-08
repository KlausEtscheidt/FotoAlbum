====================================
Überblick über die Software-Struktur
====================================

Ziel des Programms
==================

Ziel ist es aus Scans von Seiten eines Foto-Albums 
die einzelnen Fotos zu extrahieren.

Aufbau der GUI
==============

Die GUI besteht im Wesentlichen aus der von wx.Frame abgeleiteten Klasse :class:`mainframe.MainFrame`
und dem darin enthaltenen wx.Window, welches zur Anzeige der Bilder genutzt wird 
und als Eigenschaft **imagectrl** der Klasse gespeichert ist.

Der Ablauf des Programms wird hauptsächlich durch Maus- und Tastatur-Events, 
die von mainframe bzw imagectrl empfangen werden, gesteuert.

Die Event-Handler wurden in die Klasse :class:`mainframe_evts.EvtHandler` ausgelagert.

Programmstart
=============

Beim Start wird durch die :class:`fotoalbum.MyApp.OnInit`-Methode der abgeleiteten App-Klasse :class:`fotoalbum.MyApp` 
nach dem Anlegen der GUI die Methode :meth:`fotoalbum.MyApp.seiten_laden` aufgerufen.

Hier wird das Arbeitsverzeichnis festgelegt, dessen Tiff-Dateien eingelesen 
und die erste Datei (Seite des Albums) zur Bearbeitung angeboten.

Bestimmen des Arbeitsverzeichnis
--------------------------------

Beim Programmstart wird zunächst geprüft, ob es das zuletzt benutzte Verzeichnis noch gibt.
In diesem Fall wird dieses Verzeichnis zunächst als Arbeitsverzeichnis gesetzt.
Wenn nicht öffnet sich ein Dialog zur Verzeichnisauswahl.

Das Arbeitsverzeichnis kann per Drag and Drop oder **Menüauswahl ToDO noch programmieren** jederzeit geändert werden.

Die Definition des Arbeitsverzeichnis startet den Ablauf der Bearbeitung 
mit dem Einlesen der dort vorhandenen Scans neu.

Einlesen der Scans
------------------

Die Definition des Arbeitsverzeichnisses startet das Einlesen der Tiff-Dateien in diesem Verzeichnis.
Dies geschieht durch den Konstruktor der Klasse :class:`seiten.Seiten`, die von pyhon-list abgeleitet ist.
Dabei wird für jede Datei eine Instanz von :class:`seite.Seite` erzeugt und in Seiten abgelegt.
Für die neue Seite wird als Eigenschaft zunächst nur der Name der Tiff-Datei abgelegt.
Diese Daten werden im weiteren Verlauf durch eine Liste der auf der Seite enthaltenen Fotos *Seite.fotos* ergänzt.

Die erste eingelesene Seite wird angezeigt und dem Benutzer zur Bearbeitung angeboten.

Mit den Buttons **Todo Screenshot** kann jedoch die vorhergehende oder folgende Seite angezeigt werden.
Eine evtl.bereits begonnene Bearbeitung einer Seite wird dadurch abgebrochen und der Bearbeitungstatus
**ToDO Verwei auf Status** zurückgesetzt.

Bearbeitung einer Seite
=======================

Beim jedem Anzeigen der Seite kann diese bei Bedarf (falsch gescannt) 
mehrfach um 90° gedreht und dann in korrekter Drehlage gespeichert werden. **ToDO Tasten hierfür**

Die Bearbeitung einer Seite besteht dann aus der Defintion der Lage, der auf ihr enthaltenen Fotos.
Der Ablauf ist hierbei für jedes Foto gleich und wird so oft wie nötig wiederholt.

Die Bearbeitung einer Seite wird nie abgeschlossen. 
Sie kann aber jederzeit durch Wechseln auf eine andere Seite unterbrochen und später weiter geführt werden.
Eine Fotodefinition, die beim Verlassen der Seite unvollständig ist, wird komplett gelöscht.

Definition eines Fotos
-----------------------

Im ersten Schritt muss der Anwender einen Rahmen (im Folgenden Grobrahmen genannt) definieren,
der ein Foto auf der Seite grob umgibt. Er kann dabei größer als das Foto sein,
seine Ecken können aber auch ein wenig innerhalb des Fotos liegen.

Durch diesen Grobrahmen ist nun die ungefähre Lage des Fotos auf der Seite bekannt.
Nun werden nacheinander vergrößerte Ausschnitte der Umgebung der linken oberen (Ecke1), 
rechten oberen (Ecke2) und rechten unteren (Ecke3) des Grobrahmens angezeigt.
In diesen Vergrößerungen werden die Ecken des Fotos exakt definiert.
Mit Ecke1 ist der Nullpunkt des Fotos bekannt. Aus dem Vektor von Ecke1 zu Ecke2 werden 
die Drehlage und die Breite exakt bestimmt. Die Länge des Vektors von Ecke2 zu Ecke3 bestimmt die Höhe des Fotos.

Der Fortschritt bei der Definition eines Fotos wird in der property :class:`~.Seiten.status` der Klasse Seiten festgehalten.
Da zu einer Zeit immer nur ein Foto definiert wird, gilt dieser Status für die gesamte Anwendung
und nicht nur für ein Foto bzw eine Seite.

Der Status wird beim Wechsel auf eine neue Seite und nach dem Abschluss einer Foto-Definition auf 'Start Seite/Foto' gesetzt.
Mit diesem Status beginnt der Ablauf der Definition.

Wird bei diesem Status von :class:`mainframe_evts.EvtHandler` ein Mausklick oder das Drücken der Leertaste entdeckt,
wird die aktuelle Mausposition gespeichert. 

Mit diesem Punkt wird außerdem mittels :meth:`seite.Seite.neues_foto_anlegen`
eine neue Instanz der Klasse :class:`fotos.Foto` angelegt.
Der Punkt definiert die linke obere Ecke des Grob-Rahmens.
Der Status wird auf 'Rahmen ru' gesetzt, weil als nächstes die Angabe der rechten unteren Ecke des Rahmens erwartet wird.

In diesem Status wird bei Mausbewegungen ein rotes Rechteck von der gespeicherten zur aktuellen Mausposition gezeichnet.
Beim nächsten Mausklick wird der gewählte Punkt mit :meth:`foto.Foto.setze_rahmen_ecke_ru` 
als Eigenschaft der Foto-Instanz gespeichert.
Der Status wird auf 'Ecke1' gesetzt.
Mittels :meth:`mainframe.MainFrame.zeige_ecke` wird die Umgebung der linken oberen Ecke des Gron´brahmens angezeigt.

Beim nächsten Mausklick wird die Mausposition als Eigenschaft :attr:`fotos.Foto.ecke1` der aktuellen Fotoinstanz abgelegt.
Der Status wird auf 'Ecke2' gesetzt und der Ablauf wiederholt sich für Ecke2 und Ecke3.
Alle Positionen werden vor dem Abspeichern von Bildschirm- bzw Mauskoordinaten in die Bitmapkoordinaten
des angezeigten Scans umgerechnet.



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