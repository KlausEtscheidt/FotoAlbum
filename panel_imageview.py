import logging

import wx
import wx.lib.scrolledpanel as scrolledp

import config as conf
import filedrop
from seite import Seiten, Seite

logger = logging.getLogger('album')

# class ImagePanel(wx.Panel):
class ImagePanel(scrolledp.ScrolledPanel):
    def __init__(self, parent, page_id):
        # wx.Panel.__init__(self, parent=parent)
        scrolledp.ScrolledPanel.__init__(self, parent=parent)

        self.parent = parent
        self.id = page_id #id merken zum Umschalten per SetSelection

        #add drop target
        file_drop_target = filedrop.MyFileDropTarget(self)
        self.__seiten = None
        self.__seite = None#
        self.__seiten_nr = -1
        self.__bitmap = None
        self.__mouseclicks = 0
        self.__pos = []
        
        # Haupt-Image-control
        self.imagectrl = wx.Panel(self, -1, size=(1500, 3000) )
        self.imagectrl.SetCursor(wx.Cursor(wx.CURSOR_CROSS))

        #-------------------------------------------------------

        # Gesamt-Layout (Textctrl und searchbox)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.imagectrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)

        # Sizer für Gesamt-Panel zuteilen
        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(1)
        self.main_sizer.Fit(self)
        self.SetupScrolling()

        #Handler binden
        self.imagectrl.Bind(wx.EVT_PAINT, self.OnPaint)
        self.imagectrl.Bind(wx.EVT_LEFT_DOWN, self.OnPressMouse)
        self.imagectrl.Bind(wx.EVT_LEFT_UP, self.OnReleaseMouse)
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPress)
        
        #Damit Panel den Fokus bekommt (fuer keypress)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)

    def next_bearbeiten(self):
        if self.__seiten_nr < len(self.__seiten):
            self.__seiten_nr += 1
            bild = self.__seiten[self.__seiten_nr]
            self.__seite = Seite(bild)
            self.__seite.show_origbild()

    def start_bearbeiten(self):
        self.__seiten_nr = 0
        # Bilder der Seiten einlesen
        self.__seiten = Seiten(self)
        bild = self.__seiten[self.__seiten_nr]
        # Seitenobjekt erzeugen
        self.__seite = Seite(bild)
        self.__seite.show_origbild()
        # self.__seiten.bearbeiten()

    def show_pic(self, bitmap):
        self.__bitmap = bitmap
        self.imagectrl.Refresh()
        wx.Yield()
        # self.status = 'Start'

    def rahmen(self):
        msg = f'x1 { self.__pos[0].x} y1 { self.__pos[0].y} '
        logger.debug(msg + f'x2 { self.__pos[1].x} y2 { self.__pos[1].y}')
        self.__seite.show_framed(self.__pos[0], self.__pos[1])
        self.__pos = []

    # ------------------------------------------------------
    # Event handling
    # ------------------------------------------------------
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self.imagectrl)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.RED, 4))
        if self.__bitmap:
            dc.DrawBitmap ( self.__bitmap, 20, 20, useMask=False)
        dc.DrawLine(0,0,1000,1200)        

    def OnPressMouse(self, event):
        pos = event.GetPosition()
        self.__pos.append(pos)
        self.__mouseclicks += 1
        conf.mainframe.SetStatusText(f'x:{pos.x} y:{pos.y}')

    def OnMouseEnter(self, evt):
        self.SetFocusIgnoringChildren()
    
    def OnReleaseMouse(self, event):
        self.pos2 = event.GetPosition()
        self.imagectrl.Refresh()

    def OnKeyPress(self, event):
        keycode = event.GetKeyCode()    
        print(keycode)
        if keycode == wx.WXK_SPACE:
            print("you pressed the spacebar!")
            # self.next_bearbeiten()
            self.rahmen()
            
        event.Skip()
        conf.mainframe.SetStatusText(str(keycode))

    # def OnRMouseClick(self, event):
    #     m_pos = event.GetPosition()  # Pixel-Koordinaten
    #     _p, _x, y = self.txtctrl.HitTest(m_pos) #Text-Koord
    #     myfilepath = self.txtctrl.GetLineText(y)
    #     self.selected_file = myfilepath

    #     menu = self.MakePopUpMenu()
    #     self.PopupMenu(menu, m_pos)



        
    # ------------------------------------------------------
    # High-Level Funktionen
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Basis Funktionen
    # ------------------------------------------------------

    #Seite anzeigen
    def Activate(self):
        self.parent.SetSelection(self.id)
