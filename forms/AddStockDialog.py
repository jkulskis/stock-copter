from PySide2 import QtCore, QtGui, QtWidgets
from forms.AddStockDialogUI import Ui_AddStockDialog
from util.stock import Stock, Formatter
import requests

class AddStockDialog(QtWidgets.QDialog):

    def __init__(self, stocks, group='Watchlist'):
        super(AddStockDialog, self).__init__()
        self.ui = Ui_AddStockDialog()
        self.stocks = stocks
        self.ui.setupUi(self)
        self.ui.labelError.hide()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        if group == 'Watchlist':
            self.ui.radioButtonWatchList.setChecked(True)
        else:
            self.ui.radioButtonPortfolio.setChecked(True)

    def accept(self):
        ticker = self.ui.lineEditTicker.text().upper()
        shares = self.ui.lineEditShares.text() if self.ui.lineEditShares.text() else None
        shares_prices = self.ui.lineEditPrice.text() if self.ui.lineEditPrice.text() else None
        group = 'Watchlist' if self.ui.radioButtonWatchList.isChecked() else 'Portfolio'
        if not ticker:
            self.ui.labelError.setText(Formatter.get_error_text('Error: Invalid Ticker'))
            self.ui.labelError.show()
            return
        for ii in range(len(self.stocks)):
            if self.stocks[ii].ticker == ticker:
                if self.stocks[ii].group == group:     
                    self.ui.labelError.setText(Formatter.get_error_text('Error: Stock already in {0}'.format(group)))
                    self.ui.labelError.show()
                    return
                else:
                    self.stocks[ii] = Stock(ticker=ticker, group=group, shares=shares)
                    super().accept()
                    return
        data = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/{0}?modules=financialData'.format(ticker)).json()
        if data['quoteSummary']['error']:
            self.ui.labelError.setText(Formatter.get_error_text('Error: Invalid Ticker'))
            self.ui.labelError.show()
            return
        else:
            self.stocks += Stock(ticker=ticker, group=group, shares=shares)
            super().accept()
            return

