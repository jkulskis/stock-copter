from util.config import Config
from PySide2 import QtWidgets, QtCore, QtGui
from util.stock import Stock
from forms.MainWindowUI import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, config=None):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conf = config
        self.populate_tree_view()
        self.ui.treeWidget.expandAll()
    
    def closeEvent(self, event):
        self.conf.dump_settings() # dump settings before quitting
    
    def populate_tree_view(self):
        portfolio_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        portfolio_tree.setText(0, 'Portfolio')
        watch_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        watch_tree.setText(0, 'Watchlist')
        for stock in self.conf.stocks:
            if stock.group == 'Portfolio':
                QtWidgets.QTreeWidgetItem(portfolio_tree).setText(0, stock.ticker)
            if stock.group == 'Watchlist':
                QtWidgets.QTreeWidgetItem(watch_tree).setText(0, stock.ticker)