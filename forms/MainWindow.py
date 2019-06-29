from util.config import conf
from PySide2 import QtWidgets, QtCore, QtGui
from util.stock import Stock
from forms.MainWindowUI import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.stocks = [Stock(ticker=ticker, **conf['stocks'][ticker]) for ticker in conf['stocks']]
        self.populate_tree_view()
        self.ui.treeWidget.expandAll()
    
    def closeEvent(self, event):
        conf.dump_settings(self.stocks) # dump settings before quitting
    
    def populate_tree_view(self):
        portfolio_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        portfolio_tree.setText(0, 'Portfolio')
        watch_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        watch_tree.setText(0, 'Watchlist')
        for stock in self.stocks:
            if stock.group == 'Portfolio':
                QtWidgets.QTreeWidgetItem(portfolio_tree).setText(0, stock.ticker)
            if stock.group == 'Watchlist':
                QtWidgets.QTreeWidgetItem(watch_tree).setText(0, stock.ticker)