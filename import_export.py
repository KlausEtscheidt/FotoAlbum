'''
import_export.py
-------------------

Definierte Fotos im Toml-Format speichern oder einlesen.
'''
import os

import tomlkit.toml_file
import tomlkit.toml_document
import tomlkit.items

import wx

def einlesen(seitenliste, pfad):
    '''Liest bereits definierte Fotos aus Toml-Datei und erzeugt Foto-Instanzen

    Die Funktion endet, wenn im Verzeichnis **pfad** keine Toml-Datei namens "ergebnis.toml" liegt.
    Wenn es für eine in Toml vorhandene Seite, dort auch Fotodefinitoinen gibt,
    wird zu dieser Toml-Seite die zugehörige Seite in der **seitenliste** gesucht.
    Hierzu müssen die Pfade zur Tiff-Datei in Toml und seitenliste gleich sein.
    Bei Übereinstimmung wird für jedes Toml-Foto ein Foto auf der zugehörigen Seite angelegt.
    Die Daten für diese Foto-Instanzen werden aus den Toml-Daten übernommen.
    Die Eigenschaft **saved_in** wird für das Auffinden eines per Drag'n-Drop übergebenen Fotos
    in der Datenstruktur Seiten->Seite.fotos->Foto gebraucht.

    Args:
        seitenliste (Seiten): Liste der Seitenobjekte für die Tiffs existieren.
        pfad (str): Verzeichnis, aus dem die Tiffs eingelesen wurden.
    '''
    tomlfilename = os.path.join(pfad, "ergebnis.toml")
    if not os.path.isfile(tomlfilename):
        #keine Datei gefunden
        return

    # toml_document lesen
    tml = tomlkit.toml_file.TOMLFile(tomlfilename).read()
    for seite in tml['seite']:
        print(seite['pfad'])
        if 'foto' in seite:

            # Es gibt schon Fotosdefinitionen für diese Seite
            # Zum Übertragen Seite in seitenliste suchen
            found = False
            pyseite = None
            for pyseite in seitenliste:
                if pyseite.fullpath2pic == seite['pfad'] :
                    found = True
                    break

            # Nur wenn die Seite in der aktuellen seitenliste noch existiert
            if found:
                for foto in seite['foto']:
                    print(foto['pfad'])
                    # Foto-Objekt erzeugen und zur Seite dazu
                    pyseite.neues_foto_anlegen( None)
                    # Eigenschaften setzen
                    pyfoto = pyseite.akt_foto
                    pyfoto.ecke1 = wx.Point(foto['x1'], foto['y1'])
                    pyfoto.ecke2 = wx.Point(foto['x2'], foto['y2'])
                    pyfoto.ecke3 = wx.Point(foto['x3'], foto['y3'])
                    # Die ursprünglichen Koordinaten des Grobauswahl-Rahmens
                    # wurden nicht in Toml gespeichert
                    # Wir nehmen stattdessen Ecke 1 und Ecke 3
                    pyfoto.p1 = pyfoto.ecke1
                    pyfoto.p2 = pyfoto.ecke3
                    pyfoto.rahmen_plus = foto['rahmen_plus']
                    pyfoto.saved_in = foto['pfad']
                    pyfoto.fertig = True


def ausgeben(seitenliste, pfad):
    '''Speichert die Datenstruktur Seiten->Seite.fotos->Foto im Toml-Format.

    Args:
        seitenliste (Seiten): Liste der Seitenobjekte.
        pfad (str): Verzeichnis, in dem die Toml-Datei "ergebnis.toml" gespeichert wird.
    '''

    tomlfilename = os.path.join(pfad, "ergebnis.toml")
    tml = tomlkit.toml_document.TOMLDocument()
    tml["title"] = "Seitenliste"

    seiten = tomlkit.aot()
    tml.add('seite', seiten)

    for pyseite in seitenliste:
        # neue toml Tabelle
        seite = tomlkit.table()
        #neuer Eintrag in AoT
        seiten.append(seite)
        seite.add(tomlkit.comment("------------------------------------------"))
        seite.add('pfad', pyseite.fullpath2pic)

        #neue toml Aot zur seite dazu
        fotos = tomlkit.aot()
        seite.add('foto',fotos)

        foto_nr = 0
        for pyfoto in pyseite.fotos:

            #neue toml Tabelle
            foto = tomlkit.table()
            #neuer Eintrag in foto Aot
            fotos.append(foto)

            # Daten des Fotos
            foto_nr += 1
            foto.add('nr', foto_nr)
            foto.add('pfad', pyfoto.saved_in)
            foto.add('x1', pyfoto.ecke1.x)
            foto.add('y1', pyfoto.ecke1.y)
            foto.add('x2', pyfoto.ecke2.x)
            foto.add('y2', pyfoto.ecke2.y)
            foto.add('x3', pyfoto.ecke3.x)
            foto.add('y3', pyfoto.ecke3.y)
            foto.add('rahmen_plus', pyfoto.rahmen_plus)

    # toml_document schreiben
    tomlkit.toml_file.TOMLFile(tomlfilename).write(tml)

if __name__ == '__main__':
    help(einlesen)
