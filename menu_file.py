import wx
# import subprocess

import config as conf
# import seite

# Menu-Items zum Menu erzeugen und Handler registrieren
def init(parent, pMenu):
    # The "\t..." syntax defines an accelerator key that also triggers the same event
    men_items = (
        # (OnRefillTree, "Baum erneuern", "Baum neu lesen"),
        (OnStart, "Start", "Starte Bearbeitung aller Bilder."),
        (OnResetLog, "Lösche Logpanel", "Logpanel leeren"),
        # (OnEdit, "Öffne RawTherapee", "Öffne RawTherapee"),
        (OnExit, "Ende", "Programm beenden"),
    )
    for mItem in men_items:
        m = pMenu.Append(-1, mItem[1], mItem[2])
        parent.Bind(wx.EVT_MENU, mItem[0], m)

def OnStart(_event):
    #Tiff dateien suchen
    conf.imagepanel.ablauf.dateiliste_erstellen()
    #Erste Seite bearbeiten
    conf.imagepanel.ablauf.seite_bearbeiten(0)

def OnResetLog(_event):
    conf.mainframe.logpanel.Clear()

# #Öffne mit Rawtherapee
# def OnEdit(_event):
#     subprocess.Popen(config.editor)


## File-Menu Programm Ende
def OnExit(_event):
    """Close the frame, terminating the application."""
    conf.mainframe.Close(True)
