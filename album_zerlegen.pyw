#!/bin/python
# import sys
# print(sys.executable)

import wx

import config as conf
import logging
import alb_logging

from panel_log import LogPanel
from panel_imageview import ImagePanel
import menu_file
import menu_div
import seite

logger = logging.getLogger('album')

# Ermöglicht Auto-Start bei OnEventLoopEnter, also nach myApp.MainLoop()
class myApp(wx.App):
    def OnEventLoopEnter(self, loop):
        # seite.main_loop()
        conf.mainframe.imagepanel.start_bearbeiten()
        return super().OnEventLoopEnter(loop)

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):

        super(MainFrame, self).__init__(*args, **kw)

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        self.imagepanel = ImagePanel(nb, page_id=0)
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
    #Erzeuge Basis-Frame
    conf.mainframe = MainFrame(None, title='KE`s Alben-Zerleger', size=(800, 800), pos=(20, 20))
    conf.mainframe.Show()
    logger.debug('Starte Programm')

    #Endlos-Schleife
    app.MainLoop()

if __name__ == '__main__':
    run_app()
