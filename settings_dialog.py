'''
settings_dialog.py
=============================
Dialog zum Abfragen der Einstellungen des Programms
'''

import wx

#from config import conf

class SettingsDlg(wx.Dialog): # pylint: disable=too-many-ancestors
    '''Dialog'''

    def __init__(self, parent, titel, conf):
        '''
        Erfragt Einstellungen vom Benutzer

        Speichert die abgefragten Werte im conf-Objekt

        Args:
            parent (window): Vater-Fenster
            titel (str): Titel
            conf (Config): Konfigurations-Objekt, welches die Werte aufnimmt
        '''
        size = (500, 400)
        style = wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.DEFAULT_DIALOG_STYLE
        super().__init__(parent=parent, size=size, title=titel, style=style)
        self.BackgroundColour = (200, 230, 250) # pylint: disable=invalid-name

        self.conf = conf

        # Platzhalter für die aus dem Dialog ermittelten Werte
        self.min_winkel = conf.min_winkel
        self.rahmen_plus = conf.rahmen_plus
        self.pic_output = conf.pic_output
        self.scale_seite = conf.scale_seite
        self.scale_kontrollbild = conf.scale_kontrollbild

        #Panel für das Innere des Formulars (Inhalt ohne Buttons)
        self.pnl = wx.Panel(self)

        #Sizer für Gesamt-Formular anlegen
        vbox = wx.BoxSizer(wx.VERTICAL)
        #Sizer für das Innere des Panels (Inhalt ohne Buttons)
        self.vbox_inner = wx.BoxSizer(wx.VERTICAL)

        #Sizer für Panel zuteilen
        self.pnl.SetSizer(self.vbox_inner)

        #Buttons horiz. nebeneinander anlegen
        buttonbox = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(self, wx.ID_OK, label='Ok')
        self.ok_button = ok_button
        close_button = wx.Button(self, wx.ID_CANCEL, label='Abbruch')
        ok_button.BackgroundColour = (200, 230, 250)
        close_button.BackgroundColour = (200, 230, 250)
        buttonbox.Add(ok_button)
        buttonbox.Add(close_button, flag=wx.LEFT, border=5)

        #Definiere das Innere (Muss überschrieben werden)
        self.inner()

        #Panel und Buttons zum Dialog
        vbox.Add(self.pnl, proportion=1, flag=wx.ALL|wx.EXPAND, border=10)
        vbox.Add(buttonbox, flag=wx.ALIGN_CENTER|wx.BOTTOM, border=10)

        #Sizer für Gesamt-Dialog zuteilen
        self.SetSizer(vbox)

        #Events für OK- und Abbruch-Button
        #okButton.Bind(wx.EVT_BUTTON, self.OnOK)
        close_button.Bind(wx.EVT_BUTTON, self.OnCancel)

    ##Panel mit Leben füllen
    def inner(self):
        '''Definiert die widgets im Inneren (self.pnl) des Dialogs'''
        conf = self.conf
        label = wx.StaticText(self.pnl, label='Unterverzeichnis zur Ausgabe: ')
        ctrl = wx.TextCtrl(self.pnl, value=conf.pic_output, size=(120, 20))
        self.vbox_inner.Add(label, flag=wx.LEFT|wx.TOP, border=5)
        self.vbox_inner.Add(ctrl, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
        self.pic_output_ctrl = ctrl

        label = wx.StaticText(self.pnl, label='Maßstab zur Anzeige der kompletten Seite: ')
        ctrl = wx.TextCtrl(self.pnl, value=str(conf.scale_seite), size=(40, 20))
        self.vbox_inner.Add(label, flag=wx.LEFT|wx.TOP, border=5)
        self.vbox_inner.Add(ctrl, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
        self.scale_seite_ctrl = ctrl

        label = wx.StaticText(self.pnl, label='Maßstab zur finalen Kontrollanzeige: ')
        ctrl = wx.TextCtrl(self.pnl, value=str(conf.scale_kontrollbild), size=(40, 20))
        self.vbox_inner.Add(label, flag=wx.LEFT|wx.TOP, border=5)
        self.vbox_inner.Add(ctrl, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
        self.scale_kontrollbild_ctrl = ctrl

        label_txt ='minimaler Winkel, ab dem ein Bild zurück gedreht wird: '
        label = wx.StaticText(self.pnl, label=label_txt)
        ctrl = wx.TextCtrl(self.pnl, value=str(conf.min_winkel), size=(40, 20))
        self.vbox_inner.Add(label, flag=wx.LEFT|wx.TOP, border=5)
        self.vbox_inner.Add(ctrl, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
        self.min_winkel_ctrl = ctrl

        label = wx.StaticText(self.pnl, label='Definierter Fotorahmen wird um Wert vergrößert: ')
        ctrl = wx.TextCtrl(self.pnl, value=str(conf.rahmen_plus), size=(40, 20))
        self.vbox_inner.Add(label, flag=wx.LEFT|wx.TOP, border=5)
        self.vbox_inner.Add(ctrl, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=5)
        self.rahmen_plus_ctrl = ctrl

    def Validate(self): # pylint: disable=invalid-name
        '''Prüft die Eingaben.

        Wird vom Ok-Button des Standarddialogs aufgerufen.
        Dialog schließ erst, wenn alle Werte i.O. (return True)'''

        try:
            self.scale_seite = float(self.scale_seite_ctrl.GetValue())
            self.scale_kontrollbild = float(self.scale_kontrollbild_ctrl.GetValue())
            self.min_winkel = float(self.min_winkel_ctrl.GetValue())
        except ValueError:
            wx.MessageBox("Nur float für Maßstab und Winkel erlaubt")
            return False

        try:
            self.rahmen_plus = int(self.rahmen_plus_ctrl.GetValue())
        except ValueError:
            wx.MessageBox("Nur int für Fotorahmen-Änderung erlaubt")
            return False

        self.pic_output = self.pic_output_ctrl.GetValue()
        return True

    def OnCancel(self, _e): # pylint: disable=invalid-name
        '''Wird bei Abbruch aufgerufen. Schließt Dialog und liefert wx.ID_CANCEL'''
        self.EndModal(wx.ID_CANCEL)
