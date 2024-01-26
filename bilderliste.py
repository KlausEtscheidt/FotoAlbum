import glob 
import os
import logging

import wx

import config as conf

logger = logging.getLogger('album')

#######################################################################################
#
class Bild():
    def __init__(self, fullpath2pic):
        self.fullpath2pic = fullpath2pic
        self.path, self.picname = os.path.split(self.fullpath2pic)
        self.basename, self.typ = os.path.splitext(self.picname)
        self.__image = None
        # self.__bitmap = None

    def scaled_bitmap(self, faktor):
        myimage = self.image
        new_w = int(myimage.Width * faktor)
        new_h = int(myimage.Height * faktor)
        new_image = myimage.Scale(new_w, new_h)
        logger.debug(f'\nnew size: br {new_w} h: {new_h}\n')
        return new_image.ConvertToBitmap()

    def crop(self, pos1, pos2, faktor):
        logger.debug(f'crop x1 {pos1.x} y1 {pos1.y} x2 { pos2.x} y2 { pos2.y}')
        w = pos2.x - pos1.x
        h = pos2.y - pos1.y
        size = wx.Size(w,h)
        pkt = wx.Point(-pos1.x, -pos1.y)
        new_image = self.image.Resize(size, pkt)
        new_w = int(new_image.Width * faktor)
        new_h = int(new_image.Height * faktor)
        new_image = new_image.Scale(new_w, new_h)
        return new_image.ConvertToBitmap()


    @property
    def image(self):
        if not self.__image: 
            self.__image = wx.Image(self.fullpath2pic, wx.BITMAP_TYPE_ANY)
        return self.__image

    @image.setter
    def image(self, x):
        self.__image = x

#######################################################################################
#
class BilderListe(list):
    def __init__(self, srcPath, src_type):
        super().__init__()
        myFileList=[]
        # self.Liste=[]

        # Suche Bilder    
        myFileList = glob.glob(srcPath + "\*" + src_type)
        
        #Fuer jeden gefundenen Pfad, Bildobjekt erzeugen und merken
        for fullpath in myFileList:
            mBild = Bild(fullpath)
            self.append (mBild)
