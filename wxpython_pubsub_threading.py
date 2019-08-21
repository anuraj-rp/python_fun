"""
 Original Source: https://www.blog.pythonlibrary.org/2010/05/22/wxpython-and-threads/
 Created (dd.mm.yyyy): 21.08.2019
 Modified to work with pypubsub instead of wx.lib.pubsub
 Author: Anuraj R.

"""

import wx
import time
from threading import Thread
from pubsub import pub


class TestThread(Thread):
    """
    Test Worker Thread Class
    """

    def __init__(self):
        """ Init Worker Thread class"""
        super().__init__()
        self.start()

    def run(self):
        """ Run the worker Thread """
        for i in range(5):
            time.sleep(1)
            wx.CallAfter(self.postTime, i)
        time.sleep(2)
        wx.CallAfter(pub.sendMessage, "update", message="Thread Finished")

    def postTime(self, amt):
        """
        Send time to Gui
        :param amt: the current time to send
        :return: nothing
        """
        amtOfTime = amt + 1
        pub.sendMessage("update", message=amtOfTime)


class MyFrame(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title="WxPython PubSub Threading")
        panel = wx.Panel(self)
        #add a panel so that looks same on all platforms
        # panel = wx.Panel(self, wx.ID_ANY)
        self.displayLbl = wx.StaticText(panel, label="Amount of time since thread started")
        self.btn = wx.Button(panel, label="Start Thread")
        self.btn.Bind(wx.EVT_BUTTON, self.onButtonClick)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.displayLbl, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)

        pub.subscribe(self.updateDisplay, "update")
        self.Show()

    def onButtonClick(self, event):
        """ Runs the thread """
        TestThread()
        self.displayLbl.SetLabel("Thread Started!")
        self.btn.Disable()
        print("click")

    def updateDisplay(self, message):
        """ Receives data from thread and updates the display """
        t = message
        if isinstance(t, int):
            self.displayLbl.SetLabel("time since thread started: %s seconds" %t)
        else:
            self.displayLbl.SetLabel("%s" % t)
            self.btn.Enable()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()
