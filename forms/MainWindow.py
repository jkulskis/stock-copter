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

    def __init__(self, stocks, parent):
        self.stocks = stocks
        self.parent = parent
        self.update_all_time = time.time()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000*conf['preferences']['refresh_time'])

    def update_ui(self):
        """Updates the UI and stocks. Only updates all the stock properties every 20 minutes
        """
        conf.stocks = self.stocks # update the config stocks...only tickers are stored and there is no reference in conf (to avoid import loops with the Stock class)
        conf.dump_settings() # dump settings every now and then just in case of a crash or forced quit
        if not self.update_all_time:
            self.update_all()
        else:
            if time.time() - self.update_all_time > 60*60*20: # set to 20 minutes for now
                self.update_all()
            else:
                print('Updating price...')
                self.stocks.update_price()
                self.parent.populate_tree_widget()
    
    def update_all(self):
        """Updates all of the stock properties
        """
        print('Updating all...')
        self.stocks.update_all()
        self.update_all_time = time.time()
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
        self.update_thread = UpdateThread(self.stocks, self)
        self.stocks.update_all()
        self.reset_ui()
        self.resize(934, 502)
    
    def reset_ui(self):
        """Resets the UI. 
        
        There were problems with resetting the header view when an object is removed, so this method is called
        when a header item is removed, as well as if core settings are changed.
        """
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
        """Sets up and populates the tree widget that displays all of the stocks.
        """
        self.portfolio_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.portfolio_tree.setText(0, 'Portfolio')
        self.portfolio_tree.setFlags(self.portfolio_tree.flags() ^ QtCore.Qt.ItemIsSelectable)
        self.watch_tree = QtWidgets.QTreeWidgetItem(self.ui.treeWidget)
        self.watch_tree.setText(0, 'Watchlist')
        self.watch_tree.setFlags(self.watch_tree.flags() ^ QtCore.Qt.ItemIsSelectable)
        self.setup_header()
        self.populate_tree_widget()

    def setup_header(self):
        """Sets up a QHeaderView and connects it to the tree widget
        """
        self.headerView = QtWidgets.QHeaderView(QtCore.Qt.Orientation.Horizontal)
        self.headerView.setSectionsMovable(True)
        self.headerView.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.headerView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget.setHeader(self.headerView)
        header_font = QtGui.QFont(conf['preferences']['font']['family'])
        header_font.setPointSize(conf['preferences']['font']['size'])
        self.headerView.setFont(header_font)

    def closeEvent(self, event):
        """Catches the close event so that the config settings can be properly dumped when the program exits.
        
        Arguments:
            event {QEvent} -- Close event of the MainWindow
        """
        self.update_thread.timer.stop() # stop the timer to avoid hang
        del self.update_thread.timer
        self.check_headers() # check to see if the header positions were changed by the user before closing
        conf.stocks = self.stocks # update the config stocks...only tickers are stored and there is no reference in conf (to avoid import loops with the Stock class)
        conf.dump_settings() # dump settings before quitting
    
    # def keyPressEvent(self, event):
    #     """Catches a key press.
        
    #     Arguments:
    #         event {QEvent} -- Key press event of the MainWindow
    #     """
    #     if event.key() == QtCore.Qt.Key_Escape: # may delete later, makes for faster testing though
    #         self.close()
    
    def update_actions(self):
        """Updates all of the actions for the UI
        """
        self.ui.actionAdd_Stock.triggered.connect(self.open_stock_editor)
        self.ui.actionCreate_Expression.triggered.connect(self.modify_expression)
        self.ui.actionEdit_Headers.triggered.connect(self.open_header_editor)
        self.ui.actionPreferences.triggered.connect(self.open_preferences)
        self.ui.actionAbout.triggered.connect(self.show_about)
        self.ui.treeWidget.customContextMenuRequested.connect(self.treeWidget_context_menu)
        self.ui.treeWidget.itemActivated.connect(self.open_stock_view)
        self.headerView.customContextMenuRequested.connect(self.headerView_context_menu)
        self.ui.pushButtonAddStock.clicked.connect(self.open_stock_editor)
        self.ui.pushButtonExpressionCreator.clicked.connect(self.modify_expression)
        self.ui.pushButtonHeaderEditor.clicked.connect(self.open_header_editor)
    
    def show_about(self):
        """Shows an about messagebox
        """
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText('<font size="+2">Created by <a href="https://github.com/jkulskis/" size="+2">@jkulskis</a></font> <td>\
                        <font size="-1">Copyright © 2019 John Mikulskis (GNU GPL)</font>')
        msg_box.setWindowTitle('About')
        msg_box.setTextFormat(QtCore.Qt.RichText)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Close)
        msg_box.exec_()

    def open_preferences(self):
        """Opens the preferences dialog for the user to edit preferences
        """
        preferences_dialog = PreferencesDialog(self.headers)
        if preferences_dialog.exec_():
            self.reset_ui()

    def check_headers(self):
        """Checks the current place of the headers against the config.

        If headers are moved around in the QHeaderView, these changes are not reflected in the config.
        This method will move around the config headers so that everything matches the current state
        of the UI.
        """
        column_count = len(self.headers)
        for ii in range(column_count):
            logical_index = self.headerView.logicalIndex(ii)
            if self.headers[logical_index]['text'] != self.ui.treeWidget.headerItem().text(ii):
                for jj in range(ii, len(self.headers)):
                    if self.headers[jj]['text'] == self.ui.treeWidget.headerItem().text(logical_index):
                        self.headers[ii], self.headers[jj] = self.headers[jj], self.headers[ii] # swap them
                        break

    def modify_expression(self, event=None, index=None, policy='all_fields', edit=False, old_conditional=None, old_custom_variable_name=None, old_custom_description=None):
        """Modifies or Creates expressions by opening up the Expression Creator Dialog, checking the response, and dealing with it accordingly.
        
        Keyword Arguments:
            event {QEvent} -- If an event is attached to the method call (default: {None})
            index {int} -- If a header is being edited or created, this holds the index of the clicked column (default: {None})
            policy {str} --  The type of expression dialog to open. Can be in ['all_fields', 'edit_header', 'add_header', 'conditonal', 'custom'] (default: {all_fields})
            edit {bool} -- If True, an expression is being modified rather than created (default: {False})
            old_conditional {str} -- The old conditional equation, if one is being modified (default: {None})
            old_custom_variable_name {str} -- The old custom variable name, if one is being modified (default: {None})
            old_custom_description {str} -- The old custom variable description, if one is being modified (default: {None})
        """
        if policy == 'all_fields':
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
        """Opens the stock viewer widget to show the graph view and more details of a stock
        """
        selected = self.get_selected()
        if selected: # will be none if portfolio tree or watch tree was double clicked
            stock_viewer_dialog = StockViewerWidget(selected[0]['stock'])
            stock_viewer_dialog.show()

    def open_header_editor(self):
        """Opens the header editor dialog for the user to edit headers and their conditionals
        """
        header_editor_dialog = HeaderEditorDialog(self.headers)
        header_editor_dialog.exec_()
        self.reset_ui()

    def get_selected(self):
        """Gets and returns the selected item's widget and respective stock
        
        Returns:
            [dict] -- {'widget' : stock.widget, 'stock' : stock}
        """
        selected_items = []
        for stock in self.stocks:
            if stock.widget.isSelected():
                selected_items.append({'widget' : stock.widget, 'stock' : stock})
        return selected_items

    def open_stock_editor(self, stock=None):
        """Opens the stock editor dialog to either edit or add a stock
        
        Keyword Arguments:
            stock {Stock} -- The stock to edit, if editing rather than adding (default: {None})
        """
        add_stock_dialog = AddStockDialog(stocks=self.stocks, stock=stock)
        if add_stock_dialog.exec_():
            if stock: # stock is being edited
                stock.update_shares()
                self.populate_tree_widget()
            else: # stock is being added
                self.populate_tree_widget() # populate even if no values for the stock yet so it doesn't seem like it is lagging
                self.stocks[-1].update_all()
                self.populate_tree_widget()

    def remove_stock(self):
        """Removes the selected stock(s) from self.stocks as well as the tree widget
        """
        items = self.get_selected()
        for item in items:
            item['widget'].parent().removeChild(item['widget'])
            self.stocks.remove(item['stock'])

    def clear_tree_widget(self):
        """clears the tree widget
        """
        root = self.ui.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        for ii in range(child_count):
            root.child(ii).takeChildren()

    def treeWidget_context_menu(self, event):
        """Handles the treeWidget custom context menu
        
        Arguments:
            event {QEvent} -- The event passed in by the click of the context menu
        """
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
            self.open_stock_editor()
        elif action == edit_stock:
            self.open_stock_editor(stock=selected[0]['stock'])
    
    def headerView_context_menu(self, event):
        """Handles the headerView custom context menu
        
        Arguments:
            event {QEvent} -- The event passed in by the click of the context menu
        """
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
        """removes a header from the headerView and resets the UI
        
        Arguments:
            index {int} -- The index of the headerView column to remove
        """
        del self.headers[index]
        self.reset_ui()

    def populate_tree_widget(self):
        """Populates the tree widget with the stocks under their respective groups (Watchlist, Portfolio)
        """
        self.clear_tree_widget()
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
        """Updates the tree widget.

        The main expressions and conditionals for each header are evaluated for the stocks, and the tree widget is 
        populated with the resulting evaluations
        """
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
                            self.stocks[jj].widget.setForeground(ii, self.color(color='Black'))
    
    def color(self, r=0, g=0, b=0, color=None):
        """Returns a QBrush with the specified color. Evaluates RGB color if the color parameter is not specified
        
        Keyword Arguments:
            r {int} -- Red value of the RGB triplet (default: {0})
            g {int} -- Green value of the RGB triplet (default: {0})
            b {int} -- Blue value of the RGB triplet (default: {0})
            color {str} -- string that contains one of the supported colors (default: {None})
        
        Returns:
            [type] -- [description]
        """
        if not color:
            return QtGui.QBrush(QtGui.QColor(r, g, b))
        else:
            color = color.upper()
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