from util.config import conf
from PySide2 import QtWidgets, QtCore, QtGui
from util.stock import Stock
from util.stock_array import StockArray
from util.format import Formatter
from forms.MainWindowUI import Ui_MainWindow
from forms.AddStockDialog import AddStockDialog
from forms.ExpressionCreatorDialog import ExpressionCreatorDialog

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #---------------------
        #-----Config Data-----
        #---------------------
        self.headers = conf['tree_view']['headers']
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
        self.portfolio_tree = None
        self.watch_tree = None
        self.headerView = None
        self.setup_tree_widget()
        self.update_actions()

    def setup_tree_widget(self):
        self.setup_header()
        self.portfolio_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.portfolio_tree.setText(0, 'Portfolio')
        self.watch_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.watch_tree.setText(0, 'Watchlist')
        self.setup_header()
        self.populate_tree_view()
    
    def reset_ui(self):
        self.ui.setupUi(self)
        self.setup_tree_widget()
        self.update_actions()

    def setup_header(self):
        self.headerView = QtWidgets.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        self.headerView.setSectionsMovable(True)
        self.headerView.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.headerView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget.setHeader(self.headerView)

    def closeEvent(self, event):
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
            if index is None:
                index = len(self.headers) - 1
            if expression_creator_dialog.header_name:
                new_header = dict.fromkeys(('text', 'eq', 'parsed_eq'))
                new_header['text'] = expression_creator_dialog.header_name
                new_header['eq'] = expression_creator_dialog.expression
                new_header['parsed_eq'] = expression_creator_dialog.parsed_expression
                if edit:
                    self.headers[index] = new_header
                else:
                    if index == len(self.headers) - 1:
                        self.headers.append(new_header)
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
                if 'conditionals' in self.headers[index]:
                    self.headers[index]['conditionals'].append(new_conditional)
                else:
                    self.headers[index]['conditionals'] = [new_conditional]
            self.populate_tree_view()

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
            self.populate_tree_view()

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
        menu.addAction(add_stock)
        if self.get_selected():
            menu.addAction(remove_stock)
        action = menu.exec_(QtGui.QCursor.pos())
        if action == remove_stock:
            self.remove_stock()
        elif action == add_stock:
            self.add_stock()
    
    def headerView_context_menu(self, event):
        self.ui.treeWidget.clearSelection()
        logical_index = self.headerView.logicalIndexAt(event.x())
        if logical_index == -1:
            return
        menu = QtWidgets.QMenu(self.headerView)
        add_header = QtWidgets.QAction("Add Header")
        edit_header = QtWidgets.QAction("Edit Header")
        remove_header = QtWidgets.QAction("Remove Header")
        menu.addAction(add_header)
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
        #self.populate_tree_view()

    def populate_tree_view(self):
        # self.ui.treeWidget.headerItem() = QtWidgets.QTreeWidgetItem
        self.clear_tree_view()
        for stock in self.stocks:
            if stock.group == 'Portfolio':
                stock.widget = QtWidgets.QTreeWidgetItem(self.portfolio_tree)
            if stock.group == 'Watchlist':
                stock.widget = QtWidgets.QTreeWidgetItem(self.watch_tree)
        for ii in range(len(self.headers)):
            # if ii != 0: # don't center for the first column
            #     for stock in self.stocks:
            #         stock.widget.setTextAlignment(ii, QtCore.Qt.AlignHCenter)
            self.ui.treeWidget.headerItem().setText(ii, self.headers[ii]['text'])
        self.ui.treeWidget.expandAll()
        self.update_tree()
    
    def update_tree(self):
        #self.stocks.update_all()
        #self.stocks.update_price()
        for ii in range(len(self.headers)):
            evaluations = Formatter.evaluate_eq(parsed_eq=self.headers[ii]['parsed_eq'], stocks=self.stocks, string=True)
            self.stocks.populate_widgets(column=ii, evaluations=evaluations)
            if 'conditionals' in self.headers[ii]:
                for conditional in self.headers[ii]['conditionals']:
                    conditional_evaluations = Formatter.evaluate_eq(eq=conditional, stocks=self.stocks, parsed_eq=conditional['parsed_eq'])
                    print(conditional_evaluations)
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
                

