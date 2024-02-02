import tomlkit.toml_file
import tomlkit.toml_document
import tomlkit.items
import os


def einlesen(seitenliste, pfad):
    tomlfilename = os.path.join(pfad, "ergebnis.toml")
    # toml_document lesen
    tml = tomlkit.toml_file.TOMLFile(tomlfilename).read()
    for seite in tml['seite']:
        print(seite['pfad'])
        if 'foto' in seite:
            for foto in seite['foto']:
                print(foto['pfad'])
                pass

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