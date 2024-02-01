import wx

class xx(wx.Frame):
    def __init__(self, width, height):
        wx.Frame.__init__(self, None,
                          style = wx.STAY_ON_TOP |
                          wx.FRAME_NO_TASKBAR |
                          wx.FRAME_SHAPED,
                          size=(width, height))
        #self.SetTransparent(180)
        self.Show(True)
        b = wx.EmptyBitmap(width, height)
        dc = wx.MemoryDC()
        dc.SelectObject(b)
        self.neu()
        dc.SetBackground(wx.Brush('black'))
        self.neu()
        dc.Clear()
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.Pen('red', 4))
        dc.DrawRectangle(10, 10, width-20, height-20)
        self.neu()
        dc.SelectObject(wx.NullBitmap)
        b.SetMaskColour('black')
        self.neu()
        # self.SetShape(wx.RegionFromBitmap(b))
        self.SetShape(wx.Region(b))
        self.neu()

        self.Bind(wx.EVT_KEY_UP, self.OnKeyDown)
        self.SetBackgroundColour('red')
        self.neu()

    def neu(self):
        self.Show(False)
        self.Show(True)
        
    def OnKeyDown(self, event):
        """quit if user press Esc"""
        if event.GetKeyCode() == 27:
            self.Close(force=True)
        else:
            event.Skip()


app = wx.App()
f = xx(300, 300)
app.MainLoop()