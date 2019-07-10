from util.config import conf
from PySide2 import QtWidgets, QtCore, QtGui
from util.stock import Stock
from util.stock_array import StockArray
from util.format import Formatter
from forms.MainWindowUI import Ui_MainWindow
from forms.AddStockDialog import AddStockDialog
from forms.ExpressionCreatorDialog import ExpressionCreatorDialog
from forms.HeaderEditor import HeaderEditorDialog
from threading import Thread
import time

class UpdateThread():

    def __init__(self, stocks, refresh_time, parent):
        self.stocks = stocks
        self.refresh_time = refresh_time
        self.parent = parent
        self.update_times = {'all' : time.time(), 'price' : time.time()}
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(5000)

    def update_ui(self):
        if not self.update_times['all']:
            print('Updating all...')
            self.stocks.update_all()
            self.update_times['all'] = time.time()
            self.update_times['price'] = time.time()
            self.parent.populate_tree_widget()
        else:
            if time.time() - self.update_times['all'] > 60*60*20: # set to 20 minutes for now
                print('Updating all...')
                self.stocks.update_all()
                self.update_times['all'] = time.time()
                self.update_times['price'] = time.time()
                self.parent.populate_tree_widget()
            elif time.time() - self.update_times['price'] > self.refresh_time:
                print('Updating price...')
                self.stocks.update_price()
                self.update_times['price'] = time.time()
                self.parent.populate_tree_widget()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        #---------------------
        #-----Config Data-----
        #---------------------
        if conf['stocks']:
            self.stocks = StockArray([Stock(ticker=ticker, **conf['stocks'][ticker]) for ticker in conf['stocks']])
        else:
            self.stocks = StockArray()
        self.headers = conf['tree_view']['headers']
        #--------------------
        #---Main UI Setup----
        #--------------------
        self.ui = Ui_MainWindow()
        self.portfolio_tree = None
        self.watch_tree = None
        self.headerView = None
        self.stocks.update_all()
        self.reset_ui()
        self.update_thread = UpdateThread(self.stocks, conf['preferences']['refresh_time'], self)
    
    def reset_ui(self):
        self.ui.setupUi(self)
        self.setup_tree_widget()
        self.update_actions()
    
    def setup_tree_widget(self):
        self.setup_header()
        self.portfolio_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.portfolio_tree.setText(0, 'Portfolio')
        self.watch_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.watch_tree.setText(0, 'Watchlist')
        self.setup_header()
        self.populate_tree_widget()

    def setup_header(self):
        self.headerView = QtWidgets.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        self.headerView.setSectionsMovable(True)
        self.headerView.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.headerView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget.setHeader(self.headerView)

    def closeEvent(self, event):
        del self.update_thread
        self.check_headers() # check to see if the header positions were changed by the user before closing
        conf.stocks = self.stocks
        conf.dump_settings() # dump settings before quitting
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape: # may delete later, makes for faster testing though
            self.close()
    
    def update_actions(self):
        self.ui.actionAdd_Stock.triggered.connect(self.add_stock)
        self.ui.actionCreate_Expression.triggered.connect(self.modify_expression)
        self.ui.treeWidget.itemSelectionChanged.connect(self.selection_changed)
        self.ui.treeWidget.customContextMenuRequested.connect(self.treeWidget_context_menu)
        self.headerView.customContextMenuRequested.connect(self.headerView_context_menu)
        self.ui.pushButtonAddStock.clicked.connect(self.add_stock)
        self.ui.pushButtonExpressionCreator.clicked.connect(self.modify_expression)
        self.ui.pushButtonHeaderEditor.clicked.connect(self.open_header_editor)
    
    def check_headers(self):
        column_count = len(self.headers)
        for ii in range(column_count):
            logical_index = self.headerView.logicalIndex(ii)
            if self.headers[logical_index]['text'] != self.ui.treeWidget.headerItem().text(ii):
                for jj in range(ii, len(self.headers)):
                    if self.headers[jj]['text'] == self.ui.treeWidget.headerItem().text(logical_index):
                        self.headers[ii], self.headers[jj] = self.headers[jj], self.headers[ii] # swap them
                        break

    def modify_expression(self, event=None, index=None, policy=None, edit=False, old_conditional=None, old_custom_variable_name=None, old_custom_description=None):
        if policy is None or policy == 'all_fields':
            expression_creator_dialog = ExpressionCreatorDialog(policy='all_fields')
        elif policy == 'edit_header':
            old_expression = self.headers[index]['eq']
            old_header_name = self.headers[index]['text']
            expression_creator_dialog = ExpressionCreatorDialog(policy=policy, old_expression=old_expression, old_header_name=old_header_name)
        else:
            expression_creator_dialog = ExpressionCreatorDialog(policy=policy)
        accepted = expression_creator_dialog.exec_()
        if accepted:
            if not edit and index is not None:
                if index == -1:
                    index = len(self.headers)
                else:
                    index += 1 # any new changes should be applied to the right of whichever header was clicked
            if index is None:
                index = len(self.headers)
            if expression_creator_dialog.header_name:
                new_header = dict.fromkeys(('text', 'eq', 'parsed_eq'))
                new_header['text'] = expression_creator_dialog.header_name
                new_header['eq'] = expression_creator_dialog.expression
                new_header['parsed_eq'] = expression_creator_dialog.parsed_expression
                if edit:
                    self.headers[index] = new_header
                else:
                    self.headers.insert(index, new_header)
            if expression_creator_dialog.custom_variable_name:
                new_variable = dict.fromkeys(('true_casing', 'eq', 'parsed_eq'))
                new_variable['true_casing'] = expression_creator_dialog.custom_variable_name
                new_variable['eq'] = expression_creator_dialog.expression
                new_variable['parsed_eq'] = expression_creator_dialog.parsed_expression
                new_variable['description'] = expression_creator_dialog.custom_variable_description
                if edit:
                    conf['custom_variables'][expression_creator_dialog.old_custom_variable_name.upper()] = new_variable 
                else:
                    conf['custom_variables'].update({expression_creator_dialog.custom_variable.upper() : new_variable})
            if expression_creator_dialog.conditional:
                new_conditional = dict.fromkeys(('eq', 'parsed_eq'))
                new_conditional['eq'] = expression_creator_dialog.conditional
                new_conditional['parsed_eq'] = expression_creator_dialog.parsed_conditional
                if edit:
                    for ii in range(len(self.headers[index]['conditionals'])):
                        if self.headers[index]['conditionals'][ii]['eq'] == expression_creator_dialog.old_conditional:
                            self.headers[index]['conditionals'][ii] = new_conditional
                            break
                else:
                    if 'conditionals' in self.headers[index]:
                        self.headers[index]['conditionals'].append(new_conditional)
                    else:
                        self.headers[index]['conditionals'] = [new_conditional]
            self.populate_tree_widget()

    def open_header_editor(self):
        header_editor_dialog = HeaderEditorDialog(self)
        header_editor_dialog.exec_()

    def selection_changed(self):
        for item in self.ui.treeWidget.selectedItems():
            if not item.parent():
                item.setSelected(False)

    def get_selected(self):
        selected_items = []
        for stock in self.stocks:
            if stock.widget.isSelected():
                selected_items.append({'widget' : stock.widget, 'stock' : stock})
        return selected_items

    def add_stock(self):
        add_stock_dialog = AddStockDialog(self.stocks)
        if add_stock_dialog.exec_():
            self.stocks[-1].update_all()
            self.populate_tree_widget()
    
    def edit_stock(self, stock):
        add_stock_dialog = AddStockDialog(self.stocks, stock)
        if add_stock_dialog.exec_():
            if stock:
                stock.update_shares()
            self.populate_tree_widget()

    def remove_stock(self):
        items = self.get_selected()
        for item in items:
            item['widget'].parent().removeChild(item['widget'])
            self.stocks.remove(item['stock'])

    def clear_tree_view(self):
        root = self.ui.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for ii in range(child_count):
            root.child(ii).takeChildren()

    def treeWidget_context_menu(self, event):
        menu = QtWidgets.QMenu(self.ui.treeWidget)
        remove_stock = QtWidgets.QAction("Remove Stock")
        add_stock = QtWidgets.QAction("Add Stock")
        edit_stock = QtWidgets.QAction("Edit Stock")
        menu.addAction(add_stock)
        selected = self.get_selected()
        if selected:
            menu.addAction(remove_stock)
            if len(selected) == 1:
                menu.addAction(edit_stock)
        action = menu.exec_(QtGui.QCursor.pos())
        if action == remove_stock:
            self.remove_stock()
        elif action == add_stock:
            self.add_stock()
        elif action == edit_stock:
            self.edit_stock(selected[0]['stock'])
    
    def headerView_context_menu(self, event):
        self.ui.treeWidget.clearSelection()
        logical_index = self.headerView.logicalIndexAt(event.x())
        menu = QtWidgets.QMenu(self.headerView)
        add_header = QtWidgets.QAction("Add Header")
        edit_header = QtWidgets.QAction("Edit Header")
        remove_header = QtWidgets.QAction("Remove Header")
        menu.addAction(add_header)
        if logical_index != -1:
            menu.addAction(edit_header)
            if logical_index != 0:
                menu.addAction(remove_header)
        self.check_headers()
        action = menu.exec_(QtGui.QCursor.pos())
        if action == add_header:
            if logical_index == 0:
                logical_index = 1
            self.modify_expression(index=logical_index, policy='add_header')
        elif action == edit_header:
            self.modify_expression(index=logical_index, policy='edit_header', edit=True)
        elif action == remove_header:
            self.remove_header(logical_index)
    
    def remove_header(self, index):
        del self.headers[index]
        self.reset_ui()

    def populate_tree_widget(self):
        self.clear_tree_view()
        for stock in self.stocks:
            if stock.group == 'Portfolio':
                stock.widget = QtWidgets.QTreeWidgetItem(self.portfolio_tree)
            if stock.group == 'Watchlist':
                stock.widget = QtWidgets.QTreeWidgetItem(self.watch_tree)
        for ii in range(len(self.headers)):
            self.ui.treeWidget.headerItem().setText(ii, self.headers[ii]['text'])
        self.ui.treeWidget.expandAll()
        self.update_tree()
    
    def update_tree(self):
        for ii in range(len(self.headers)):
            evaluations = Formatter.evaluate_eq(parsed_eq=self.headers[ii]['parsed_eq'], stocks=self.stocks, string=True)
            self.stocks.populate_widgets(column=ii, evaluations=evaluations)
            if 'conditionals' in self.headers[ii]:
                for conditional in self.headers[ii]['conditionals']:
                    conditional_evaluations = Formatter.evaluate_eq(eq=conditional, stocks=self.stocks, parsed_eq=conditional['parsed_eq'])
                    for jj in range(len(conditional_evaluations)):
                        if conditional_evaluations[jj]:
                            self.stocks[jj].widget.setBackground(ii, self.color(color=conditional_evaluations[jj]))
    
    def color(self, r=255, g=255, b=255, color=None):
        if not color:
            return QtGui.QBrush(QtGui.QColor(r, g, b))
        else:
            if 'RED' in color:
                return QtGui.QBrush(QtGui.QColor(255, 0, 0))
            elif 'GREEN' in color:
                return QtGui.QBrush(QtGui.QColor(0, 255, 0))
            elif 'ORANGE' in color:
                return QtGui.QBrush(QtGui.QColor(255, 155, 0))
            elif 'YELLOW' in color:
                return QtGui.QBrush(QtGui.QColor(255, 255, 0))
            elif 'CYAN' in color:
                return QtGui.QBrush(QtGui.QColor(0, 255, 255))
            elif 'PINK' in color:
                return QtGui.QBrush(QtGui.QColor(255, 192, 203))