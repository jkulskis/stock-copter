from PySide2 import QtCore, QtGui, QtWidgets
from forms.StockViewerDialogUI import Ui_StockViewerDialog
from util.stock import Stock
from util.format import Formatter
import pyqtgraph as pg
import numpy as np

class StockViewerDialog(QtWidgets.QDialog):

    def __init__(self, stock):
        super(StockViewerDialog, self).__init__()
        self.ui = Ui_StockViewerDialog()
        self.ui.setupUi(self)
        self.ui.graphicsView.enableAutoRange()
        self.stock = stock
        self.ui.labelTicker.setText(self.stock.ticker)
        self.stock_variables = []
        self.populate_table()
        self.ui.tableWidget.resizeColumnsToContents()
        self.update_graph()
        self.historical_data = {'timestamp': [], 'price_data': {}, 'timeframe': None, 'interval': None}
        self.ui.comboBox.currentIndexChanged.connect(self.update_graph)
    
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
        print(timeframe)
        self.historical_data = self.stock.update_historical(timeframe=timeframe, return_data=True)
        if self.historical_data is not None: # if invalid time range, will return none
            x = []
            y = []
            for ii in range(len(self.historical_data['timestamp'])):
                if self.historical_data['price_data']['close'][ii] is not None:
                    x.append(self.historical_data['timestamp'][ii])
                    y.append(self.historical_data['price_data']['close'][ii])
            self.ui.graphicsView.plot(np.asarray(x), np.asarray(y), title='Price data: {}'.format(self.ui.comboBox.currentText()), pen='g', clear=True)

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


        

