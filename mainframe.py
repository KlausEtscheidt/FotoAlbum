#!/bin/python
'''
mainframe.py
----------------

Hauptpanel
'''

# import os
import logging

import wx

from config import conf
#from panel_log import LogPanel
import menu_file
import menu_div
from mainframe_evts import EvtHandler
from seiten import Seiten
import filedrop
# import import_export as impex
from filesaver import EVT_RESULT_ID

logger = logging.getLogger('album')

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):

        super(MainFrame, self).__init__(*args, **kw)

        self.seiten = None
        self.__bitmap = None
        self.__zbmp = None
        self.__mausanker_rechteck = wx.Point(0,0) #fuer boxdraw
        self.mousepos = None
        self.dc = None
        self.dc_scale = 1.
        self.dc_matrix = wx.AffineMatrix2D()
        self.overlay = wx.Overlay() #zum temp Zeichnen        

        # Unterfenster fuer bitmaps
        self.imagectrl = wx.Window(self)

        #-------------------------------------------------------------------
        # Buttons und labels oben
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # self.label_li = wx.StaticText(self, -1, size=(300,20), label='links')
        self.label_li = wx.StaticText(self, -1, size=(200,15), style = wx.ALIGN_LEFT)
        self.next_btn = wx.Button(self, -1, '>>')
        self.prev_btn = wx.Button(self, -1, '<<')
        self.label_re = wx.StaticText(self, -1, size=(200,15), style = wx.ALIGN_LEFT)
        # self.button_sizer.AddStretchSpacer()
        self.button_sizer.Add(self.label_li, flag=wx.TOP, border=5)
        self.button_sizer.AddSpacer(size=100)
        self.button_sizer.Add(self.prev_btn)
        self.button_sizer.Add(self.next_btn, flag=wx.LEFT, border=10)
        self.button_sizer.Add(self.label_re, flag=wx.LEFT|wx.Top, border=15)
        
        # Gesamt-Layout
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.button_sizer, proportion=0, flag=wx.ALL|wx.ALIGN_TOP, border=1)
        main_sizer.Add(self.imagectrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=1)

        self.SetSizer(main_sizer)

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        # sizer = wx.BoxSizer()
        # sizer.Add(nb, 1, wx.EXPAND)
        # p.SetSizer(sizer)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Willkommen beim Alben-Zerleger !")

        #add drop target
        file_drop_target = filedrop.MyFileDropTarget(self)
        self.imagectrl.SetDropTarget(file_drop_target)

        # Events binden
        evh = EvtHandler(self)
        self.next_btn.Bind(wx.EVT_BUTTON, evh.OnNextBtn)
        self.prev_btn.Bind(wx.EVT_BUTTON, evh.OnPrevBtn)
        self.imagectrl.Bind(wx.EVT_PAINT, evh.OnPaint)
        self.imagectrl.Bind(wx.EVT_LEFT_DOWN, evh.OnPressMouse)
        self.imagectrl.Bind(wx.EVT_CHAR_HOOK, evh.OnKeyPress)
        self.imagectrl.Bind(wx.EVT_MOTION, evh.OnMouseMove)

        # Verbinde Event handler für Rückmeldungen aus worker thread
        self.Connect(-1, -1, EVT_RESULT_ID, evh.OnThreadResult)
    
    @property
    def bitmap(self):
        return(self.__bitmap)

    @property
    def zbmp(self):
        return(self.__zbmp)
    
    @property
    def mausanker_rechteck(self):
        return(self.__mausanker_rechteck)

    @mausanker_rechteck.setter
    def mausanker_rechteck(self, punkt):
        self.__mausanker_rechteck = punkt


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


    # ------------------------------------------------------
    # High-Level Funktionen
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Basis Funktionen
    # ------------------------------------------------------

    def MausKlickAktionen(self, act_pos):
        p = self.get_pos_in_bitmap(act_pos)
        if self.seiten.status == 'Start Seite/Foto':
            self.mausanker_rechteck = act_pos
            self.seiten.rahmen_lo = p
        elif self.seiten.status == 'Rahmen ru':
            self.seiten.rahmen_ru = p
            self.seiten.foto_rahmen_ablegen()
        elif self.seiten.status == 'Ecke1':
            self.seiten.ecke1(p)
        elif self.seiten.status == 'Ecke2':
            self.seiten.ecke2(p)
        elif self.seiten.status == 'Ecke3':
            self.seiten.ecke3(p)
        elif self.seiten.status == 'Foto Kontrolle':
            self.seiten.foto_speichern(p)

        # conf.mainframe.SetStatusText(f'n: {self.__mouseclicks} x:{pos.x} y:{pos.y}')
        logger.debug(f'Mausklick bei x:{p.x} y:{p.y}\n')


    def get_pos_in_bitmap(self, pos):
        mat, tr = self.dc_matrix.Get()
        new = wx.AffineMatrix2D()
        new.Set(mat, tr)
        new.Invert()
        # mat, tr = new.Get()
        x, y =new.TransformPoint(pos.x,pos.y)
        p2 =  wx.Point(round(x), round(y))
        return p2

    # ------------------------------------------------------
    # Zeichnen und Anzeigen
    # ------------------------------------------------------

    def show_pic(self, image_bmp, zeichen_bmp=None, scale=1):
        ''' Zeigt eine image_bmp evtl mit überlagerter zeichen_bmp an. 

        Das Zeichnen wird vom OnPaint-Event erledigt 
        '''
        self.__bitmap = image_bmp
        self.__zbmp = zeichen_bmp
        self.overlay.Reset()
        self.dc_matrix = wx.AffineMatrix2D()
        dx, dy =self.dc_matrix.TransformPoint(image_bmp.Width, image_bmp.Height)
        cs = self.imagectrl.GetClientSize()
        dx = round((cs.x - image_bmp.Width * scale)/2)
        dy = round((cs.y - image_bmp.Height * scale)/2)
        self.dc_matrix.Translate(dx,dy)
        self.dc_matrix.Scale(scale, scale)
        
        self.imagectrl.Refresh()
        wx.Yield()


