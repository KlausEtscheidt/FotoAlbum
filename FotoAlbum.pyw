#!/bin/python
'''
FotoAlbum.py
----------------

Hauptprogramm
'''

import os
import logging

import wx

from config import conf
import alb_logging

from mainframe import MainFrame
from seiten import Seiten
import import_export as impex

logger = logging.getLogger('album')

# Ermöglicht Auto-Start bei OnEventLoopEnter, also nach myApp.MainLoop()
class MyApp(wx.App):
    '''Hauptprogramm

        Eigene Klasse statt wx.App ermöglicht Initialisierungen nach Aufbau aller GUI-Elemente
    '''

    # pylint: disable=invalid-name
    def OnInit(self):
        '''Konstruktor'''

        #Erzeuge Basis-Frame
        mainframe = MainFrame(None, title='KE`s Alben-Zerleger', size=(800, 800), pos=(20, 20))
        mainframe.SetTransparent(254) #Soll flickern verhindern
        self.mainframe = mainframe # pylint: disable=attribute-defined-outside-init
        conf.mainframe = mainframe
        conf.thisapp = self
        #Noetig ????
        self.SetTopWindow(mainframe)
        mainframe.Show()
        logger.debug('Starte Programm')
        self.seiten_laden()

        return True

    def seiten_laden(self):
        '''Durchsucht Verzeichnis nach Tiff-Dateien und legt Instanzen der Klasse seite an.

        Das Verzeichnis wird aus conf.pic_path ermittelt. 
        Wenn dieses nicht existiert, wird es per Dialog erfragt.
        '''

        # Gibt es das zuletzt benutzte Verzeichnis "conf.pic_path" noch
        if not os.path.isdir(conf.pic_path):
            msg = 'Verzeichnis mit Scans wählen'
            with wx.DirDialog(self.mainframe, message=msg, defaultPath=conf.pic_basispfad) as dlg:
                if dlg.ShowModal() == wx.ID_CANCEL:
                    return
                conf.pic_path = dlg.GetPath()

        # Tiff dateien suchen
        self.mainframe.seiten = Seiten(self.mainframe)

        # Evtl bereits vorhandene Rahmen aus Toml einlesen
        impex.einlesen(self.mainframe.seiten, conf.pic_path)

        # Erste Seite bearbeiten
        self.mainframe.seiten.seite_bearbeiten(0)

    def OnExit(self):
        '''Bei Programmende Konfiguration und bisher definierte Fotos in Toml-Dateien sichern.'''
        conf.config_write()
        impex.ausgeben(self.mainframe.seiten, conf.pic_path)
        return super().OnExit()

if __name__ == '__main__':
    alb_logging.init()
    app = MyApp()

    #Endlos-Schleife
    app.MainLoop()
