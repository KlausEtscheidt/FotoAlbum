import tomlkit.toml_file
import tomlkit.toml_document
import tomlkit.items
import os

import wx

from fotos import Foto

def einlesen(seitenliste, pfad):
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
            for pyseite in seitenliste:
                if pyseite.fullpath2pic == seite['pfad'] :
                    found = True
                    break

            # Nur wenn die Seite in der aktuellen seitenliste noch existiert
            if found:
                for foto in seite['foto']:
                    print(foto['pfad'])
                    # Foto-Objekt erzeugen und zur Seite dazu
                    pyseite.foto_dazu( None, None)
                    # Eigenschaften setzen
                    pyfoto = pyseite.akt_foto
                    pyfoto.ecke1 = wx.Point(foto['x1'], foto['y1'])
                    pyfoto.ecke2 = wx.Point(foto['x2'], foto['y2'])
                    pyfoto.ecke3 = wx.Point(foto['x3'], foto['y3'])
                    # pyfoto.ecke1.y = foto['y1']
                    # pyfoto.ecke2.x = foto['x2']
                    # pyfoto.ecke2.y = foto['y2']
                    # pyfoto.ecke3.x = foto['x3']
                    # pyfoto.ecke3.y = foto['y3']
                    pyfoto.rahmen_plus = foto['rahmen_plus']
                    pyfoto.saved_in = foto['pfad']
                    pyfoto.fertig = True


def ausgeben(seitenliste, pfad):
    
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
        
        for i in range(0, len(pyseite.fotos)):

            pyfoto = pyseite.fotos[i]

            #neue toml Tabelle
            foto = tomlkit.table()
            #neuer Eintrag in foto Aot
            fotos.append(foto)
            
            # Daten des Fotos
            foto.add('nr', i)
            foto.add('pfad', pyfoto.saved_in)
            foto.add('x1', pyfoto.ecke1.x)
            foto.add('y1', pyfoto.ecke1.y)
            foto.add('x2', pyfoto.ecke2.x)
            foto.add('y2', pyfoto.ecke2.y)
            foto.add('x3', pyfoto.ecke3.x)
            foto.add('y3', pyfoto.ecke3.y)
            foto.add('rahmen_plus', pyfoto.rahmen_plus)

    # toml_document schreiben
    tmlfile = tomlkit.toml_file.TOMLFile(tomlfilename).write(tml)

# ausgeben()
# einlesen()
pass