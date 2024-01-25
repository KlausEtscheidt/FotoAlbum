# taken from:
# http://webcache.googleusercontent.com/search?q=cache:UzkbJn_xaRwJ:https://www.daniweb.com/software-development/python/code/216581/wxpython-gui-to-display-a-jpeg-jpg-image+&cd=1&hl=en&ct=clnk
# show a jpeg (.jpg) image using wxPython, newer coding style
# two different ways to load and display are given
# tested with Python24 and wxPython25   vegaseat   24 jul 2005
import wx
# import  cStringIO

mypic = r'C:\Users\Etscheidt\Pictures\IMG-20230126-WA0001.jpg'    

class Panel1(wx.Panel):
    """ class Panel1 creates a panel with an image on it, inherits wx.Panel """
    def __init__(self, parent, id):
        # create the panel
        wx.Panel.__init__(self, parent, id)
        
        try:
            jpg1 = wx.Image(mypic, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
            
            # bitmap upper left corner is in the position tuple (x, y) = (5, 5)
            self.imageCtrl = wx.StaticBitmap(self, -1, jpg1, (10 + jpg1.GetWidth(), 5), (jpg1.GetWidth(), jpg1.GetHeight()))

            self.mainSizer = wx.BoxSizer(wx.VERTICAL)
            self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)

            self.SetSizer(self.mainSizer)
            self.mainSizer.Fit(parent)
            self.Layout()

        except IOError:
            print ("Image file %s not found" % mypic)
            raise SystemExit

app = wx.PySimpleApp()

# create a window/frame, no parent, -1 is default ID
# increase the size of the frame for larger images
frame1 = wx.Frame(None, -1, "An image on a panel", size = (400, 300))

# call the derived class
Panel1(frame1,-1)
frame1.Show(1)

app.MainLoop()