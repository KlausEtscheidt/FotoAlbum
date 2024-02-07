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
#from seiten import Seiten
import zeichenfabrik
import filedrop
# import import_export as impex
from filesaver import EVT_RESULT_ID

logger = logging.getLogger('album')

# pylint: disable=R0901
class MainFrame(wx.Frame):
    '''Mainframe zur Darstellung und Steuerung des Ablaufs'''

    def __init__(self, *args, **kw):

        super(MainFrame, self).__init__(*args, **kw)

        self.BackgroundColour = "light blue" # pylint: disable=invalid-name
        self.seiten = None
        self.__bitmap = None
        self.__zbmp = None
        self.__mausanker_rechteck = wx.Point(0,0) #fuer boxdraw
        # self.mousepos = None
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

        # create a menu bar
        self.make_menubar()

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Willkommen beim Alben-Zerleger !")

        #add drop target
        file_drop_target = filedrop.MyFileDropTarget(self)
        self.imagectrl.SetDropTarget(file_drop_target)

        # Events binden
        evh = EvtHandler(self)
        self.next_btn.Bind(wx.EVT_BUTTON, evh.on_next_btn)
        self.prev_btn.Bind(wx.EVT_BUTTON, evh.on_prev_btn)
        self.imagectrl.Bind(wx.EVT_PAINT, evh.on_paint)
        self.imagectrl.Bind(wx.EVT_LEFT_DOWN, evh.on_press_mouse)
        self.imagectrl.Bind(wx.EVT_CHAR_HOOK, evh.on_key_press)
        self.imagectrl.Bind(wx.EVT_MOTION, evh.on_mouse_move)

        # Verbinde Event handler für Rückmeldungen aus worker thread
        self.Connect(-1, -1, EVT_RESULT_ID, evh.on_thread_result)

    @property
    def bitmap(self):
        '''Bitmap zum Anzeigen der Seite oder eines Fotos.'''
        return self.__bitmap

    @property
    def zbmp(self):
        '''Bitmap zum Zeichnen. Wird über **self.bitmap** gelegt.'''
        return self.__zbmp

    @property
    def mausanker_rechteck(self):
        '''Nullpunkt zum Aufziehen eines Rechtecks per Maus.'''
        return self.__mausanker_rechteck

    @mausanker_rechteck.setter
    def mausanker_rechteck(self, punkt):
        self.__mausanker_rechteck = punkt


    def make_menubar(self):
        '''Definiert Menubar für mainframe'''

        # Make the menu bar
        menubar = wx.MenuBar()

        menubar.BackgroundColour = "light blue"

        ## add menus to menu bar.
        #------------------------------------------------------------
        # File menu
        menu = wx.Menu()
        menubar.Append(menu, "&File")
        menu_file.init(self, menu) # Menu-Items und Handler dazu

        # help menu
        menu = wx.Menu()
        menubar.Append(menu, "&Help")
        menu_div.init(self, menu) # Menu-Items und Handler dazu

        # Give the menu bar to the frame
        self.SetMenuBar(menubar)


    # ------------------------------------------------------
    # Zeichnen und Anzeigen
    # ------------------------------------------------------

    def show_pic(self, image_bmp, zeichen_bmp=None, scale=1):
        ''' Zeigt eine image_bmp evtl mit überlagerter zeichen_bmp an.

        Die Bitmaps werden in self.imagectrl angezeigt.
        Das eigentliche Zeichnen wird von dessen OnPaint-Event erledigt.
        Der Event wird durch self.imagectrl.Refresh() ausgelöst.
        Lage und Größe des Bild werden durch self.dc_matrix definiert.
        '''
        # Bitmaps merken für nachfolgende Operationen (OnPaint)
        self.__bitmap = image_bmp
        self.__zbmp = zeichen_bmp
        # Ohne Reset werden hier alte Inhalte angezeigt.
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


    def rescale(self, faktor):
        '''Dient zum Zoomen und den Faktor '*faktor*'

        Args:
            faktor (float): Zoom-Faktor
        '''

        # Bildmitte
        cs = self.imagectrl.GetClientSize()
        bildmitte_x = round(cs.x/2)
        bildmitte_y = round(cs.y/2)

        #Alte Bildmitte in Bitmap
        # pm_bmp1 = self.get_pos_in_bitmap(wx.Point(bildmitte_x, bildmitte_y))

        # Aktuelle Verschiebung
        _mat1, tr1 = self.dc_matrix.Get()

        # Abstand Bildmitte zu tr
        bm_zu_tr_x = bildmitte_x - tr1.x
        bm_zu_tr_y = bildmitte_y - tr1.y

        self.dc_matrix.Scale(faktor, faktor)
        mat2, _tr2 = self.dc_matrix.Get()

        # Abstand wird mit skaliert => rückgängig machen
        bm_zu_tr_x *= (1-faktor)
        bm_zu_tr_y *= (1-faktor)
        self.dc_matrix.Set(mat2,(tr1.x + bm_zu_tr_x, tr1.y + bm_zu_tr_y))

        self.overlay.Reset()
        self.imagectrl.Refresh()
        wx.Yield()

    def translate(self, richtung, delta):
        '''Dient zum Verschieben der Grafik.

        Args:
            richtung (str): Richtung der Verschiebung ("l","r","h","t")
            delta (int): Betrag der Verschiebung in Pixel (Bildschirm-Koordinaten)
        '''
        if richtung == 'l':
            self.dc_matrix.Translate(delta,0)
        if richtung == 'r':
            self.dc_matrix.Translate(-delta,0)
        if richtung == 'h':
            self.dc_matrix.Translate(0,delta)
        if richtung == 't':
            self.dc_matrix.Translate(0,-delta)
        self.overlay.Reset()
        self.imagectrl.Refresh()
        wx.Yield()

    def zeige_ecke(self, nr):
        '''Zeigt eine Ecke gezoomed an.

        Die Anzeige ermöglicht die exakte Auswahl der Ecke eines Fotos.
        Die Koordinaten werden aus dem vorher definierten Grobrahmen ermittelt.
        Der angezeigte Ausschnitt zeigt die linke obere Ecke des Grobrahmens
        in X- und Y-Richtung bei jeweils 25% der Zeichenfläche.
        Ecke 2 (rechts oben) liegt bei 75% X und 25% Y.
        Ecke 3 (rechts unten) liegt bei 75% X und 75% Y.
        Dadurch wird jeweils möglichst viel des Fotos gezeigt.
        Bei Ecke 2 wird eine horizontale Linie in rot angezeigt, welche y von Ecke 1 übernimmt.
        Analog wird für Ecke 3 eine Vertikale mit x von Ecke 2 angezeigt.
        Diese Linien verdeutlichen eine evtl Schrägstellung des Fotos.

        Args:
            nr (int): Nr der Ecke, deren Umfeld gezeigt werden soll.
        '''

        # Koordinaten des Rahmens in der Bitmap
        x1, y1 = self.seiten.akt_seite.akt_foto.p1
        x2, y2 = self.seiten.akt_seite.akt_foto.p2

        # Zuerst die Zielpos der Ecke in Mauskoordinaten und
        # die Koordinaten der anzuzeigenden Ecke in der Bitmap ermitteln
        cs = self.imagectrl.GetClientSize()
        if nr == 1:
            x_bmp = x1
            y_bmp = y1
            ziel_x = int(cs.x * 0.25)
            ziel_y = int(cs.y * 0.25)
        if nr == 2:
            # horizontale Linie zeichnen von Ecke 1 zu Ecke 2
            y = self.seiten.akt_seite.akt_foto.ecke1.y
            self.__zbmp = zeichenfabrik.zeichne_ecke(self.__bitmap, x2-1000, y, x2+100, y)
            # Koordinaten der Ecke
            x_bmp = x2
            y_bmp = y1
            ziel_x = int(cs.x * 0.75)
            ziel_y = int(cs.y * 0.25)
        if nr == 3:
            # vertikale Linie zeichnen von Ecke 2 zu Ecke 3
            x = self.seiten.akt_seite.akt_foto.ecke2.x
            self.__zbmp = zeichenfabrik.zeichne_ecke(self.__bitmap, x, y2-1000, x, y2+100)
            # Koordinaten der Ecke
            x_bmp = x2
            y_bmp = y2
            ziel_x = int(cs.x * 0.75)
            ziel_y = int(cs.y * 0.75)

        # Einheitsmatrix
        self.dc_matrix = wx.AffineMatrix2D()
        # Scale
        self.dc_matrix.Scale(conf.scale_ecke, conf.scale_ecke)
        mat2, _tr2 = self.dc_matrix.Get()

        # Wo liegt unsere Ecke jetzt (Mauskoord)
        dx, dy =self.dc_matrix.TransformPoint(x_bmp, y_bmp)
        self.dc_matrix.Set(mat2,(ziel_x -dx, ziel_y -dy))

        self.overlay.Reset()
        self.imagectrl.Refresh()
        wx.Yield()

    # ------------------------------------------------------
    # Basis Funktionen
    # ------------------------------------------------------
    def zeichne_alles(self):
        '''Stellt die Bitmap einer Seite oder eines Fotos dar.

        Die Bitmap *self.bitmap* wird von einer Bitmap *self.zbmp*
        transparent überlagert, in der Linien gezeichnet wurden.'''
        self.overlay.Reset()
        dc = wx.PaintDC(self.imagectrl)
        self.dc = dc
        dc.SetTransformMatrix(self.dc_matrix)
        dc.SetBackground(wx.Brush("light blue"))
        dc.Clear()
        if self.bitmap:
            dc.DrawBitmap ( self.bitmap, 0, 0, useMask=False)
        if self.zbmp:
            dc.DrawBitmap ( self.zbmp, 0, 0, useMask=True)

    def get_pos_in_bitmap(self, pos):
        '''Ermittelt Bitmap-Koordinaten aus Bildschirm-Koordinaten.

        Hiermit kann z.B. berechnet werden, welches Pixel einer Bitmap per Maus geklickt wurde.'''
        mat, tr = self.dc_matrix.Get()
        new = wx.AffineMatrix2D()
        new.Set(mat, tr)
        new.Invert()
        # mat, tr = new.Get()
        x, y =new.TransformPoint(pos.x,pos.y)
        p2 =  wx.Point(round(x), round(y))
        return p2
