"""
seiten.py
=====================================================
Speichert alle Seiten.
Dient zur Steuerung des Ablaufs (Div. Funktionen werden von den Evt-Handlern gerufen)
"""

import logging
import glob

# import wx

from config import conf
from seite import Seite

logger = logging.getLogger('album')


class Seiten(list):
    '''Liste aller Seiten eines Fotoalbums (Tiff-Dateien)

    Nimmt alle Seiten auf und wird von Events gesteuert
    '''

    def __init__(self, parent):
        '''Durchsucht Verzeichnis nach tif-Dateien und erzeugt eine Seite je Tiff

        Args:
            imagepanel (ImagePanel): widget zur Darstellung einer Seite (Bitmap)
        '''
        self.mainframe = parent
        self.imagectrl = parent.imagectrl

        # Klassenvar in Seite setzen
        # imagepanel ist self.mainframe.imagepanel.innerpanel
        Seite.mainframe = parent

        # self.myfilenames = []
        self.seitenliste_erstellen()

        #: Kontrolliert den Ablauf
        self.__status = 'Start Seite/Foto'

        self.__id_aktseite = 0
        '''Index der aktuell bearbeiteten Seite'''
        self.__aktseite = None
        '''aktuell bearbeitete Seite'''

    @property
    def akt_seite(self):
        '''Instanz der aktuell bearbeiteten Seite'''
        return self.__aktseite

    @akt_seite.setter
    def akt_seite(self, x):
        self.__aktseite = x

    @property
    def id_aktseite(self):
        '''id der aktuell bearbeiteten Seite (in der Liste aller Seiten)'''
        return self.__id_aktseite

    @id_aktseite.setter
    def id_aktseite(self, x):
        self.__id_aktseite = x


    @property
    def status(self):
        '''Aktueller Stand der Bearbeitung'''
        return self.__status

    @status.setter
    def status(self, x):
        self.__status = x


    ############################################################################
    #
    # Aktionen übergeordnet
    #
    ############################################################################

    def seitenliste_erstellen(self):
        '''Filenamen der Seiten-Tiffs einlesen

        Seiten erzeugen (ohne image) und in Liste merken
        '''

        # Suche Bilder
        myfilenames = glob.glob(conf.pic_path + r"\*" + conf.pic_type)

        # Fuer jeden gefundenen Pfad, Seitenobjekt erzeugen und merken
        for fullpath in myfilenames:
            seite = Seite(fullpath)
            self.append(seite)

        msg = f'Liste mit {len(self):d} Bildern geladen.'
        # if conf.mainframe:
        self.mainframe.SetStatusText(msg)
        logger.debug(msg + f'\nVerzeichnis: {conf.pic_path} Endung: {conf.pic_type}\n')


    def foto_neu_beschneiden(self, pfad_zum_foto=None, mauspos=None):
        '''Benutzer kann Beschnittrahmen ändern

        Aufruf durch droppen des zu korrigierenden Tif-Files oder Strg-s über Foto
        :param pfad_zum_foto: filename des berits gespeicherten Fotos, defaults to None
        :type pfad_zum_foto: string, optional
        :param mauspos: Mauspos in Bitmap-Koord beim Drücken von Strg-s, defaults to None
        :type mauspos: wx.Point, optional
        '''

        foto_zum_schneiden = None

        # Wenn mit mauspos aufgerufen
        if mauspos:
            seiten_nr = self.id_aktseite
            akt_seite = self[seiten_nr]
            #Suche ein Foto, das die geklickte Pos umgibt
            for foto in akt_seite.fotos:
                if foto.pos_ist_innen(mauspos.x, mauspos.y):
                    foto_zum_schneiden = foto
                    break

        # Wenn mit Pfad aufgerufen
        if pfad_zum_foto:
            seiten_nr = 0
            for seite in self:
                for foto in seite.fotos:
                    if pfad_zum_foto == foto.saved_in:
                        foto_zum_schneiden = foto
                        break
                if foto_zum_schneiden:
                    break
                seiten_nr += 1

        if foto_zum_schneiden:
            # Seite anzeigen
            self.seite_bearbeiten(seiten_nr)
            # Zustand nach foto_drehen herstellen
            self.akt_seite.akt_foto = foto_zum_schneiden
            self.status = 'Foto Kontrolle'
            self.akt_seite.foto_drehen()

    def alle_speichern(self):
        '''Alle definierten Fotos exportieren'''
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
        self.mainframe.SetStatusText('Foto definieren')

        self.imagectrl.SetFocus()

        # Seite als aktiv merken (Id und Objekt)
        self.akt_seite = self[seiten_nr]
        self.id_aktseite = seiten_nr

        # Status auf Anfang Seite bearbeiten
        self.status = 'Start Seite/Foto'

        # Anzeigen
        txt = f'{self.akt_seite.basename}{self.akt_seite.typ}   ({seiten_nr+1:d} von {len(self)})'
        self.mainframe.label_li.SetLabel(txt)
        self.mainframe.label_re.SetLabel(f'{self.status}')
        self.akt_seite.seite_laden()

    def seite_bearbeiten_next(self):
        '''Nächste Seite anwählen und bearbeiten'''
        if self.id_aktseite < len(self)-1:
            self.id_aktseite += 1
        else:
            self.id_aktseite = 0
        self.seite_bearbeiten(self.id_aktseite)

    def seite_bearbeiten_prev(self):
        '''Vorhergehende Seite anwählen und bearbeiten'''
        if self.id_aktseite > 0:
            self.id_aktseite -= 1
        else:
            self.id_aktseite = len(self)-1
        self.seite_bearbeiten(self.id_aktseite)


    ############################################################################
    #
    # Aktionen je Foto
    #
    ############################################################################

    def reset(self):
        """reset Bearbeitung abbrechen

        Status auf Start Seite/Foto setzen
        Fragmente der Eingabe loeschen
        """
        akt_seite = self[self.id_aktseite]
        akt_foto = akt_seite.akt_foto
        # akt_foto wird beim Klicken des Rahmens l.o gesetzt
        if akt_foto:
            # loeschen wenn noch nicht fertig definiert
            if not akt_foto.fertig:
                akt_seite.fotos.remove(akt_foto)
                akt_seite.akt_foto = None
        #Status reset und weiter
        self.seite_bearbeiten(self.id_aktseite)

    def foto_entfernen(self, mauspos):
        '''Entfernt die Definition eines Fotos'''
        akt_seite = self[self.id_aktseite]
        for foto in akt_seite.fotos:
            if foto.pos_ist_innen(mauspos.x, mauspos.y):
                akt_seite.fotos.remove(foto)
                break
        self.seite_bearbeiten(self.id_aktseite)
