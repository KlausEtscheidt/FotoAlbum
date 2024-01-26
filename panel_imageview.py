import logging

import wx
import wx.lib.scrolledpanel as scrolledp

import config as conf
import filedrop
from seite import Seiten, Seite

logger = logging.getLogger('album')

class ImagePanelOuter(scrolledp.ScrolledPanel):
    def __init__(self, parent, page_id):
        scrolledp.ScrolledPanel.__init__(self, parent=parent)

class ImagePanel(scrolledp.ScrolledPanel):
    def __init__(self, parent, page_id):
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
        self.define_ctrls()

    def define_ctrls(self):

        # Haupt-Image-control
        self.imagectrl = wx.Window(self, -1, size=(1500, 3000) )
        self.imagectrl.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.SetFocus() # Einmal Focus auf self, damit key-events empfangen werden

        #-------------------------------------------------------------------
        # Buttons
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer_i = wx.BoxSizer(wx.HORIZONTAL)
        self.next_btn = wx.Button(self, -1, '>>')
        self.prev_btn = wx.Button(self, -1, '<<')
        # self.button_sizer.AddStretchSpacer()
        self.button_sizer_i.Add(self.prev_btn, flag=wx.LEFT|wx.ALIGN_CENTER, border=5)
        self.button_sizer_i.Add(self.next_btn, flag=wx.LEFT|wx.ALIGN_CENTER, border=5)
        self.button_sizer.Add(self.button_sizer_i, flag=wx.LEFT|wx.ALIGN_CENTER, border=100)
        # self.button_sizer.AddStretchSpacer()
        # Gesamt-Layout
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.button_sizer, proportion=0, flag=wx.ALL|wx.ALIGN_TOP, border=1)
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

    # Funktion wird von Key-Event 'space' aufgerufen
    # Pruefen, was als naechstes zu tun ist
    def weiter(self):
        if self.__status == 'Start Seite':
            # Haben wir zwei Punkte geklickt
            if len(self.__pos) == 2:
                #Foto erzeugen und ablegen
                self.__seite.foto_dazu(self.__pos[0], self.__pos[1])
                # self.__seite.show_origbild()
                # Mauspunkte loeschen
                self.__pos = []
                # Weiter mit exakter Eckendefinition
                self.__status = 'Ecke1'
                self.__seite.zeige_ecke1()
            else:
                msg = f'Status: {self.__status}. Erst Rahmen klicken.'
                wx.MessageBox(msg, 'Fehler!', wx.OK|wx.ICON_INFORMATION)

        elif self.__status == 'Ecke1':
                self.__seite.speichere_ecke1(self.__pos[0])
                self.__pos = []
                self.__status = 'Ecke2'
                self.__seite.zeige_ecke2()

        elif self.__status == 'Ecke2':
                self.__seite.speichere_ecke2(self.__pos[0])
                self.__pos = []
                self.__status = 'Ecke3'
                self.__seite.zeige_ecke3()

        elif self.__status == 'Ecke3':
                self.__seite.speichere_ecke3(self.__pos[0])
                self.__pos = []
                self.__status = 'Ende Seite'
                self.__seite.ausgeben()

        elif self.__status == 'Ende Seite':
            self.seite_bearbeiten_next()

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
        # Rand berücksichtigen
        pos.x -= self.rand
        pos.y -= self.rand
        # merken
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

