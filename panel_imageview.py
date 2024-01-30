import logging

import wx
import wx.lib.scrolledpanel as scrolledp

import config as conf
import filedrop
from seite import Seiten
from ablauf import Ablauf

logger = logging.getLogger('album')


class ImagePanelOuter(wx.Window):
    def __init__(self, parent, page_id):
        wx.Window.__init__(self, parent=parent)
        
        self.parent = parent
        self.id = page_id #id merken zum Umschalten per SetSelection

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

        # Image Panel
        self.ipanel = ImagePanel(self)

        # Gesamt-Layout
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.button_sizer, proportion=0, flag=wx.ALL|wx.ALIGN_TOP, border=1)
        self.main_sizer.Add(self.ipanel, proportion=1, flag=wx.ALL|wx.EXPAND, border=1)

        # Sizer für Gesamt-Panel zuteilen
        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(1)
        self.main_sizer.Fit(self)

        self.next_btn.Bind(wx.EVT_BUTTON, self.OnNextBtn)
        self.prev_btn.Bind(wx.EVT_BUTTON, self.OnPrevBtn)

    # diesen Tab anzeigen
    def Activate(self):
        self.parent.SetSelection(self.id)

    def OnNextBtn(self, _):
        self.ipanel.ablauf.seite_bearbeiten_next()

    def OnPrevBtn(self, _):
        self.ipanel.ablauf.seite_bearbeiten_prev()

##############################################################################################
#
class ImagePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        #add drop target
        file_drop_target = filedrop.MyFileDropTarget(self)
        self.define_ctrls()
        self.ablauf = Ablauf(self)
        self.__bitmap = None
        self.__zbmp = None
        self.__mouse1 = wx.Point(0,0) #fuer boxdraw
        self.mousepos = None
        self.rand = 0  #rand um imagectrl
        self.dc_scale = 1.
        self.dc_matrix = wx.AffineMatrix2D()
        self.overlay = wx.Overlay()

    def define_ctrls(self):
        # Haupt-Image-control
        # self.imagectrl = wx.Window(self, -1, size=(150, 300) )
        self.imagectrl = wx.Window(self, -1)
        self.imagectrl.SetCursor(wx.Cursor(wx.CURSOR_CROSS))
        self.SetFocus() # Einmal Focus auf self, damit key-events empfangen werden

        # Gesamt-Layout
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.imagectrl, proportion=1, flag=wx.ALL|wx.EXPAND, border=1)

        # Sizer für Gesamt-Panel zuteilen
        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(1)
        self.main_sizer.Fit(self)
        # self.SetupScrolling()

        #Handler binden
        
        self.imagectrl.Bind(wx.EVT_PAINT, self.OnPaint)
        self.imagectrl.Bind(wx.EVT_LEFT_DOWN, self.OnPressMouse)
        # self.imagectrl.Bind(wx.EVT_LEFT_UP, self.OnReleaseMouse)
        # self.imagectrl.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
        self.imagectrl.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPress)
        self.imagectrl.Bind(wx.EVT_MOTION, self.OnMouseMove)

    def show_pic(self, image_bmp, zeichen_bmp=None, scale=1):
        self.__bitmap = image_bmp
        self.__zbmp = zeichen_bmp
        # self.zeichen_bitmap(0,(0,0))
        self.overlay.Reset()
        self.dc_matrix = wx.AffineMatrix2D()
        dx, dy =self.dc_matrix.TransformPoint(image_bmp.Width, image_bmp.Height)
        cs = self.imagectrl.GetClientSize()
        dx = round((cs.x - image_bmp.Width * scale)/2)
        dy = round((cs.y - image_bmp.Height * scale)/2)
        self.dc_matrix.Translate(dx,dy)
        self.dc_matrix.Scale(scale, scale)
        # self.dc = self.fotodraw()
        # self.imagectrl.SetMaxSize(wx.Size(bitmap.Width + 2*self.rand, bitmap.Height + 2*self.rand))
        
        self.imagectrl.Refresh()
        wx.Yield()

    def rescale(self, faktor):
        #Alte Bildmitte in Bitmap
        pm_bmp1, xm, ym = self.mitte_anzeige()
        mat1, tr1 = self.dc_matrix.Get()

        self.dc_matrix.Scale(faktor, faktor)
        mat2, tr2 = self.dc_matrix.Get()

        # Mitte Anzeige-Ist in Bitmap-Koord (pm_bmp1 ist Mitte Anzeige-Soll)
        pm_bmp2, xm, ym = self.mitte_anzeige()

        # Delta in Bitmap
        dbmp_x = pm_bmp2.x - pm_bmp1.x
        dbmp_y = pm_bmp2.y - pm_bmp1.y
        
        # Delta in Maus
        dm_x, dm_y =self.dc_matrix.TransformPoint(dbmp_x, dbmp_y)
        
        self.dc_matrix.Set(mat2,(dm_x, dm_y))
        pm_bmp3, xm, ym = self.mitte_anzeige()
        print(f'Mitte: x {pm_bmp3.x} y {pm_bmp3.y}')

        self.overlay.Reset()
        self.imagectrl.Refresh()
        wx.Yield()
        
    def translate(self, richtung):
        delta = 25
        if richtung == 'l':
            self.dc_matrix.Translate(-delta,0)
        if richtung == 'r':
            self.dc_matrix.Translate(delta,0)
        if richtung == 'h':
            self.dc_matrix.Translate(0,-delta)
        if richtung == 't':
            self.dc_matrix.Translate(0,delta)
        self.overlay.Reset()
        self.imagectrl.Refresh()
        wx.Yield()
        
    # ------------------------------------------------------
    # Event handling
    # ------------------------------------------------------
        
    def OnPaint(self, event=None):
        dc = wx.PaintDC(self.imagectrl)
        self.dc = dc
        # m=wx.AffineMatrix2D()
        # m.Translate(10,0)
        erg = dc.SetTransformMatrix(self.dc_matrix)
        # dc.SetUserScale(self.dc_scale, self.dc_scale)
        dc.SetBackground(wx.Brush("sky blue"))
        dc.Clear()
        # dc.SetPen(wx.Pen(wx.RED, 4))
        if self.__bitmap:
            dc.DrawBitmap ( self.__bitmap, self.rand, self.rand, useMask=False)
        if self.__zbmp:
            dc.DrawBitmap ( self.__zbmp, self.rand, self.rand, useMask=True)

    def OnPressMouse(self, event):
        act_pos = event.GetPosition()
        p = self.get_pos_in_bitmap(act_pos)
        if self.ablauf.status == 'Start Seite':
            self.__mouse1 = act_pos
            self.ablauf.rahmen_lo = p
        elif self.ablauf.status == 'Rahmen ru':
            self.ablauf.rahmen_ru = p
            self.ablauf.foto_rahmen_ablegen()
        elif self.ablauf.status == 'Ecke1':
            self.ablauf.ecke1(p)
        elif self.ablauf.status == 'Ecke2':
            self.ablauf.ecke2(p)
        elif self.ablauf.status == 'Ecke3':
            self.ablauf.ecke3(p)
        elif self.ablauf.status == 'Foto definiert':
            self.ablauf.foto_speichern(p)

        # conf.mainframe.SetStatusText(f'n: {self.__mouseclicks} x:{pos.x} y:{pos.y}')
        logger.debug(f'Mausklick bei x:{p.x} y:{p.y}\n')
        
    def OnMouseMove(self, evt):
        act_pos = evt.GetPosition()
        if self.ablauf.status == 'Start Seite':
            self.maus_zeigt_fadenkreuz(act_pos)
            # self.zeichen_bitmap(1, act_pos)
            # self.imagectrl.Refresh()
        elif self.ablauf.status == 'Rahmen ru':
            # if evt.Dragging() and evt.LeftIsDown():
            # self.zeichen_bitmap(2, act_pos)
            # self.imagectrl.Refresh()
            self.maus_zeigt_rahmen(act_pos)
        elif self.ablauf.status in ('Ecke1', 'Ecke2', 'Ecke3'):
            # self.zeichen_bitmap(1, act_pos)
            # self.imagectrl.Refresh()
            self.maus_zeigt_fadenkreuz(act_pos)
        #     dc.CrossHair(act_pos.x, act_pos.y)

    def maus_zeigt_fadenkreuz(self, pos):

        if not self.dc:
            return
        dc=self.dc
        # # dc.Clear()
        # # dc.DrawBitmap ( self.__bitmap, self.rand, self.rand, useMask=False)
        dc = wx.ClientDC(self.imagectrl)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        dc.SetPen(wx.Pen("red", 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.CrossHair(pos.x, pos.y)
        del odc # work around a bug in the Python wrappers to make
                # sure the odc is destroyed before the dc is.

    def maus_zeigt_rahmen(self, pos):
        if not self.dc:
            return
        dc=self.dc
        # dc.Clear()
        dc = wx.ClientDC(self.imagectrl)
        # dc.DrawBitmap ( self.__bitmap, self.rand, self.rand, useMask=False)
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        dc.SetPen(wx.Pen("red", 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        x1, y1 = self.__mouse1
        x2, y2 = pos
        dc.DrawRectangle(x1, y1, x2-x1, y2-y1)
        del odc # work around a bug in the Python wrappers to make
                # sure the odc is destroyed before the dc is.

    # def OnReleaseMouse(self, event):
    #     self.pos2 = event.GetPosition()
    #     self.imagectrl.Refresh()

    def OnKeyPress(self, event):
        keycode = event.GetKeyCode()    
        print(keycode)
        conf.mainframe.SetStatusText(str(keycode))
        if keycode == 388:  #num+
            self.rescale(2.)
        if keycode == 390:  #num-
            self.rescale(.5)

        if keycode == 314: #links
            self.translate('l')
        if keycode == 316: #rechts
            self.translate('r')
        if keycode == 315: #hoch
            self.translate('h')
        if keycode == 317: #tief
            self.translate('t')

        if keycode == wx.WXK_SPACE:
            print("you pressed the spacebar!")
            # self.next_bearbeiten()
            self.weiter()
        # event.Skip()

    #     menu = self.MakePopUpMenu()
    #     self.PopupMenu(menu, m_pos)

    # ------------------------------------------------------
    # High-Level Funktionen
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Basis Funktionen
    # ------------------------------------------------------
        
    def get_pos_in_bitmap(self, pos):
        mat, tr = self.dc_matrix.Get()
        new = wx.AffineMatrix2D()
        new.Set(mat, tr)
        new.Invert()
        # mat, tr = new.Get()
        x, y =new.TransformPoint(pos.x,pos.y)
        p2 =  wx.Point(round(x), round(y))
        return p2

    # => bildmitte in bmp-koord
    def mitte_anzeige(self):
        xmax = self.dc.MaxX()
        xmin = self.dc.MinX()
        ymin = self.dc.MinY()
        ymax = self.dc.MaxY()
        xmitte = round((xmin+xmax)/2)
        ymitte = round((ymin+ymax)/2)
        pmitte = self.get_pos_in_bitmap(wx.Point(xmitte,ymitte))
        return pmitte, xmitte, ymitte
