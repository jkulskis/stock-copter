from util.config import conf
from PySide2 import Qt, QtWidgets, QtCore, QtGui
from util.stock import Stock
from util.stock_array import StockArray
from util.stock import Formatter
from forms.MainWindowUI import Ui_MainWindow
from forms.AddStockDialog import AddStockDialog

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #---------------------
        #-----Config Data-----
        #---------------------
        self.headers = conf.headers
        if conf['stocks']:
            self.stocks = StockArray([Stock(ticker=ticker, **conf['stocks'][ticker]) for ticker in conf['stocks']])
        else:
            self.stocks = StockArray()
        #---------------------
        #----Other Dialogs----
        #---------------------
        
        #--------------------
        #---Main UI Setup----
        #--------------------
        self.headerItem = self.ui.treeWidget.headerItem()
        self.portfolio_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.portfolio_tree.setText(0, 'Portfolio')
        self.watch_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.watch_tree.setText(0, 'Watchlist')
        self.populate_tree_view()
        self.ui.treeWidget.expandAll()
        self.update_actions()
    
    def closeEvent(self, event):
        conf.stocks = self.stocks
        conf.dump_settings() # dump settings before quitting
    
    def update_actions(self):
        self.ui.actionAdd_Stock.triggered.connect(self.add_stock)
    
    def add_stock(self):
        add_stock_dialog = AddStockDialog(self.stocks)
        if add_stock_dialog.exec_():
            self.populate_tree_view()

    def clear_tree_view(self):
        root = self.ui.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for ii in range(child_count):
            root.child(ii).takeChildren()

    def populate_tree_view(self):
        self.clear_tree_view()
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
            evaluations = Formatter.evaluate_eq(self.headers[ii]['eq'], stocks=self.stocks, string=True)
            if isinstance(evaluations, str):
                evaluations = [evaluations]
            self.stocks.populate_widgets(column=ii, evaluations=evaluations) 
            #self.stocks[0].widget.setBackground(0, self.color(color='RED'))
    
    def color(self, r=255, g=255, b=255, color=None):
        if not color:
            return QtGui.QBrush(QtGui.QColor(r, g, b))
        else:
            if color == 'RED':
                return QtGui.QBrush(QtGui.QColor(255, 0, 0))
