"""
mainframe_evts.py
=====================================================
Definiert das Event handling für den mainframe.
Zur besseren Übersichtlichkeit hierhin ausgelagert.
"""
import wx

class EvtHandler():

    def __init__(self, parent):
        self.p = parent

    def OnNextBtn(self, _):
        self.p.seiten.seite_bearbeiten_next()

    def OnPrevBtn(self, _):
        self.p.seiten.seite_bearbeiten_prev()

    def OnThreadResult(self, event):
        if event.had_err:
            wx.MessageBox(f'{event.data}','Fehler beim Speichern')
        else:
            # Process results here
            self.p.SetStatusText(f'{event.data}')
        
    def OnPaint(self, event=None):
        self.p.overlay.Reset()
        dc = wx.PaintDC(self.p.imagectrl)
        self.p.dc = dc
        erg = dc.SetTransformMatrix(self.p.dc_matrix)
        dc.SetBackground(wx.Brush("light blue"))
        dc.Clear()
        if self.p.bitmap:
            dc.DrawBitmap ( self.p.bitmap, 0, 0, useMask=False)
        if self.p.zbmp:
            dc.DrawBitmap ( self.p.zbmp, 0, 0, useMask=True)

    def OnPressMouse(self, event):
        act_pos = event.GetPosition()
        self.p.MausKlickAktionen(act_pos)
        
    def OnMouseMove(self, evt):
        act_pos = evt.GetPosition()
        if self.p.seiten.status == 'Start Seite/Foto':
            self.maus_zeigt_fadenkreuz(act_pos)
        elif self.p.seiten.status == 'Rahmen ru':
            # if evt.Dragging() and evt.LeftIsDown():
            self.maus_zeigt_rahmen(act_pos)
        elif self.p.seiten.status in ('Ecke1', 'Ecke2', 'Ecke3'):
            self.maus_zeigt_fadenkreuz(act_pos)

    def OnKeyPress(self, event):
        act_pos = event.GetPosition()
        keycode = event.GetKeyCode()
        # print(keycode)
        # conf.mainframe.SetStatusText(str(keycode))
        
        if keycode == 388:  #num+
            if event.GetModifiers() == wx.MOD_CONTROL:
                if self.p.seiten.status == 'Foto Kontrolle':
                    self.p.seiten.foto_beschneiden('+')
            else:
                self.p.rescale(2.)
        if keycode == 390:  #num-
            if event.GetModifiers() == wx.MOD_CONTROL:
                if self.p.seiten.status == 'Foto Kontrolle':
                    self.p.seiten.foto_beschneiden('-')
            else:
                self.p.rescale(.5)

        if keycode == 314: #links
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.p.translate('l')
            else:
                self.p.imagectrl.WarpPointer(act_pos.x-1, act_pos.y)
        if keycode == 316: #rechts
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.p.translate('r')
            else:
                self.p.imagectrl.WarpPointer(act_pos.x+1, act_pos.y)
        if keycode == 315: #hoch
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.p.translate('h')
            else:
                self.p.imagectrl.WarpPointer(act_pos.x, act_pos.y-1)
        if keycode == 317: #tief
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.p.translate('t')
            else:
                self.p.imagectrl.WarpPointer(act_pos.x, act_pos.y+1)

        if keycode == 82: #'r'
            self.p.seiten.akt_seite.seite_drehen()

        if keycode == 83: #'s'
            if event.GetModifiers() == wx.MOD_CONTROL:
                p = self.p.get_pos_in_bitmap(act_pos)
                self.p.seiten.foto_neu_beschneiden(mauspos=p)
            else:
                self.p.seiten.akt_seite.seite_speichern()

        if keycode == 69: #'e'
            p = self.p.get_pos_in_bitmap(act_pos)
            self.p.seiten.foto_entfernen(p)

        if keycode == 27: #'esc'
            self.p.seiten.reset()

        if keycode == wx.WXK_SPACE:
            # print("you pressed the spacebar!")
            self.p.MausKlickAktionen(act_pos)
        # event.Skip()


    def maus_zeigt_fadenkreuz(self, pos):

        if not self.p.dc:
            return
        # dc=self.dc
        # # dc.Clear()
        dc = wx.ClientDC(self.p.imagectrl)
        odc = wx.DCOverlay(self.p.overlay, dc)
        odc.Clear()
        dc.SetPen(wx.Pen("red", 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.CrossHair(pos.x, pos.y)
        del odc # work around a bug in the Python wrappers to make
                # sure the odc is destroyed before the dc is.

    def maus_zeigt_rahmen(self, pos):
        if not self.p.dc:
            return
        # dc=self.dc
        # dc.Clear()
        dc = wx.ClientDC(self.p.imagectrl)
        odc = wx.DCOverlay(self.p.overlay, dc)
        odc.Clear()
        dc.SetPen(wx.Pen("red", 1))
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        x1, y1 = self.p.mausanker_rechteck
        x2, y2 = pos
        dc.DrawRectangle(x1, y1, x2-x1, y2-y1)
        del odc # work around a bug in the Python wrappers to make
                # sure the odc is destroyed before the dc is.
