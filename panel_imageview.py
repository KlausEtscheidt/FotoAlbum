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
        self.__seite = None
        self.__status = 'Start Seite'
        self.__seiten_nr = -1
        self.__bitmap = None
        self.__mouseclicks = 0
        self.__pos = [] #speichert mausklicks
        self.rand = 10  #rand um imagectrl
        # Haupt-Image-control
        self.imagectrl = wx.Window(self, -1, size=(1500, 3000) )
        self.imagectrl.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.SetFocus() #Einmal Focus auf self, damit key-events empfangen werden

        #-------------------------------------------------------

        # Gesamt-Layout (Textctrl und searchbox)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.imagectrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=1)

        # Sizer für Gesamt-Panel zuteilen
        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(1)
        self.main_sizer.Fit(self)
        self.SetupScrolling()

        #Handler binden
        self.imagectrl.Bind(wx.EVT_PAINT, self.OnPaint)
        self.imagectrl.Bind(wx.EVT_LEFT_DOWN, self.OnPressMouse)
        self.imagectrl.Bind(wx.EVT_LEFT_UP, self.OnReleaseMouse)
        self.imagectrl.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
        # self.imagectrl.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPress)
        
        #Damit Panel den Fokus bekommt (fuer keypress)
        # self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)

    def seite_bearbeiten_next(self):
        if self.__seiten_nr < len(self.__seiten)-1:
            self.__seiten_nr += 1
            self.seite_bearbeiten(self.__seiten_nr)

    def dateiliste_erstellen(self):
        # Filenamen der Seiten-Tiffs einlesen
        # Seiten erzeugen (ohne image) und in Liste merken
        self.__seiten = Seiten(self)
    
    def seite_bearbeiten(self, seiten_nr):
        self.__seiten_nr = seiten_nr # merken f next
        # Status auf Anfang Seite bearbeiten
        self.__status = 'Start Seite'
        # Seite als aktiv merken
        self.__seite = self.__seiten[seiten_nr]
        # Anzeigen
        self.__seite.show_origbild()

    def show_pic(self, bitmap):
        self.__bitmap = bitmap
        self.imagectrl.Refresh()
        wx.Yield()

    #Funktion wird von Key-Event 'space' aufgerufen
    # Pruefen, was als naechstes zu tun ist
    def weiter(self):
        # self.seite_bearbeiten_next()
        # return
        if self.__status == 'Start Seite':
            # Haben wir zwei Punkte geklickt
            if len(self.__pos) == 2:
                # Skalierung in der Anzeige beachten
                p1 = self.koor_trans(self.__pos[0])
                p2 = self.koor_trans(self.__pos[1])
                #Foto erzeugen und ablegen
                self.__seite.foto_dazu(p1, p2)
                self.__seite.zeige_ecke3()
                # self.__seite.show_origbild()
                # Mauspunkte loeschen
                self.__pos = []
                # Weiter mit exakter Eckendefinition
                self.__status == '1. Ecke'
            else:
                msg = f'Status: {self.__status}. Erst Rahmen klicken.'
                wx.MessageBox(msg, 'Fehler!', wx.OK|wx.ICON_INFORMATION)

    # ------------------------------------------------------
    # Event handling
    # ------------------------------------------------------
    
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self.imagectrl)
        dc.Clear()
        # dc.SetPen(wx.Pen(wx.RED, 4))
        if self.__bitmap:
            dc.DrawBitmap ( self.__bitmap, self.rand, self.rand, useMask=False)
        # dc.DrawLine(0,0,1000,1200)        

    def OnPressMouse(self, event):
        pos = event.GetPosition()
        self.__pos.append(pos)
        self.__mouseclicks += 1
        conf.mainframe.SetStatusText(f'x:{pos.x} y:{pos.y}')
        logger.debug(f'Mausklick bei x:{pos.x} y:{pos.y}\n')

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
            self.weiter()
            
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

    def koor_trans(self, p):
        p_trans = wx.Point(0,0)
        p_trans.x = int( (p.x - self.rand) / conf.SCALE_SEITE)
        p_trans.y = int( (p.y - self.rand) / conf.SCALE_SEITE)
        return p_trans

