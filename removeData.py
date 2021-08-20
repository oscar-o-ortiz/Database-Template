import sys
import sqlite3

from PyQt5.uic import loadUi
from tableModel import TableModel
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableView,
    QDialog,
    QWidget
)
    
class RemoveDataWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("removeDataWindow.ui", self)
        
        # Connects to database
        connection = sqlite3.connect("inventory.db")
        cur = connection.cursor()
        cur.execute("SELECT * FROM Inventory ORDER BY Part_Num")
        data = cur.fetchall()

        # Uses TableModel class with QAbstractTableModel subclass to create model
        self.model = TableModel(data)

        # Creating filter for model
        filter_proxy_model = QSortFilterProxyModel()
        filter_proxy_model.setSourceModel(self.model)
        filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model.setFilterKeyColumn(1)
        
        filter_proxy_model_brand = QSortFilterProxyModel()
        filter_proxy_model_brand.setSourceModel(filter_proxy_model)
        filter_proxy_model_brand.setFilterCaseSensitivity(Qt.CaseInsensitive)
        filter_proxy_model_brand.setFilterKeyColumn(2)       
        
        # Setting up tableView
        self.tableView.setModel(filter_proxy_model_brand)
        
        # Setting up the filter on the lineEdit widget
        self.lineEdit_searchBar.textChanged.connect(filter_proxy_model.setFilterRegExp)
        self.lineEdit_searchBar_2.textChanged.connect(filter_proxy_model_brand.setFilterRegExp)
        
        # Displaying chosen data from tableview into lineEdit widgets
        self.tableView.clicked.connect(self.tableClicked)
        
        self.tableView.setHorizontalHeaderLabels(["Part #", "Sheen", "Brand", "Package", "Color/Base", "Units", "Description", "Vendor", "Location"])

        
    def tableClicked(self, cur):
        # Connects to database
        connection = sqlite3.connect("inventory.db")
        cur = connection.cursor()
        
        rows = sorted(set(index.row() for index in self.tableView.selectedIndexes()))
        print(rows)
        
        cur.execute("SELECT * FROM Inventory ORDER BY Part_Num LIMIT " + str(rows[0]) + ", 1")
        
        data = cur.fetchall()
        print(data)
        self.lineEdit_searchBar.setText(data[0][1])
        
    # Add data to the sqlite3 database using client input
    def removeData(self, data): 
        # Read data from the QTextEdit widgets
        newPart = self.partEdit.toPlainText()
        newSheen = self.sheenEdit.toPlainText()
        newBrand = self.brandEdit.toPlainText()
        newPackage = self.packageEdit.toPlainText()
        newColor = self.colorEdit.toPlainText()
        newUnits = self.unitsEdit.toPlainText()
        newVendor = self.vendorEdit.toPlainText()
        newLocation = self.locationEdit.toPlainText()
        newDescription = self.descriptionEdit.toPlainText()
        
        data = (newPart, newSheen, newBrand, newPackage, newColor, newUnits, newDescription, newVendor, newLocation)
        
        # Open connection to database
        connection = sqlite3.connect("inventory.db")
        cur = connection.cursor()
        
        # Insert data into the database
        cur.execute("INSERT INTO Inventory VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        connection.commit()
        connection.close()
        
    # Closes window given client input - Attach to widget
    def closeWindow(self):
        self.close()
        
# main
app = QApplication(sys.argv)
win = RemoveDataWindow()

win.show()
sys.exit(app.exec_())