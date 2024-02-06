#!/bin/python
'''
FotoAlbum.py
----------------

Hauptprogramm
'''

import os

import wx

from config import conf
import logging
import alb_logging

from mainframe import MainFrame
from seiten import Seiten
import import_export as impex

logger = logging.getLogger('album')

# Ermöglicht Auto-Start bei OnEventLoopEnter, also nach myApp.MainLoop()
class myApp(wx.App):
   
    def OnInit(self):
        # self.leaving = False
        #Erzeuge Basis-Frame
        mainframe = MainFrame(None, title='KE`s Alben-Zerleger', size=(800, 800), pos=(20, 20))
        mainframe.SetTransparent(254) #Soll flickern verhindern
        self.mainframe = mainframe
        conf.mainframe = mainframe
        conf.thisapp = self
        #Noetig ????
        self.SetTopWindow(mainframe)
        mainframe.Show()
        logger.debug('Starte Programm')
        self.seiten_laden()

        return True

    def seiten_laden(self):

        # Gibt es das zu durchsuchende Verzeichnis "conf.pic_path"
        if not os.path.isdir(conf.pic_path):
            msg = 'Verzeichnis mit Scans wählen'
            with wx.DirDialog(self.mainframe, message=msg, defaultPath=conf.pic_basispfad) as Dlg:
                if Dlg.ShowModal() == wx.ID_CANCEL:
                    return
                conf.pic_path = Dlg.GetPath()

        # Tiff dateien suchen
        self.mainframe.seiten = Seiten(self.mainframe)

        # Evtl bereits vorhandene Rahmen aus Toml einlesen
        impex.einlesen(self.mainframe.seiten, conf.pic_path)

        # Erste Seite bearbeiten
        self.mainframe.seiten.seite_bearbeiten(0)

    def OnExit(self):
        conf.config_write()
        impex.ausgeben(self.mainframe.seiten, conf.pic_path)
        return super().OnExit()

def run_app():
    alb_logging.init()
    # app = wx.App()
    app = myApp()

    #Endlos-Schleife
    app.MainLoop()

if __name__ == '__main__':
    run_app()
