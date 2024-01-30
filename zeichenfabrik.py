import logging

import wx

import config as conf

logger = logging.getLogger('album')

dc = None #device context
zbmp = None #Zeichenbitmap

def zeichne_rahmen(image_bmp, akt_seite):
    __prepare_dc(image_bmp)
    for foto in akt_seite.fotos:
        p4 = wx.Point(foto.ecke1.x, foto.ecke3.y)
        punkte = [foto.ecke1, foto.ecke2, foto.ecke3, foto.ecke1, p4, foto.ecke3]
        dc.DrawPolygon(punkte)
        dc.DrawLine(p4, foto.ecke2)
    __release_dc()

def zeichne_ecke(image_bmp, linie_hor=None, linie_vert=None):
    __prepare_dc(image_bmp)
    dc.SetPen(wx.Pen(wx.RED, 3))
    if linie_hor:
        dc.DrawLine(0, linie_hor, 1600, linie_hor)
    if linie_vert:
        dc.DrawLine(linie_vert, 0, linie_vert, 1600)
    __release_dc()

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
