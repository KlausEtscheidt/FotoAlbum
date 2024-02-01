import logging

import wx

from config import conf

logger = logging.getLogger('album')

dc = None #device context
zbmp = None #Zeichenbitmap

# Alle folgenden Bitmaps dienen als transparente Overlays über das Originalbild
# ------------------------------------------------------------------------------
#
#

# Durchkreuzter Rahmen über die gewählten Ecken aller definierten Fotos der Seite
def zeichne_rahmen(image_bmp, akt_seite):
    __prepare_dc(image_bmp)
    for foto in akt_seite.fotos:
        p4 = wx.Point(foto.ecke1.x, foto.ecke3.y)
        punkte = [foto.ecke1, foto.ecke2, foto.ecke3, foto.ecke1, p4, foto.ecke3]
        dc.DrawPolygon(punkte)
        dc.DrawLine(p4, foto.ecke2)
    __release_dc()

# Linie bei Ecke2 und Ecke3 entsprechend der Vorgänger-Ecke
def zeichne_ecke(image_bmp, linie_hor=None, linie_vert=None):
    __prepare_dc(image_bmp)
    dc.SetPen(wx.Pen(wx.RED, 3))
    if linie_hor:
        dc.DrawLine(0, linie_hor, 1600, linie_hor)
    if linie_vert:
        dc.DrawLine(linie_vert, 0, linie_vert, 1600)
    __release_dc()

# Rahmen in gedrehtem Bild entsprechend Ecke1, Breite und Höhe
# zur Korrektur des Clippings einzeichnen
def zeichne_clip_rahmen(image_bmp, foto, rand, rahmen_plus):
    p1 = wx.Point(rand - rahmen_plus, rand - rahmen_plus)
    p2 = wx.Point(p1.x + foto.breite + 2*rahmen_plus, p1.y)
    p3 = wx.Point(p2.x, p1.y + foto.hoehe + 2*rahmen_plus)
    p4 = wx.Point(p1.x, p3.y)
    __prepare_dc(image_bmp)
    dc.SetPen(wx.Pen(wx.RED, 5))
    punkte = [p1, p2, p3, p4]
    dc.DrawPolygon(punkte)
    __release_dc()

# Hier wird ins Bild gezeichnet
# ------------------------------------------------------------------------------
#
def zeichne_clip_rahmen_ins_bild(image_bmp, foto, rand, rahmen_plus):
    p1 = wx.Point(rand - rahmen_plus, rand - rahmen_plus)
    p2 = wx.Point(p1.x + foto.breite + 2*rahmen_plus, p1.y)
    p3 = wx.Point(p2.x, p1.y + foto.hoehe + 2*rahmen_plus)
    p4 = wx.Point(p1.x, p3.y)

    dc = wx.MemoryDC()
    dc.SelectObject(image_bmp)
    dc.SetBrush(wx.TRANSPARENT_BRUSH)
    dc.SetPen(wx.Pen(wx.RED, 5))
    punkte = [p1, p2, p3, p4]
    dc.DrawPolygon(punkte)
    dc.SelectObject(wx.NullBitmap)
    dc = None
    return image_bmp


####################################################################################
# Helper


def __prepare_dc(image_bmp):
    global dc
    global zbmp
    dc = wx.MemoryDC()
    h = image_bmp.Height
    w = image_bmp.Width
    zbmp = wx.Bitmap(w, h)
    
    dc.SelectObject(zbmp)
    dc.SetBackground(wx.Brush('black'))
    dc.SetBrush(wx.TRANSPARENT_BRUSH)
    dc.SetPen(wx.Pen(wx.RED, 15))
    dc.Clear

def __release_dc():
    global dc
    global zbmp
    dc.SelectObject(wx.NullBitmap)
    zbmp.SetMaskColour('black')
    dc = None
