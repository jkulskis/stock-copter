from PySide2 import QtCore, QtGui, QtWidgets
from forms.AddStockDialogUI import Ui_AddStockDialog
from util.stock import Stock, Formatter
import requests
import ast

class AddStockDialog(QtWidgets.QDialog):

    def __init__(self, stocks, stock=None, group='Watchlist'):
        super(AddStockDialog, self).__init__()
        self.ui = Ui_AddStockDialog()
        self.ui.setupUi(self)
        self.group = group
        self.stocks = stocks
        if stock:
            self.group = stock.group
            self.ui.lineEditTicker.setText(stock.ticker)
            self.ui.lineEditShares.setText(str(stock.shares).replace('[', '').replace(']', ''))
            self.ui.lineEditPrices.setText(str(stock.sharesPrices).replace('[', '').replace(']', ''))
        if self.group == 'Watchlist':
            self.ui.radioButtonWatchList.setChecked(True)
        else:
            self.ui.radioButtonPortfolio.setChecked(True)
        self.stock = stock
        self.ui.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.ui.labelError.hide()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.update_line_edits()
        self.ui.radioButtonWatchList.toggled.connect(self.update_line_edits)
        if stock:
            self.ui.lineEditTicker.setReadOnly(True)
    
    def update_line_edits(self):
        if self.ui.radioButtonPortfolio.isChecked():
            self.ui.lineEditShares.show()
            self.ui.lineEditPrices.show()
            self.ui.labelPrices.show()
            self.ui.labelShares.show()
            self.group = 'Portfolio'
        else:
            if self.stock and self.stock.shares:
                self.ui.lineEditShares.setText(str(self.stock.shares)[1:-1]) # use 1:-1 so that the list brackes will not be included
                self.ui.lineEditPrices.setText(str(self.stock.sharesPrices)[1:-1])
            else:
                self.ui.lineEditShares.setText('')
                self.ui.lineEditPrices.setText('')
            self.ui.lineEditShares.hide()
            self.ui.lineEditPrices.hide()
            self.ui.labelPrices.hide()
            self.ui.labelShares.hide()
            self.group = 'Watchlist'

    def accept(self):
        ticker = self.ui.lineEditTicker.text().upper()
        shares = self.ui.lineEditShares.text() if self.ui.lineEditShares.text() else None
        shares_prices = self.ui.lineEditPrices.text() if self.ui.lineEditPrices.text() else None
        group = self.group
        if not ticker:
            self.ui.labelError.setText(Formatter.get_error_text('Error: Invalid Ticker'))
            self.ui.labelError.show()
            return
        if not self.stock:
            for ii in range(len(self.stocks)):
                if self.stocks[ii].ticker == ticker:
                    self.ui.labelError.setText(Formatter.get_error_text('Error: Stock already in {0}'.format(self.stocks[ii].group)))
                    self.ui.labelError.show()
                    return
            data = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/{0}?modules=financialData'.format(ticker)).json()
            if data['quoteSummary']['error']:
                self.ui.labelError.setText(Formatter.get_error_text('Error: Invalid Ticker'))
                self.ui.labelError.show()
                return
        if group == 'Watchlist':
            if self.stock:
                self.stock.group = group
                self.stock.shares = None
                self.stock.sharesPrices = None
                self.stock.totalShares = 0
                self.stock.averageSharePrice = 0
                self.stock.profit = None
            else:
                self.stocks += Stock(ticker=ticker)
            super().accept()
        if not shares:
            self.ui.labelError.setText(Formatter.get_error_text('Error: Shares not specified'))
            self.ui.labelError.show()
            return
        else:
            try:
                shares = [float(share) for share in ast.literal_eval('[{}]'.format(shares))]
                shares_prices = [float(share_price) for share_price in ast.literal_eval('[{}]'.format(shares_prices.replace('$', '')))]
                assert(len(shares) == len(shares_prices))
            except ValueError:
                self.ui.labelError.setText(Formatter.get_error_text('Error: Invalid shares and/or prices'))
                self.ui.labelError.show()
                return
            except AssertionError:
                self.ui.labelError.setText(Formatter.get_error_text('Error: num shares != num prices'))
                self.ui.labelError.show()
                return
        if self.stock:
            self.stock.group = group
            self.stock.shares = shares
            self.stock.sharesPrices = shares_prices
        else:
            self.stocks += Stock(ticker=ticker, group=group, shares=shares, sharesPrices=shares_prices)
        super().accept()
