from util.config import conf
from PySide2 import QtWidgets, QtCore, QtGui
from util.stock import Stock
from util.stock_array import StockArray
from util.format import Formatter
from forms.MainWindowUI import Ui_MainWindow
from forms.AddStockDialog import AddStockDialog
from forms.ExpressionCreatorDialog import ExpressionCreatorDialog
from forms.HeaderEditor import HeaderEditorDialog
from forms.StockViewerWidget import StockViewerWidget
from forms.PreferencesDialog import PreferencesDialog
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
    
    def update_all(self):
        print('Updating all...')
        self.stocks.update_all()
        self.update_times['all'] = time.time()
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
        self.update_thread = UpdateThread(self.stocks, conf['preferences']['refresh_time'], self)
        self.stocks.update_all()
        self.reset_ui()
    
    def reset_ui(self):
        self.ui.setupUi(self)
        label_font = QtGui.QFont(conf['preferences']['font']['family'])
        label_font.setPointSize(13)
        self.setup_tree_widget()
        self.ui.labelTitle.setFont(label_font)
        tree_font = QtGui.QFont(conf['preferences']['font']['family'])
        tree_font.setPointSize(conf['preferences']['font']['size'])
        self.ui.treeWidget.setFont(tree_font)
        self.update_actions()
    
    def setup_tree_widget(self):
        self.portfolio_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.portfolio_tree.setText(0, 'Portfolio')
        self.portfolio_tree.setFlags(self.portfolio_tree.flags() ^ QtCore.Qt.ItemIsSelectable)
        self.watch_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.watch_tree.setText(0, 'Watchlist')
        self.watch_tree.setFlags(self.watch_tree.flags() ^ QtCore.Qt.ItemIsSelectable)
        self.setup_header()
        self.populate_tree_widget()

    def setup_header(self):
        self.headerView = QtWidgets.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        self.headerView.setSectionsMovable(True)
        self.headerView.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.headerView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget.setHeader(self.headerView)
        header_font = QtGui.QFont(conf['preferences']['font']['family'])
        header_font.setPointSize(conf['preferences']['font']['size'])
        self.headerView.setFont(header_font)

    def closeEvent(self, event):
        self.update_thread.timer.stop() # stop the timer to avoid hang
        self.check_headers() # check to see if the header positions were changed by the user before closing
        conf.stocks = self.stocks # update the config stocks...only tickers are stored and there is no reference in conf (to avoid import loops with the Stock class)
        conf.dump_settings() # dump settings before quitting
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape: # may delete later, makes for faster testing though
            self.close()
    
    def update_actions(self):
        self.ui.actionAdd_Stock.triggered.connect(self.add_stock)
        self.ui.actionCreate_Expression.triggered.connect(self.modify_expression)
        self.ui.actionEdit_Headers.triggered.connect(self.open_header_editor)
        self.ui.actionPreferences.triggered.connect(self.open_preferences)
        self.ui.actionAbout.triggered.connect(self.show_about)
        self.ui.treeWidget.customContextMenuRequested.connect(self.treeWidget_context_menu)
        self.ui.treeWidget.itemActivated.connect(self.open_stock_view)
        self.headerView.customContextMenuRequested.connect(self.headerView_context_menu)
        self.ui.pushButtonAddStock.clicked.connect(self.add_stock)
        self.ui.pushButtonExpressionCreator.clicked.connect(self.modify_expression)
        self.ui.pushButtonHeaderEditor.clicked.connect(self.open_header_editor)
    
    def show_about(self):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText('<font size="+2">Created by <a href="https://github.com/jkulskis/" size="+2">@jkulskis</a></font> <td>\
                        <font size="-1">Copyright © 2019 John Mikulskis under the MIT license</font>')
        msg_box.setWindowTitle('About')
        msg_box.setTextFormat(QtCore.Qt.RichText)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Close)
        msg_box.exec_()

    def open_preferences(self):
        preferences_dialog = PreferencesDialog(self.headers)
        if preferences_dialog.exec_():
            self.reset_ui()

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

    def open_stock_view(self):
        selected = self.get_selected()
        if selected: # will be none if portfolio tree or watch tree was double clicked
            stock_viewer_dialog = StockViewerWidget(selected[0]['stock'])
            stock_viewer_dialog.show()

    def open_header_editor(self):
        header_editor_dialog = HeaderEditorDialog(self.headers)
        header_editor_dialog.exec_()
        self.reset_ui()

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
            self.update_thread.update_all()
    
    def edit_stock(self, stock):
        add_stock_dialog = AddStockDialog(self.stocks, stock)
        if add_stock_dialog.exec_():
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
                already_applied = [False]*len(self.stocks)
                for conditional in self.headers[ii]['conditionals']:
                    conditional_evaluations = Formatter.evaluate_eq(eq=conditional, stocks=self.stocks, parsed_eq=conditional['parsed_eq'])
                    for jj in range(len(conditional_evaluations)):
                        if conditional_evaluations[jj] and not already_applied[jj]: # apply the first conditional that is not None
                            already_applied[jj] = True
                            self.stocks[jj].widget.setBackground(ii, self.color(color=conditional_evaluations[jj]))
                            self.stocks[jj].widget.setForeground(ii, self.color(color='BLACK'))
    
    def color(self, r=0, g=0, b=0, color=None):
        if not color:
            return QtGui.QBrush(QtGui.QColor(r, g, b))
        else:
            if 'BLACK' in color:
                return QtGui.QBrush(QtGui.QColor(0, 0, 0))
            elif 'RED' in color:
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