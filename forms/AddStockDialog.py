from PySide2 import QtCore, QtGui, QtWidgets
from forms.AddStockDialogUI import Ui_Dialog
from util.stock import Stock
import requests

class AddStockDialog(QtWidgets.QDialog):

    def __init__(self, stocks):
        super(AddStockDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.stocks = stocks
        self.ui.setupUi(self)
        self.ui.labelError.hide()
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.stock = None

    def accept(self):
        ticker = self.ui.lineEditTicker.text().upper()
        shares = self.ui.lineEditShares.text() if self.ui.lineEditShares.text() else None
        price = self.ui.lineEditPrice.text() if self.ui.lineEditPrice.text() else None
        group = 'Watchlist' if self.ui.radioButtonWatchList.isChecked() else 'Portfolio'
        if not ticker:
            self.ui.labelError.setText(self.get_color_text('Error: Invalid Ticker'))
            self.ui.labelError.show()
            return
        for ii in range(len(self.stocks)):
            if self.stocks[ii].ticker == ticker:
                if self.stocks[ii].group == group:     
                    self.ui.labelError.setText(self.get_color_text('Error: Stock already in {0}'.format(group)))
                    self.ui.labelError.show()
                    return
                else:
                    self.stocks[ii] = Stock(ticker=ticker, group=group, shares=shares)
                    super().accept()
                    return
        data = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/{0}?modules=financialData'.format(ticker)).json()
        if data['quoteSummary']['error']:
            self.ui.labelError.setText(self.get_color_text('Error: Invalid Ticker'))
            self.ui.labelError.show()
            return
        else:
            self.stocks += Stock(ticker=ticker, group=group, shares=shares)
            super().accept()
            return
    
    def get_color_text(self, text):
        return "<html><head/><body><p><span style=\" color:#ff0000;\">{0}</span></p></body></html>".format(text)

