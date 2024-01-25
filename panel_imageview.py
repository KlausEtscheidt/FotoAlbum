import pathlib
import subprocess
import wx
import wx.lib.scrolledpanel as scrolledp

import config as conf
import filedrop
# import FileClass
# import DiskImport
# import DiskTools

#from PopUpMenu_Files import FilePopupMenu

# class ImagePanel(wx.Panel):
class ImagePanel(scrolledp.ScrolledPanel):
    def __init__(self, parent, page_id):
        # wx.Panel.__init__(self, parent=parent)
        scrolledp.ScrolledPanel.__init__(self, parent=parent)

        self.parent = parent
        self.id = page_id #id merken zum Umschalten per SetSelection
        

        #add drop target
        file_drop_target = filedrop.MyFileDropTarget(self)

        self.bitmap = None

        # leere bitmap
        # mybitmap = wx.Bitmap()
        # Haupt-Image-control
        # self.imagectrl = wx.StaticBitmap(self, -1, mybitmap, (0,0), (300,400))
        self.imagectrl = wx.Panel(self, -1, size=(1500, 3000) )
        self.imagectrl.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))

        #-------------------------------------------------------

        # Gesamt-Layout (Textctrl und searchbox)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.imagectrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=5)

        # Sizer für Gesamt-Panel zuteilen
        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(1)
        self.main_sizer.Fit(self)
        self.SetupScrolling()

        #Handler binden
        #R-Maus in Anzeige für Popup Menu
        # self.txtctrl.Bind(wx.EVT_RIGHT_DOWN, self.OnRMouseClick)
        self.pos1, self.pos2 = None, None
        self.imagectrl.Bind(wx.EVT_PAINT, self.OnPaint)
        self.imagectrl.Bind(wx.EVT_LEFT_DOWN, self.pressMouse)
        self.imagectrl.Bind(wx.EVT_LEFT_UP, self.releaseMouse)        

    def center_bitmap(self):
        self.ScrollChildIntoView( self.imagectrl)        

    # ------------------------------------------------------
    # Event handling
    # ------------------------------------------------------
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self.imagectrl)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.RED, 4))
        if self.bitmap:
            dc.DrawBitmap ( self.bitmap, 10, 10, useMask=False)
        dc.DrawLine(0,0,1000,1200)        

    def pressMouse(self, event):
        self.pos1 = event.GetPosition()
        conf.mainframe.SetStatusText(f'x:{self.pos1.x} y:{self.pos1.y}')

    def releaseMouse(self, event):
        self.pos2 = event.GetPosition()
        self.imagectrl.Refresh()        

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
