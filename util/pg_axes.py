#############################################################################
# Slighly modified by me from https://gist.github.com/cpascual/cdcead6c166e63de2981bc23f5840a98
#
# This file was adapted from Taurus TEP17, but all taurus dependencies were 
# removed so that it works with just pyqtgraph
#
# Just run it and play with the zoom to see how the labels and tick positions 
# automatically adapt to the shown range
#
#############################################################################
# http://taurus-scada.org
#
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
#
# Taurus is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Taurus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

__all__ = ["DateAxisItem"]

import numpy
from pyqtgraph import AxisItem
from util.format import Formatter
from datetime import datetime, timedelta
from time import mktime, localtime

class PriceAxisItem(AxisItem):
    def __init__(self, *args, **kwargs):
        AxisItem.__init__(self, *args, **kwargs)
        self._oldAxis = None

    def tickStrings(self, values, scale, spacing):
        """Reimplemented from PlotItem to format as price with custom formatter"""
        ret = []
        for x in values:
            ret.append('${}'.format(Formatter.format_number(x, string=True, no_scientific=True)))
        return ret
    
    def attachToPlotItem(self, plotItem):
        """Add this axis to the given PlotItem
        :param plotItem: (PlotItem)
        """
        self.setParentItem(plotItem)
        viewBox = plotItem.getViewBox()
        self.linkToView(viewBox)
        self._oldAxis = plotItem.axes[self.orientation]['item']
        self._oldAxis.hide()
        plotItem.axes[self.orientation]['item'] = self
        pos = plotItem.axes[self.orientation]['pos']
        plotItem.layout.addItem(self, *pos)
        self.setZValue(-1000)

class DateAxisItem(AxisItem):
    """
    A tool that provides a date-time aware axis. It is implemented as an
    AxisItem that interpretes positions as unix timestamps (i.e. seconds
    since 1970).
    The labels and the tick positions are dynamically adjusted depending
    on the range.
    It provides a  :meth:`attachToPlotItem` method to add it to a given
    PlotItem
    """
    
    # Max width in pixels reserved for each label in axis
    _pxLabelWidth = 80

    def __init__(self, *args, **kwargs):
        AxisItem.__init__(self, *args, **kwargs)
        self._oldAxis = None
        self.time_padding = []
        self.timestamps = []

    def set_times(self, timestamps, time_padding):
        self.timestamps = timestamps
        self.time_padding = time_padding

    def tickValues(self, minVal, maxVal, size):
        """
        Reimplemented from PlotItem to adjust to the range and to force
        the ticks at "round" positions in the context of time units instead of
        rounding in a decimal base
        """
        maxMajSteps = int(size/self._pxLabelWidth)
        dt1 = datetime.fromtimestamp(minVal)
        dt2 = datetime.fromtimestamp(maxVal)
        dx = maxVal - minVal
        majticks = []

        if dx > 63072001:  # 3600s*24*(365+366) = 2 years (count leap year)
            d = timedelta(days=366)
            for y in range(dt1.year + 1, dt2.year):
                dt = datetime(year=y, month=1, day=1)
                majticks.append(mktime(dt.timetuple()))
        elif dx > 5270400:  # 3600s*24*61 = 61 days
            d = timedelta(days=31)
            dt = dt1.replace(day=1, hour=0, minute=0,
                             second=0, microsecond=0) + d
            while dt < dt2:
                # make sure that we are on day 1 (even if always sum 31 days)
                dt = dt.replace(day=1)
                majticks.append(mktime(dt.timetuple()))
                dt += d
        elif dx > 172800:  # 3600s24*2 = 2 days
            d = timedelta(days=1)
            dt = dt1.replace(hour=0, minute=0, second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d
        elif dx > 7200:  # 3600s*2 = 2hours
            d = timedelta(hours=1)
            dt = dt1.replace(minute=0, second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d
        elif dx > 1200:  # 60s*20 = 20 minutes
            d = timedelta(minutes=10)
            dt = dt1.replace(minute=(dt1.minute // 10) * 10,
                             second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d
        elif dx > 120:  # 60s*2 = 2 minutes
            d = timedelta(minutes=1)
            dt = dt1.replace(second=0, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d
        elif dx > 20:  # 20s
            d = timedelta(seconds=10)
            dt = dt1.replace(second=(dt1.second // 10) * 10, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d
        elif dx >= 1:  # 2s
            d = timedelta(seconds=1)
            dt = dt1.replace(second=(dt1.second // 1) * 1, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d
        elif dx >= 0.001:
            d = timedelta(milliseconds=1)
            dt = dt1.replace(second=(dt1.second // 1) * 1, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d
        else:
            d = timedelta(microseconds=1)
            dt = dt1.replace(second=(dt1.second // 1) * 1, microsecond=0) + d
            while dt < dt2:
                majticks.append(mktime(dt.timetuple()))
                dt += d
        L = len(majticks)
        if L > maxMajSteps:
            majticks = majticks[::int(numpy.ceil(float(L) / maxMajSteps))]
        return [(d.total_seconds(), majticks)]

    def tickStrings(self, values, scale, spacing):
        """Reimplemented from PlotItem to adjust to the range"""
        ret = []
        if not values:
            return []
        if spacing < 1:
            fmt = "%H:%S.%f"
        elif spacing < timedelta(hours=0.5).total_seconds():
            fmt = "%b/%d-%H:%S"
        elif spacing < timedelta(days=1).total_seconds():
            fmt = "%b/%d-%H:%M"
        elif spacing < timedelta(days=31).total_seconds():
            fmt = "%b/%d"
        elif spacing < timedelta(days=366).total_seconds():
            fmt = "%Y %b"
        else:
            fmt = "%Y"
        ii = 0
        for ti in range(len(self.timestamps)):
            if ii == len(values):
                break
            elif self.timestamps[ti] >= values[ii]:
                for jj in range(ii, len(values)):
                    if self.timestamps[ti] >= values[jj]:
                        values[ii] += self.time_padding[ti]
                        ii += 1
                    else:
                        break
        if ii < len(values):
            for jj in range(ii, len(values)):
                values[ii] += self.time_padding[-1]
        for x in values:
            try:
                t = datetime.fromtimestamp(x)
                if spacing < 0.000001:
                    ret.append(t.strftime(fmt))
                elif spacing < 0.001:
                    ret.append(t.strftime(fmt))[:-3]
                else:
                    ret.append(t.strftime(fmt))
            except ValueError:  # Windows can't handle dates before 1970
                ret.append('')             
            except TypeError: # if striftime returns None
                return []
        return ret

    def attachToPlotItem(self, plotItem):
        """Add this axis to the given PlotItem
        :param plotItem: (PlotItem)
        """
        self.setParentItem(plotItem)
        viewBox = plotItem.getViewBox()
        self.linkToView(viewBox)
        self._oldAxis = plotItem.axes[self.orientation]['item']
        self._oldAxis.hide()
        plotItem.axes[self.orientation]['item'] = self
        pos = plotItem.axes[self.orientation]['pos']
        plotItem.layout.addItem(self, *pos)
        self.setZValue(-1000)

    def detachFromPlotItem(self):
        """Remove this axis from its attached PlotItem
        (not yet implemented)
        """
        raise NotImplementedError()  # TODO