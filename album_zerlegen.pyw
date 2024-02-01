#!/bin/python
import os

import wx

from config import conf
import logging
import alb_logging

from panel_log import LogPanel
from panel_imageview import ImagePanelOuter
import menu_file
import menu_div
from seiten import Seiten

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
        conf.imagepanel = mainframe.imagepanel.innerpanel
        conf.thisapp = self
        #Noetig ????
        self.SetTopWindow(mainframe)
        mainframe.Show()
        logger.debug('Starte Programm')
        self.seiten_laden()
        conf.settings()

        return True

    def seiten_laden(self):

        # Gibt es das zu durchsuchende Verzeichnis "conf.pic_path"
        if not os.path.isdir(conf.pic_path):
            msg = 'Verzeichnis mit Scans wählen'
            with wx.DirDialog(self.mainframe, message=msg, defaultPath=conf.pic_basispfad) as Dlg:
                if Dlg.ShowModal() == wx.ID_CANCEL:
                    return
                conf.pic_path= Dlg.GetPath()
                    
        # Tiff dateien suchen
        self.seiten = Seiten(self.mainframe.imagepanel.innerpanel)
        # Erste Seite bearbeiten
        self.seiten.seite_bearbeiten(0)
    
    def OnExit(self):
        conf.config_write()
        return super().OnExit()

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):

        super(MainFrame, self).__init__(*args, **kw)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        self.imagepanel = ImagePanelOuter(nb, page_id=0)
        self.logpanel = LogPanel(nb, page_id=1)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(self.imagepanel, "File")
        nb.AddPage(self.logpanel, "Log")

        self.imagepanel.Activate()

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Willkommen beim Alben-Zerleger !")


    def makeMenuBar(self):

        # Make the menu bar
        menuBar = wx.MenuBar()

        ## add menus to menu bar.
        #------------------------------------------------------------
        # File menu
        Menu = wx.Menu()
        menuBar.Append(Menu, "&File")
        menu_file.init(self, Menu) # Menu-Items und Handler dazu

        # help menu
        Menu = wx.Menu()
        menuBar.Append(Menu, "&Help")
        menu_div.init(self, Menu) # Menu-Items und Handler dazu

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

def run_app():
    alb_logging.init()
    # app = wx.App()
    app = myApp()

    #Endlos-Schleife
    app.MainLoop()

if __name__ == '__main__':
    run_app()
