"""
seiten.py
=====================================================
Speichert alle Seiten.
Dient zur Steuerung des Ablaufs (Div. Funktionen werden von den Evt-Handlern gerufen)
"""

import logging
import glob

import wx

from config import conf
from seite import Seite

logger = logging.getLogger('album')


class Seiten(list):
    '''Liste aller Seiten eines Fotoalbums (Tiff-Dateien)

    Nimmt alle Seiten auf und wird von Events gesteuert

    Attributes:
        seiten_nr (int): Index der aktuell bearbeiteten Seite
    '''    

    seiten_nr = 0

    def __init__(self, parent):
        '''Durchsucht Verzeichnis nach tif-Dateien und erzeugt eine Seite je Tiff

        Args:
            imagepanel (ImagePanel): widget zur Darstellung einer Seite (Bitmap)
        '''
        self.parent = parent
        self.imagectrl = parent.imagectrl

        # Klassenvar in Seite setzen
        # imagepanel ist self.mainframe.imagepanel.innerpanel
        Seite.mainframe = parent
        # imagepanel und imagepanel.imagectrl als Eigenschaft
        # Rueckverweis Seiten <-> imagepanel
        #---------------- imagepanel.seiten = self
        
        self.myFileList = []
        self.seitenliste_erstellen()

        #: Kontrolliert den Ablauf
        self.__status = 'Start Seite/Foto'
        
        self.__seiten_nr = -1
        '''Index der aktuell bearbeiteten Seite'''
        self.__seite = None
        '''aktuell bearbeitete Seite'''

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
    
    def foto_neu_beschneiden(self, pfad_zum_foto=None, mauspos=None):

        foto_zum_schneiden = None

        # Wenn mit mauspos aufgerufen
        if mauspos:
            seiten_nr = self.__seiten_nr
            akt_seite = self[seiten_nr]
            #Suche ein Foto, das die geklickte Pos umgibt
            for foto in akt_seite.fotos:
                if foto.pos_ist_innen(mauspos.x, mauspos.y):
                    foto_zum_schneiden = foto
                    break
                
        # Wenn mit Pfad aufgerufen
        if pfad_zum_foto:
            for seiten_nr in range(len(self)):
                self.__seite = self[seiten_nr]
                for foto in self.__seite.fotos:
                    if pfad_zum_foto == foto.saved_in:
                        foto_zum_schneiden = foto
                        break
                if foto_zum_schneiden:
                    break

        if foto_zum_schneiden:
            # Seite anzeigen
            self.seite_bearbeiten(seiten_nr)
            # Zustand nach foto_drehen herstellen
            self.__seite.akt_foto = foto_zum_schneiden
            self.__status = 'Foto Kontrolle'
            self.__seite.foto_drehen()

    def alle_speichern(self):
        for seite in self:
            for foto in seite.fotos:
                seite.seite_laden()
                seite.akt_foto = foto
                seite.foto_drehen()
                seite.foto_speichern()
    ############################################################################
    #
    # Aktionen je Seite
    #
    ############################################################################

    def seite_bearbeiten(self, seiten_nr):
        """Seite eines Fotoalbums bearbeiten.

        Fragt vom Benutzer die Daten (Ecken) aller Fotos auf der Seite ab
        und speichert die Fotos als tiff-Datei.

        :param seiten_nr: index der zu bearbeitenden Seite in self.__seiten
        :type seiten_nr: int
        """
        conf.mainframe.SetStatusText('Foto definieren')

        self.imagectrl.SetFocus()
        self.__seiten_nr = seiten_nr # merken f next
        # Status auf Anfang Seite bearbeiten
        self.__status = 'Start Seite/Foto'
        # Seite als aktiv merken
        self.__seite = self[seiten_nr]
        # Anzeigen
        txt = f'{self.__seite.basename}{self.__seite.typ}   ({seiten_nr+1:d} von {len(self)})'
        # self.parent.label_li.SetLabel(txt)
        # self.parent.label_re.SetLabel(f'{self.__status}')
        self.__seite.seite_laden()

    def seite_bearbeiten_next(self):
        if self.__seiten_nr < len(self)-1:
            self.__seiten_nr += 1
        else:
            self.__seiten_nr = 0
        self.seite_bearbeiten(self.__seiten_nr)

    def seite_bearbeiten_prev(self):
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

    def foto_rahmen_ablegen(self):
        '''1. Aktion je Foto

        Foto-Objekt anhand des vom Benutzer aufgezogenen Rahmens erzeugen
        und im Seiten-Objekt ablegen.
        Umfeld der linken oberen Ecke des Rahmens (Ecke1) vergrößert anzeigen.
        Status auf "Ecke1" setzen
        '''
        self.__seite.foto_dazu(self.rahmen_lo, self.rahmen_ru)
        # Weiter mit exakter Eckendefinition
        self.__status = 'Ecke1'
        # self.imagepanel.parent.label_re.SetLabel(f'   {self.__status}')
        self.__seite.zeige_ecke1()

    def ecke1(self, p):
        '''2. Aktion je Foto: Ecke 1 abspeichern und Ecke 2 anzeigen.

        Ecke 1 im Seiten-Objekt ablegen.
        Umfeld der rechten oberen Ecke des Rahmens (Ecke2) vergrößert anzeigen.
        Status auf "Ecke2" setzen
        '''
        self.__seite.speichere_ecke1(p)
        self.__status = 'Ecke2'
        # self.imagepanel.parent.label_re.SetLabel(f'   {self.__status}')
        self.__seite.zeige_ecke2()

    def ecke2(self, p):
        '''3. Aktion je Foto: Ecke 2 abspeichern und Ecke 3 anzeigen.

        Status auf "Ecke3" setzen
        '''
        self.__seite.speichere_ecke2(p)
        self.__status = 'Ecke3'
        # self.imagepanel.parent.label_re.SetLabel(f'   {self.__status}')
        self.__seite.zeige_ecke3()

    def ecke3(self, p):
        '''3. Aktion je Foto: Ecke 3 abspeichern und beschnittenes Foto anzeigen.

        Status auf "Foto Kontrolle" setzen
        '''
        self.__seite.speichere_ecke3(p)
        self.__status = 'Foto Kontrolle'
        # self.imagepanel.parent.label_re.SetLabel(f' {self.__status}')
        akt_foto = self.__seite.akt_foto
        # self.imagepanel.parent.label_re.SetLabel(f'   {self.__status} Rahmen: {akt_foto.rahmen_plus}')    
        self.__seite.foto_drehen()

    # 4. Aktion je Foto:
    # Beschnitt ändern
    def foto_beschneiden(self, plusminus):
        '''4. Aktion je Foto: Beschnitt ändern und beschnittenes Foto anzeigen.
        '''
        self.__seite.foto_beschneiden(plusminus)
        akt_foto = self.__seite.akt_foto
        # self.imagepanel.parent.label_re.SetLabel(f'   {self.__status} Rahmen: {akt_foto.rahmen_plus}')    

    def foto_speichern(self, p):
        '''5. Aktion je Foto: Beschnittenes Foto speichern und n. Seite bearbeiten.

        Status auf "Foto fertig" setzen
        '''
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

