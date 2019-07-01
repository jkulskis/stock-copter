from util.config import conf
from PySide2 import Qt, QtWidgets, QtCore, QtGui
from util.stock import Stock
from util.stock_array import StockArray
from util.stock import Formatter
from forms.MainWindowUI import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #---------------------
        #-----Config Data-----
        #---------------------
        self.headers = conf.headers
        self.stocks = StockArray([Stock(ticker=ticker, **conf['stocks'][ticker]) for ticker in conf['stocks']])
        #--------------------
        #------UI Setup------
        #--------------------
        self.headerItem = self.ui.treeWidget.headerItem()
        self.portfolio_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.portfolio_tree.setText(0, 'Portfolio')
        self.watch_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.watch_tree.setText(0, 'Watchlist')
        self.populate_tree_view()
        self.ui.treeWidget.expandAll()
    
    def closeEvent(self, event):
        conf.stocks = self.stocks
        conf.dump_settings() # dump settings before quitting
    
    def populate_tree_view(self):
        for stock in self.stocks:
            if stock.group == 'Portfolio':
                stock.widget = QtWidgets.QTreeWidgetItem(self.portfolio_tree)
            if stock.group == 'Watchlist':
                stock.widget = QtWidgets.QTreeWidgetItem(self.watch_tree)
        for ii in range(len(self.headers)):
            self.headerItem.setText(ii, self.headers[ii]['text'])
        self.update_tree()
    
    def update_tree(self):
        self.stocks.update_price()
        # self.headerItem.columnCount()
        for ii in range(len(self.headers)):
            for stock in self.stocks:
                stock.widget.setText(ii, Formatter.evaluate_eq(self.headers[ii]['eq'], stock=stock, string=True))
        # self.ui.treeWidget.headerItem().setText(1, "Price")
        # print(self.ui.treeWidget.headerItem().getText(1))
        # print (stock.widget.setText)
