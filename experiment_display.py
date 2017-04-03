# -*- coding: utf-8 -*-
"""
@brief experiment_display

This program is free software under the GNU General Public License
(>=v2). Read the file COPYING that comes with GRASS for details.

@author: Anna Petrasova (akratoc@ncsu.edu)
"""

import numpy as np
from collections import deque

import wx

class DisplayFrame(wx.Frame):
    def __init__(self, parent, fontsize, average, maximum, title, formatting_string):
        wx.Frame.__init__(self, parent, style=wx.NO_BORDER)
        # TODO add title
        self.maximum = maximum
        self.formatting_string = formatting_string
        self.label = wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL)
        self.gauge = wx.Gauge(self, range=maximum, style=wx.GA_VERTICAL)
        self.gauge.SetBackgroundColour(wx.WHITE)
        font = wx.Font(fontsize, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.label.SetFont(font)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.gauge, 1, wx.ALL|wx.EXPAND, border=5)
        self.sizer.Add(self.label, 0, wx.ALL|wx.ALIGN_CENTER|wx.GROW, border=10)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

        self.values = deque(maxlen=average)

    def show_value(self, value):
        if value is None:
            self.label.SetLabel('')
            self.gauge.SetValue(0)
            return
        self.values.append(value)
        mean = np.mean(np.array(self.values))
        self.label.SetLabel(self.formatting_string.format(int(mean)))
        if mean > self.maximum:
            mean = self.maximum
        self.gauge.SetValue(mean)
        self.sizer.Layout()
        self.Layout()


class MultipleDisplayFrame(wx.Frame):
    def __init__(self, parent, fontsize, average, maximum, title, formatting_string):
        wx.Frame.__init__(self, parent, style=wx.NO_BORDER)
        # TODO: average not used yet here

        # maximum, title and formatting_string are lists
        self.list_maximum = maximum
        self.list_title = title
        self.list_formatting_string = formatting_string
        self.labels = []
        self.titles = []
        self.gauges = []
        self.sizer = wx.GridBagSizer(5, 5)
        for i in range(len(self.list_title)):
            self.titles.append(wx.StaticText(self, label=self.list_title[i], style=wx.ALIGN_CENTRE))
            self.labels.append(wx.StaticText(self, style=wx.ALIGN_CENTRE_HORIZONTAL))
            self.gauges.append(wx.Gauge(self, range=self.list_maximum[i], style=wx.GA_VERTICAL))
            self.gauges[i].SetBackgroundColour(wx.WHITE)
            font = wx.Font(fontsize, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            self.labels[i].SetFont(font)
            self.titles[i].SetFont(font)
            self.sizer.Add(self.titles[i], pos=(0, i), flag=wx.ALL|wx.ALIGN_CENTER)
            self.sizer.Add(self.gauges[i], pos=(1, i), flag=wx.ALL|wx.EXPAND)
            self.sizer.Add(self.labels[i], pos=(2, i), flag=wx.ALL|wx.ALIGN_CENTER)
            self.sizer.AddGrowableCol(i, 0)
        self.sizer.AddGrowableRow(1)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def show_value(self, values):
        if len(self.gauges) != len(values):
            print 'wrong number of values!'
            return
        for i in range(len(self.gauges)):
            if values[i] is None:
                self.labels[i].SetLabel('')
                self.gauges[i].SetValue(0)
                continue

            self.labels[i].SetLabel(self.list_formatting_string[i].format(values[i]))
            if values[i] > self.list_maximum[i]:
                values[i] = self.list_maximum[i]
            self.gauges[i].SetValue(values[i])
        self.sizer.Layout()
        self.Layout()


if __name__ == "__main__":
    app = wx.App()
    if True:
        fr = MultipleDisplayFrame(parent=None, fontsize=20, list_maximum=[200, 100, 20],
                                  list_title=['T 1', 'T 2', 'T 3'], list_formatting_string=['{}', '{}', '{}'])
        fr.SetPosition((700, 200))
        fr.SetSize((500, 200))
        fr.show_values([50, 20, 10])
    else:
        fr = DisplayFrame(None, 20, 3, 100)
        fr.SetPosition((2700, 200))
        fr.SetSize((100, 500))
        fr.show_value(50)
    fr.Show()
   
    app.MainLoop()
