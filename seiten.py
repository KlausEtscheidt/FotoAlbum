import logging
import glob

import wx

from config import conf
from seite import Seite

logger = logging.getLogger('album')


class Seiten(list):

    seiten_nr = 0

    def __init__(self, imagepanel):
        # imagepanel ist Instanz von ImagePanel (Kind v ImagePanelOuter) aus panel_imageview
        # Klassenvar in Seite setzen
        Seite.imagepanel = imagepanel
        # imagepanel und imagepanel.imagectrl als Eigenschaft
        self.imagepanel = imagepanel
        self.imagectrl = imagepanel.imagectrl
        # Rueckverweis Seiten <-> imagepanel
        imagepanel.seiten = self
        
        self.myFileList = []
        self.seitenliste_erstellen()

        self.__status = 'Start Seite/Foto'
        self.__seiten_nr = -1
        # self.__seiten = None
        self.__seite = None

        self.__rahmen_lo = (0, 0)
        self.__rahmen_ru = (0, 0)
    
    @property
    def akt_seite(self):
        return self.__seite
    
    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, x):
        self.__status = x

    @property
    def rahmen_lo(self):
        return self.__rahmen_lo

    @rahmen_lo.setter
    def rahmen_lo(self, x):
        self.__rahmen_lo = x
        self.__status = 'Rahmen ru'

    @property
    def rahmen_ru(self):
        return self.__rahmen_ru

    @rahmen_ru.setter
    def rahmen_ru(self, x):
        self.__rahmen_ru = x

    ############################################################################
    #
    # Aktionen übergeordnet
    #
    ############################################################################

    def seitenliste_erstellen(self):
        # Filenamen der Seiten-Tiffs einlesen
        # Seiten erzeugen (ohne image) und in Liste merken

        # Suche Bilder    
        self.myFileList = glob.glob(conf.pic_path + "\*" + conf.pic_type)
        
        # Fuer jeden gefundenen Pfad, Seitenobjekt erzeugen und merken
        for fullpath in self.myFileList:
            seite = Seite(fullpath)
            self.append(seite)
        
        msg = f'Liste mit {len(self):d} Bildern geladen.'
        if conf.mainframe:
            conf.mainframe.SetStatusText(msg)
        logger.debug(msg + f'\nVerzeichnis: {conf.pic_path} Endung: {conf.pic_type}\n')        

        # self.__seiten = Seiten()
    
    def foto_neu_beschneiden(self, pfad_zum_foto):
        # 
        for i in range(len(self)):
            seite = self[i]            
            for foto in seite.fotos:
                if pfad_zum_foto == foto.saved_in:
                    # Seite anzeigen
                    self.seite_bearbeiten(i)
                    # Zustand nach foto_drehen herstellen
                    seite.akt_foto = foto
                    self.__status = 'Foto Kontrolle'
                    self.__seite.foto_drehen()
                    # self.foto_beschneiden(foto.rahmen_plus)
                    # self.bild_gedreht = neu_image.crop(p1, p2)

    ############################################################################
    #
    # Aktionen je Seite
    #
    ############################################################################

    def seite_bearbeiten(self, seiten_nr):
        """seite_bearbeiten Seite eines Fotoalbums bearbeiten

        Fragt vom Benutzer die Daten (Ecken) aller Fotos auf der Seite ab
        und speichert die Fotos als tiff-Datei.
        Durch die Anzeige des Original-Bilds wird für dieses ein Image erzeugt.
        Es sollte beim Verlassen der Seite freigegeben werden.

        :param seiten_nr: index der zu bearbeitenden Seite in self.__seiten
        :type seiten_nr: int
        """

        self.imagectrl.SetFocus()
        self.__seiten_nr = seiten_nr # merken f next
        # Status auf Anfang Seite bearbeiten
        self.__status = 'Start Seite/Foto'
        # Seite als aktiv merken
        self.__seite = self[seiten_nr]
        # Anzeigen
        txt = f'{self.__seite.basename}{self.__seite.typ}   ({seiten_nr+1:d} von {len(self)})'
        self.imagepanel.parent.label_li.SetLabel(txt)
        self.imagepanel.parent.label_re.SetLabel(f'{self.__status}')
        self.__seite.seite_laden()

    def seite_bearbeiten_next(self):
        # Speicher freigeben
        if self.__seiten_nr < len(self)-1:
            self.__seiten_nr += 1
        else:
            self.__seiten_nr = 0
        self.seite_bearbeiten(self.__seiten_nr)

    def seite_bearbeiten_prev(self):
        # Speicher freigeben
        if self.__seiten_nr > 0:
            self.__seiten_nr -= 1
        else:
            self.__seiten_nr = len(self)-1
        self.seite_bearbeiten(self.__seiten_nr)


    ############################################################################
    #
    # Aktionen je Foto
    #
    ############################################################################

    # 1. Aktion je Foto:
    # Foto anhand Rahmen erzeugen und ablegen
    def foto_rahmen_ablegen(self):
        self.__seite.foto_dazu(self.rahmen_lo, self.rahmen_ru)
        # Weiter mit exakter Eckendefinition
        self.__status = 'Ecke1'
        self.imagepanel.parent.label_re.SetLabel(f'   {self.__status}')
        self.__seite.zeige_ecke1()

    # 2. Aktion je Foto:
    # Ecke 1 abspeichern und Ecke 2 anzeigen
    def ecke1(self, p):
        self.__seite.speichere_ecke1(p)
        self.__status = 'Ecke2'
        self.imagepanel.parent.label_re.SetLabel(f'   {self.__status}')
        self.__seite.zeige_ecke2()

    # 3. Aktion je Foto:
    # Ecke 2 abspeichern und Ecke 3 anzeigen
    def ecke2(self, p):
        self.__seite.speichere_ecke2(p)
        self.__status = 'Ecke3'
        self.imagepanel.parent.label_re.SetLabel(f'   {self.__status}')
        self.__seite.zeige_ecke3()

    # 3. Aktion je Foto:
    # Ecke 3 abspeichern und beschnittenes Foto anzeigen
    def ecke3(self, p):
        self.__seite.speichere_ecke3(p)
        self.__status = 'Foto Kontrolle'
        # self.imagepanel.parent.label_re.SetLabel(f' {self.__status}')
        akt_foto = self.__seite.akt_foto
        self.imagepanel.parent.label_re.SetLabel(f'   {self.__status} Rahmen: {akt_foto.rahmen_plus}')    
        self.__seite.foto_drehen()

    # 4. Aktion je Foto:
    # Beschnitt ändern
    def foto_beschneiden(self, plusminus):
        self.__seite.foto_beschneiden(plusminus)
        akt_foto = self.__seite.akt_foto
        self.imagepanel.parent.label_re.SetLabel(f'   {self.__status} Rahmen: {akt_foto.rahmen_plus}')    


    # 5. Aktion je Foto:
    # Beschnittenes Foto speichern und n. Seite bearbeiten
    def foto_speichern(self, p):
        self.__seite.foto_speichern()
        self.__status = 'Foto fertig'
        self.seite_bearbeiten(self.__seiten_nr)

    def reset(self):
        """reset Bearbeitung abbrechen

        Status auf Start Seite/Foto setzen
        Fragmente der Eingabe loeschen
        """        
        akt_seite = self[self.__seiten_nr]
        akt_foto = akt_seite.akt_foto
        # akt_foto wird beim Klicken des Rahmens l.o gesetzt
        if akt_foto:
            # loeschen wenn noch nicht fertig definiert
            if not akt_foto.fertig:
                akt_seite.fotos.remove(akt_foto)
                akt_seite.akt_foto = None
        #Status reset und weiter
        self.seite_bearbeiten(self.__seiten_nr)

    def foto_entfernen(self, mauspos):
        akt_seite = self[self.__seiten_nr]
        for foto in akt_seite.fotos:
            if foto.pos_ist_innen(mauspos.x, mauspos.y):
                akt_seite.fotos.remove(foto)
                break
        self.seite_bearbeiten(self.__seiten_nr)

