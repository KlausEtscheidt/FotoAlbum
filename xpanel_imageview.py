'''
panel_imageview.py
-------------------

Panel zur Bearbeitung und Anzeige der Seiten (Tiff)
'''

import logging

import wx
import wx.lib.scrolledpanel as scrolledp

from config import conf
import filedrop
from seiten import Seiten

logger = logging.getLogger('album')


class ImagePanelOuter(wx.Window):
    def __init__(self, parent, page_id):
        wx.Window.__init__(self, parent=parent)
        
        self.parent = parent
        self.id = page_id #id merken zum Umschalten per SetSelection

        #-------------------------------------------------------------------
        # Buttons
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
        

        # Image Panel
        self.innerpanel = ImagePanel(self)

        # Gesamt-Layout
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.button_sizer, proportion=0, flag=wx.ALL|wx.ALIGN_TOP, border=1)
        self.main_sizer.Add(self.innerpanel, proportion=1, flag=wx.ALL|wx.EXPAND, border=1)

        # Sizer für Gesamt-Panel zuteilen
        self.SetSizer(self.main_sizer)
        self.SetAutoLayout(1)
        self.Layout()
        # self.main_sizer.Fit(self)

        self.next_btn.Bind(wx.EVT_BUTTON, self.OnNextBtn)
        self.prev_btn.Bind(wx.EVT_BUTTON, self.OnPrevBtn)

    # diesen Tab anzeigen
    def Activate(self):
        self.parent.SetSelection(self.id)

    def OnNextBtn(self, _):
        self.innerpanel.seiten.seite_bearbeiten_next()

    def OnPrevBtn(self, _):
        self.innerpanel.seiten.seite_bearbeiten_prev()

##############################################################################################
#
class ImagePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent

        self.define_ctrls()
        self.seiten = None
        self.__bitmap = None
        self.__zbmp = None
        self.__mouse1 = wx.Point(0,0) #fuer boxdraw
        self.mousepos = None
        self.dc = None
        self.dc_scale = 1.
        self.dc_matrix = wx.AffineMatrix2D()
        self.overlay = wx.Overlay() #zum temp Zeichnen
        #add drop target
        file_drop_target = filedrop.MyFileDropTarget(self)
        self.imagectrl.SetDropTarget(file_drop_target)

    def define_ctrls(self):
        # Haupt-Image-control
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

        #Handler binden
        
        self.imagectrl.Bind(wx.EVT_PAINT, self.OnPaint)
        self.imagectrl.Bind(wx.EVT_LEFT_DOWN, self.OnPressMouse)
        # self.imagectrl.Bind(wx.EVT_LEFT_UP, self.OnReleaseMouse)
        # self.imagectrl.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
        self.imagectrl.Bind(wx.EVT_CHAR_HOOK, self.OnKeyPress)
        self.imagectrl.Bind(wx.EVT_MOTION, self.OnMouseMove)

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

    def rescale(self, faktor):
        cs = self.imagectrl.GetClientSize()
        bildmitte_x = round(cs.x/2)
        bildmitte_y = round(cs.y/2)

        #Alte Bildmitte in Bitmap
        pm_bmp1 = self.get_pos_in_bitmap(wx.Point(bildmitte_x, bildmitte_y))
        mat1, tr1 = self.dc_matrix.Get()

        #Abstand zu tr
        bm_zu_tr_x = bildmitte_x - tr1.x
        bm_zu_tr_y = bildmitte_y - tr1.y

        self.dc_matrix.Scale(faktor, faktor)
        mat2, tr2 = self.dc_matrix.Get()

        # Abstand wird mit skaliert => rückgängig machen
        bm_zu_tr_x *= (1-faktor)
        bm_zu_tr_y *= (1-faktor)
        self.dc_matrix.Set(mat2,(tr1.x + bm_zu_tr_x, tr1.y + bm_zu_tr_y))

        self.overlay.Reset()
        self.imagectrl.Refresh()
        wx.Yield()
        return

    def translate(self, richtung):
        delta = 25
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
        
    # ------------------------------------------------------
    # Event handling
    # ------------------------------------------------------
        
    def OnPaint(self, event=None):
        self.overlay.Reset()
        dc = wx.PaintDC(self.imagectrl)
        self.dc = dc
        erg = dc.SetTransformMatrix(self.dc_matrix)
        dc.SetBackground(wx.Brush("light blue"))
        dc.Clear()
        if self.__bitmap:
            dc.DrawBitmap ( self.__bitmap, 0, 0, useMask=False)
        if self.__zbmp:
            dc.DrawBitmap ( self.__zbmp, 0, 0, useMask=True)

    def OnPressMouse(self, event):
        act_pos = event.GetPosition()
        self.MausKlickAktionen(act_pos)
        
    def OnMouseMove(self, evt):
        act_pos = evt.GetPosition()
        if self.seiten.status == 'Start Seite/Foto':
            self.maus_zeigt_fadenkreuz(act_pos)
        elif self.seiten.status == 'Rahmen ru':
            # if evt.Dragging() and evt.LeftIsDown():
            self.maus_zeigt_rahmen(act_pos)
        elif self.seiten.status in ('Ecke1', 'Ecke2', 'Ecke3'):
            self.maus_zeigt_fadenkreuz(act_pos)

    def OnKeyPress(self, event):
        act_pos = event.GetPosition()
        keycode = event.GetKeyCode()
        # print(keycode)
        # conf.mainframe.SetStatusText(str(keycode))
        
        if keycode == 388:  #num+
            if event.GetModifiers() == wx.MOD_CONTROL:
                if self.seiten.status == 'Foto Kontrolle':
                    self.seiten.foto_beschneiden('+')
            else:
                self.rescale(2.)
        if keycode == 390:  #num-
            if event.GetModifiers() == wx.MOD_CONTROL:
                if self.seiten.status == 'Foto Kontrolle':
                    self.seiten.foto_beschneiden('-')
            else:
                self.rescale(.5)

        if keycode == 314: #links
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.translate('l')
            else:
                self.imagectrl.WarpPointer(act_pos.x-1, act_pos.y)
        if keycode == 316: #rechts
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.translate('r')
            else:
                self.imagectrl.WarpPointer(act_pos.x+1, act_pos.y)
        if keycode == 315: #hoch
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.translate('h')
            else:
                self.imagectrl.WarpPointer(act_pos.x, act_pos.y-1)
        if keycode == 317: #tief
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.translate('t')
            else:
                self.imagectrl.WarpPointer(act_pos.x, act_pos.y+1)

        if keycode == 82: #'r'
            self.seiten.akt_seite.seite_drehen()

        if keycode == 83: #'s'
            if event.GetModifiers() == wx.MOD_CONTROL:
                p = self.get_pos_in_bitmap(act_pos)
                self.seiten.foto_neu_beschneiden(mauspos=p)
            else:
                self.seiten.akt_seite.seite_speichern()

        if keycode == 69: #'e'
            p = self.get_pos_in_bitmap(act_pos)
            self.seiten.foto_entfernen(p)

        if keycode == 27: #'esc'
            self.seiten.reset()

        if keycode == wx.WXK_SPACE:
            # print("you pressed the spacebar!")
            self.MausKlickAktionen(act_pos)
        # event.Skip()

    # ------------------------------------------------------
    # High-Level Funktionen
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Basis Funktionen
    # ------------------------------------------------------

    def MausKlickAktionen(self, act_pos):
        p = self.get_pos_in_bitmap(act_pos)
        if self.seiten.status == 'Start Seite/Foto':
            self.__mouse1 = act_pos
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

    def maus_zeigt_fadenkreuz(self, pos):

        if not self.dc:
            return
        dc=self.dc
        # # dc.Clear()
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
        odc = wx.DCOverlay(self.overlay, dc)
        odc.Clear()
        dc.SetPen(wx.Pen("red", 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        x1, y1 = self.__mouse1
        x2, y2 = pos
        dc.DrawRectangle(x1, y1, x2-x1, y2-y1)
        del odc # work around a bug in the Python wrappers to make
                # sure the odc is destroyed before the dc is.

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
