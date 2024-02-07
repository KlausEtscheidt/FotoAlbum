"""
mainframe_evts.py
=====================================================
Definiert das Event handling für den mainframe.
Zur besseren Übersichtlichkeit hierhin ausgelagert.
"""
import wx

from config import conf

class EvtHandler():
    '''Klasse fürs Event-Handling des mainframes'''

    def __init__(self, parent):
        '''Konstruktor

        Args:
            parent (wx.Window): Vaterklasse des Objekts (hier mainframe)
        '''
        self.p = parent

    def on_next_btn(self, _):
        '''Bearbeite nächste Seite'''
        self.p.seiten.seite_bearbeiten_next()

    def on_prev_btn(self, _):
        '''Bearbeite vorhergehende Seite'''
        self.p.seiten.seite_bearbeiten_prev()

    def on_thread_result(self, event):
        '''Behandelt die Nachrichten aus dem Thread zum Speichern der Bilder'''
        if event.had_err:
            wx.MessageBox(f'{event.data}','Fehler beim Speichern')
        else:
            # Process results here
            self.p.SetStatusText(f'{event.data}')

    def on_paint(self, _event=None):
        '''On-Paint Eventhandler von mainframe.imagectrl.

        Wird durch u.A. durch imagectrl.Refresh() ausgelöst
        und dient zur Darstellung von Bitmaps der gescannten Seiten oder Fotos.
        '''
        self.p.zeichne_alles()

    def on_press_mouse(self, event):
        '''EVT_LEFT_DOWN-Handler von mainframe.imagectrl.

        Der Mausklick wird an *mausklick_aktionen* weitergeleitet,
        welches in Abhängigkeit vom Status des Programms reagiert
        und auch durch Tastatur-Events aktiviert wird.'''
        act_pos = event.GetPosition()
        self.mausklick_aktionen(act_pos)

    def on_mouse_move(self, evt):
        '''EVT_MOTION-Handler von mainframe.imagectrl.

        Je nach Status des Programms wird der Cursor zu einem Fadenkreuz
        bzw. wird mit der Maus ein Rahmen aufgezogen.'''
        act_pos = evt.GetPosition()
        if self.p.seiten.status == 'Start Seite/Foto':
            self.maus_zeigt_fadenkreuz(act_pos)
        elif self.p.seiten.status == 'Rahmen ru':
            # if evt.Dragging() and evt.LeftIsDown():
            self.maus_zeigt_rahmen(act_pos)
        elif self.p.seiten.status in ('Ecke1', 'Ecke2', 'Ecke3'):
            self.maus_zeigt_fadenkreuz(act_pos)

    def on_key_press(self, event):
        '''Tastatur-handler'''
        act_pos = event.GetPosition()
        keycode = event.GetKeyCode()
        # print(keycode)
        # conf.mainframe.SetStatusText(str(keycode))

        if keycode == 388:  #num+
            if event.GetModifiers() == wx.MOD_CONTROL:
                if self.p.seiten.status == 'Foto Kontrolle':
                    self.p.seiten.akt_seite.foto_beschneiden('+')
            else:
                self.p.rescale(2.)
        if keycode == 390:  #num-
            if event.GetModifiers() == wx.MOD_CONTROL:
                if self.p.seiten.status == 'Foto Kontrolle':
                    self.p.seiten.akt_seite.foto_beschneiden('-')
            else:
                self.p.rescale(.5)

        if keycode == 314: #links
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.p.translate('l', conf.delta)
            else:
                self.p.imagectrl.WarpPointer(act_pos.x-1, act_pos.y)
        if keycode == 316: #rechts
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.p.translate('r', conf.delta)
            else:
                self.p.imagectrl.WarpPointer(act_pos.x+1, act_pos.y)
        if keycode == 315: #hoch
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.p.translate('h', conf.delta)
            else:
                self.p.imagectrl.WarpPointer(act_pos.x, act_pos.y-1)
        if keycode == 317: #tief
            if event.GetModifiers() == wx.MOD_CONTROL:
                self.p.translate('t', conf.delta)
            else:
                self.p.imagectrl.WarpPointer(act_pos.x, act_pos.y+1)

        if keycode == 82: #'r'
            self.p.seiten.akt_seite.seite_drehen()

        if keycode == 83: #'s'
            if event.GetModifiers() == wx.MOD_CONTROL:
                pos = self.p.get_pos_in_bitmap(act_pos)
                self.p.seiten.foto_neu_beschneiden(mauspos=pos)
            else:
                self.p.seiten.akt_seite.seite_speichern()

        if keycode == 69: #'e'
            p = self.p.get_pos_in_bitmap(act_pos)
            self.p.seiten.foto_entfernen(p)

        if keycode == 27: #'esc'
            self.p.seiten.reset()

        if keycode == wx.WXK_SPACE:
            # print("you pressed the spacebar!")
            self.mausklick_aktionen(act_pos)
        # event.Skip()


    def mausklick_aktionen(self, act_pos):
        '''Wird durch Klick mit linker Maustaste oder Leertaste ausgelöst'''
        seiten = self.p.seiten
        pos = self.p.get_pos_in_bitmap(act_pos)
        if seiten.status == 'Start Seite/Foto':
            self.p.mausanker_rechteck = act_pos
            seiten.akt_seite.neues_foto_anlegen(pos)
            seiten.status = 'Rahmen ru'

        elif seiten.status == 'Rahmen ru':
            seiten.akt_seite.akt_foto.setze_rahmen_ecke_ru(pos)
            seiten.status = 'Ecke1'
            self.p.label_re.SetLabel(f'   {seiten.status}')
            self.p.zeige_ecke(1)

        elif seiten.status == 'Ecke1':
            seiten.akt_seite.akt_foto.ecke1 = pos
            seiten.status = 'Ecke2'
            self.p.label_re.SetLabel(f'   {seiten.status}')
            self.p.zeige_ecke(2)

        elif seiten.status == 'Ecke2':
            seiten.akt_seite.akt_foto.ecke2 = pos
            seiten.status = 'Ecke3'
            self.p.label_re.SetLabel(f'   {seiten.status}')
            self.p.zeige_ecke(3)

        elif seiten.status == 'Ecke3':
            seiten.akt_seite.akt_foto.ecke3 = pos
            seiten.status = 'Foto Kontrolle'
            msg = f'   {seiten.status} Rahmen: {seiten.akt_seite.akt_foto.rahmen_plus}'
            self.p.label_re.SetLabel(msg)
            seiten.akt_seite.foto_drehen()
            # Hier nach weiter mit keypress + -

        elif seiten.status == 'Foto Kontrolle':
            seiten.akt_seite.foto_speichern()
            seiten.status = 'Foto fertig'
            self.p.label_re.SetLabel('Foto gespeichert')
            seiten.seite_bearbeiten(seiten.id_aktseite)

        # conf.mainframe.SetStatusText(f'n: {self.__mouseclicks} x:{pos.x} y:{pos.y}')
        #logger.debug(f'Mausklick bei x:{p.x} y:{p.y}\n')


    #---------------------------------------------------------------------------
    # Cursor zeichnen
    #---------------------------------------------------------------------------

    def maus_zeigt_fadenkreuz(self, pos):
        '''Zeigt an der Mausposition ein CrossHair-Fadenkreuz über den ganzen Bildschirm'''

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
        '''Zeigt einen Rahmen von der gespeicherten Start-Position **self.p.mausanker_rechteck**
        zur aktuellen Maus-Position'''
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
