from PySide2 import QtCore, QtGui, QtWidgets
from forms.StockViewerWidgetUI import Ui_StockViewerWidget
from util.config import conf
from util.stock import Stock
from util.format import Formatter
from util.config import conf
from util.pg_axes import DateAxisItem, PriceAxisItem
from datetime import datetime, timedelta
import pyqtgraph as pg
import numpy as np
# import os, signal
import time
''' line 38 dark theme fix for combobox in ui code
delegate = QtWidgets.QStyledItemDelegate()
self.comboBox = QtWidgets.QComboBox(StockViewerWidget)
self.comboBox.setItemDelegate(delegate)

line 43 dark theme fix for interval combobox in ui code
delegate = QtWidgets.QStyledItemDelegate()
self.comboBoxInterval = QtWidgets.QComboBox(StockViewerWidget)
self.comboBoxInterval.setItemDelegate(delegate)
'''

class StockViewerWidget(QtWidgets.QWidget):

    def __init__(self, stock):
        super(StockViewerWidget, self).__init__()
        if conf['preferences']['theme'] == 'light':
            pg.setConfigOption('background', 'w')
            pg.setConfigOption('foreground', 'k')
            self.draw_line_color = 'k'
        else:
            pg.setConfigOption('background', 'k')
            pg.setConfigOption('foreground', 'd')
            self.draw_line_color = 'd'
        self.ui = Ui_StockViewerWidget()
        self.ui.setupUi(self)
        self.ui.labelGraph.hide()
        self.ui.labelPosition.hide()
        self.ui.graphicsView.enableAutoRange()
        self.clicks = []
        self.axisX = DateAxisItem(orientation='bottom')
        self.axisX.attachToPlotItem(self.ui.graphicsView.getPlotItem())
        self.axisY = PriceAxisItem(orientation='left')
        self.axisY.attachToPlotItem(self.ui.graphicsView.getPlotItem())
        self.last_coords = (None, None)
        self.follow_segment_last_coords = (None, None)
        self.follow_segment = None
        self.line_segments = []
        self.line_draw_mode = False
        self.timestamps = []
        self.time_padding = []
        self.prices = []
        self.stock = stock
        self.setWindowTitle('Stock View of {}'.format(self.stock))
        self.line_threshold_time = 60*10 # update the follow line every 10 minute interval
        self.line_threshold_price = self.stock.attr_num('currentPrice') / 100 # update the follow line every 1/100 of price
        self.follow_timer = QtCore.QTimer()
        self.follow_timer.timeout.connect(self.update_follow_line)
        self.follow_timer.setSingleShot(False)
        self.ui.labelTicker.setText(self.stock.ticker)
        self.stock_variables = []
        self.populate_table()
        self.ui.tableWidget.resizeColumnsToContents()
        self.add_combo_items()
        self.ui.comboBox.setCurrentIndex(12)
        self.ui.comboBoxInterval.setCurrentIndex(0)
        self.last_comboBox_index = 12
        self.last_comboBox_interval_index = 0
        self.update_graph()
        self.historical_data = {'timestamp': [], 'price_data': {}, 'timeframe': None, 'interval': None}
        self.update_actions()
        #signal.signal(signal.SIGSEGV, self.exit_line_draw_mode)

    def update_actions(self):
        self.ui.comboBox.currentIndexChanged.connect(self.update_graph)
        self.ui.comboBoxInterval.currentIndexChanged.connect(self.update_graph)
        self.ui.pushButtonResize.clicked.connect(lambda: self.ui.graphicsView.getPlotItem().enableAutoScale())
        self.ui.pushButtonDrawLine.clicked.connect(lambda: self.draw_line(self.ui.graphicsView.getPlotItem()))
        self.ui.pushButtonReset.clicked.connect(self.reset_graph)
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def reset_graph(self):
        for segment in self.line_segments:
            self.ui.graphicsView.getPlotItem().removeItem(segment)
        self.line_segments = []
        self.clicks = []
        if self.line_draw_mode:
            self.exit_line_draw_mode()
        self.ui.graphicsView.getPlotItem().enableAutoScale()

    def add_combo_items(self):
        self.ui.comboBox.addItem("30 minutes")
        self.ui.comboBox.addItem("1 hour")
        self.ui.comboBox.addItem("3 hours")
        self.ui.comboBox.addItem("6 hours")
        self.ui.comboBox.addItem("12 hours")
        self.ui.comboBox.addItem("1 day")
        self.ui.comboBox.addItem("3 days")
        self.ui.comboBox.addItem("1 week")
        self.ui.comboBox.addItem("2 weeks")
        self.ui.comboBox.addItem("1 month")
        self.ui.comboBox.addItem("3 months")
        self.ui.comboBox.addItem("6 months")
        self.ui.comboBox.addItem("1 year")
        self.ui.comboBox.addItem("3 years")
        self.ui.comboBox.addItem("5 years")
        self.ui.comboBox.addItem("max")
        self.ui.comboBoxInterval.addItem("Default Interval")
        self.ui.comboBoxInterval.addItem("1 minute")
        self.ui.comboBoxInterval.addItem("5 minutes")
        self.ui.comboBoxInterval.addItem("1 day")
        self.ui.comboBoxInterval.addItem("3 months")
    
    def populate_table(self):
        row_num = 0
        self.ui.tableWidget.insertColumn(0)
        self.ui.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Variable'))
        self.ui.tableWidget.insertColumn(1)
        self.ui.tableWidget.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Value'))
        for variable in Stock.get_variables()[0]:
            if variable not in ['ticker', 'group']:
                attr_str = self.stock.attr_str(variable)
                if attr_str:
                    value_widget = QtWidgets.QTableWidgetItem(attr_str)
                    self.ui.tableWidget.insertRow(row_num)
                    variable_widget = QtWidgets.QTableWidgetItem(variable)
                    variable_widget.setFlags(variable_widget.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable ^ QtCore.Qt.ItemFlag.ItemIsSelectable)
                    self.ui.tableWidget.setItem(row_num, 0, variable_widget)
                    value_widget.setFlags(value_widget.flags() ^ QtCore.Qt.ItemFlag.ItemIsEditable ^ QtCore.Qt.ItemFlag.ItemIsSelectable)
                    self.ui.tableWidget.setItem(row_num, 1, value_widget)
                    row_num += 1

    def update_graph(self):
        # TIMEFRAME COMBOBOX
        if self.ui.comboBox.currentIndex() == 0: # 30 minutes
            timeframe = self.get_days('30m')
        elif self.ui.comboBox.currentIndex() == 1: # 1 hour
            timeframe = self.get_days('1h')
        elif self.ui.comboBox.currentIndex() == 2: # 3 hours
            timeframe = self.get_days('3h')
        elif self.ui.comboBox.currentIndex() == 3: # 6 hours
            timeframe = self.get_days('6h')
        elif self.ui.comboBox.currentIndex() == 4: # 12 hours
            timeframe = self.get_days('12h')
        elif self.ui.comboBox.currentIndex() == 5: # 1 day
            timeframe = self.get_days('1d')
        elif self.ui.comboBox.currentIndex() == 6: # 3 days
            timeframe = self.get_days('3d')
        elif self.ui.comboBox.currentIndex() == 7: # 1 week
            timeframe = self.get_days('1w')
        elif self.ui.comboBox.currentIndex() == 8: # 2 weeks
            timeframe = self.get_days('2w')
        elif self.ui.comboBox.currentIndex() == 9: # 1 month
            timeframe = self.get_days('1M')
        elif self.ui.comboBox.currentIndex() == 10: # 3 months
            timeframe = self.get_days('3M')
        elif self.ui.comboBox.currentIndex() == 11: # 6 months
            timeframe = self.get_days('6M')
        elif self.ui.comboBox.currentIndex() == 12: # 1 year
            timeframe = self.get_days('1y')
        elif self.ui.comboBox.currentIndex() == 13: # 3 years
            timeframe = self.get_days('3y')
        elif self.ui.comboBox.currentIndex() == 14: # 5 years
            timeframe = self.get_days('5y')
        elif self.ui.comboBox.currentIndex() == 15: # max
            timeframe = -1
        
        # INTERVAL COMBOBOX
        if self.ui.comboBoxInterval.currentIndex() == 0: # Default Interval
            interval = None
        elif self.ui.comboBoxInterval.currentIndex() == 1: # 1 minute
            interval = '1m'
        elif self.ui.comboBoxInterval.currentIndex() == 2: # 5 minutes
            interval = '5m'
        elif self.ui.comboBoxInterval.currentIndex() == 3: # 1 day
            interval = '1d'
        elif self.ui.comboBoxInterval.currentIndex() == 4: # 3 months
            interval = '3mo'

        self.historical_data = self.stock.update_historical(timeframe=timeframe, interval=interval, return_data=True)
        if self.historical_data is not None: # if invalid time range, will return none
            self.timestamps = []
            self.prices = []
            for ii in range(len(self.historical_data['timestamp'])):
                if self.historical_data['price_data']['close'][ii] is not None:
                    self.timestamps.append(self.historical_data['timestamp'][ii])
                    self.prices.append(self.historical_data['price_data']['close'][ii])
            self.adjust_timeframes() # get rid of large gaps for when trading is not going on
            self.axisX.set_times(timestamps=self.timestamps, time_padding=self.time_padding)
            self.ui.graphicsView.plot(x=self.timestamps, 
                                        y=self.prices, 
                                        title='Price data: {}'.format(self.ui.comboBox.currentText()), 
                                        pen=pg.mkPen(conf['preferences']['graph_settings']['color'], 
                                        width=conf['preferences']['graph_settings']['line_width']), 
                                        clear=True)
            self.ui.graphicsView.getPlotItem().enableAutoScale()
            self.cross_hair(self.ui.graphicsView.getPlotItem())
            self.last_comboBox_index = self.ui.comboBox.currentIndex()
            self.last_comboBox_interval_index = self.ui.comboBoxInterval.currentIndex()
        else:
            self.timer = QtCore.QTimer()
            self.ui.labelGraph.setText(Formatter.get_error_text('No data for this time range + interval combo, defaulting back to the previous choice'))
            self.ui.labelGraph.show()
            self.timer.timeout.connect(self.ui.labelGraph.hide)
            self.timer.setSingleShot(True)
            self.timer.start(5000)
            print('No data for this time range')
            self.ui.comboBox.setCurrentIndex(self.last_comboBox_index)
            self.ui.comboBoxInterval.setCurrentIndex(self.last_comboBox_interval_index)

    def update_follow_line(self):
        if self.follow_segment and self.clicks[0] != self.last_coords: # draw a new follow segment if self.follow_segment == True or if self.follow_segment already exists
            self.ui.graphicsView.getPlotItem().removeItem(self.follow_segment)
            self.follow_segment = pg.LineSegmentROI([self.clicks[0], self.last_coords], pen=pg.mkPen(self.draw_line_color, width=2))
            self.ui.graphicsView.getPlotItem().addItem(self.follow_segment)

    def adjust_timeframes(self):
        new_timestamps = [self.timestamps[0]] # don't pad the first timestamp at all
        self.time_padding = [0]
        threshold_time = 0
        interval = self.historical_data['interval']
        if interval == '1d':
            threshold_time = timedelta(days=2).total_seconds()
            delta_time = timedelta(days=1).total_seconds()
        elif interval == '1m':
            threshold_time = timedelta(hours=1).total_seconds()
            delta_time = timedelta(minutes=1).total_seconds()
        elif interval == '5m':
            threshold_time = timedelta(hours=1).total_seconds()
            delta_time = timedelta(minutes=5).total_seconds()
        if threshold_time:
            for ii in range(1, len(self.timestamps)):
                if self.timestamps[ii] - self.timestamps[ii - 1] > threshold_time:
                    self.time_padding.append(self.time_padding[ii - 1] + self.timestamps[ii] - self.timestamps[ii - 1] - delta_time)
                    new_timestamps.append(self.timestamps[ii] + delta_time - self.time_padding[-1])
                else:
                    new_timestamps.append(self.timestamps[ii] - self.time_padding[ii - 1])
                    self.time_padding.append(self.time_padding[ii - 1]) # if not below the threshold, do not increase the time padding
            self.timestamps = new_timestamps
        else:
            self.time_padding = [0]*len(self.timestamps) # if no threshold, still reset the time padding so that previous paddings do not interfere

    def cross_hair(self, plot_wg):
        # adapted from https://stackoverflow.com/questions/56056453/how-to-make-cross-hair-mouse-tracker-on-a-plotwidget-promoted-in-designer-qt5
        vLine = pg.InfiniteLine(angle=90, movable=False)
        hLine = pg.InfiniteLine(angle=0,  movable=False)
        plot_wg.addItem(vLine, ignoreBounds=True)
        plot_wg.addItem(hLine, ignoreBounds=True)
        vb = plot_wg.getViewBox() 
        def mouseMoved(evt):
            self.ui.labelPosition.show()
            pos = evt[0]  ## using signal proxy turns original arguments into a tuple
            if plot_wg.sceneBoundingRect().contains(pos):
                mousePoint = vb.mapSceneToView(pos)
                self.last_coords = (mousePoint.x(), mousePoint.y())
                padded_time = self.padded_timestamp(self.last_coords[0])
                self.ui.labelPosition.setText('Date = {0}, Price = ${1}'.format(
                    time.strftime('%m-%e-%y %H:%M', time.localtime(padded_time)), Formatter.format_number(mousePoint.y(), string=True)))
                vLine.setPos(self.last_coords[0])
                hLine.setPos(self.last_coords[1])
        plot_wg.getViewBox().setAutoVisible(y=True)
        proxy = pg.SignalProxy(plot_wg.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)    
        plot_wg.proxy = proxy
    
    def draw_line(self, plot_wg):
        # adapted from https://stackoverflow.com/questions/48389140/how-to-register-coordinates-and-draw-a-line
        if self.line_draw_mode:
            self.exit_line_draw_mode()
            return
        def onClick(evt):
            if plot_wg.sceneBoundingRect().contains(evt.pos()):
                if len(self.clicks) == 0:  # First mouse click - ONLY register coordinates
                    print("First click!")
                    self.clicks.append((self.last_coords[0], self.last_coords[1]))
                    self.follow_segment = True # start to draw a segment that follows the mouse
                    self.follow_timer.start(100)
                elif len(self.clicks) == 1:  # Second mouse click - register coordinates of second click
                    self.ui.graphicsView.getPlotItem().removeItem(self.follow_segment) # remove the current follow segment
                    self.follow_segment = False # do not keep drawing the follow segment
                    self.follow_timer.stop()
                    print("Second click...")
                    if self.last_coords[0] == self.clicks[0][0] and self.last_coords[1] == self.clicks[0][1]:
                        self.clicks = [] # don't draw, reset instead, if double click in the same place
                        return
                    self.clicks.append((self.last_coords[0], self.last_coords[1]))
                    print("...drawing line")
                    line = pg.LineSegmentROI(self.clicks, pen=pg.mkPen(self.draw_line_color, width=2)) # Draw line connecting the two self.clicks
                    self.line_segments.append(line) 
                    self.ui.graphicsView.getPlotItem().addItem(line)
                    self.exit_line_draw_mode()
                else:  # something went wrong, just reset self.clicks
                    self.clicks = [] 
        plot_wg.scene().sigMouseClicked.connect(onClick)
        self.line_draw_mode = True
    
    def exit_line_draw_mode(self):
        print('Exiting Line Draw Mode')
        self.ui.graphicsView.getPlotItem().scene().sigMouseClicked.disconnect()
        self.clicks = []
        if self.follow_segment:
            self.ui.graphicsView.getPlotItem().removeItem(self.follow_segment)
            self.follow_segment = False
        self.ui.pushButtonDrawLine.setChecked(False)
        self.line_draw_mode = False

    def padded_timestamp(self, epoch):
        for timestamp in self.timestamps:
            if timestamp >= epoch:
                return epoch + self.time_padding[self.timestamps.index(timestamp)]
        return epoch + self.time_padding[-1]

    def get_days(self, time):
        assert time[-1] in ['m', 'h', 'd', 'w', 'M', 'y']
        if time[-1] == 'm':
            multiplier = 1/60/24
        elif time[-1] == 'h':
            multiplier = 1/24
        elif time[-1] == 'd':
            multiplier = 1
        elif time[-1] == 'w':
            multiplier = 7
        elif time[-1] == 'M':
            multiplier = 30
        elif time[-1] == 'y':
            multiplier = 365 
        return int(time[:-1]) * multiplier
