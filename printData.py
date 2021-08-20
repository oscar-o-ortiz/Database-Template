import sys
import sqlite3

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableView,
    QDialog,
    QWidget
)

class PrintDataWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("printDataWindow.ui", self)
        
        self.tableWidget.setHorizontalHeaderLabels(["ID (PK)", "Part #", "Sheen", "Brand", "Package", "Color/Base", "Units", "Description", "Vendor", "Location", "Edit?"])
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setFixedHeight(30)
        self.tableWidget.setColumnCount(10)
        
        self.pushButton_search.clicked.connect(self.filterData)

    def loadPrintData(self):
        connection = sqlite3.connect("inventory.db")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM Transition ORDER BY ID"
        
        # Enters loaded data into the tableWidget
        rowCount = 0
        tableRow = 0
        self.tableWidget.setRowCount(rowCount)
        
        for row in cur.execute(sqlquery):
            rowCount += 1
            self.tableWidget.setRowCount(rowCount)
            
            self.tableWidget.setItem(tableRow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tableRow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tableRow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tableRow, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.tableWidget.setItem(tableRow, 4, QtWidgets.QTableWidgetItem(row[4]))
            self.tableWidget.setItem(tableRow, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.tableWidget.setItem(tableRow, 6, QtWidgets.QTableWidgetItem(row[6]))
            self.tableWidget.setItem(tableRow, 7, QtWidgets.QTableWidgetItem(row[7]))
            self.tableWidget.setItem(tableRow, 8, QtWidgets.QTableWidgetItem(row[8]))
            self.tableWidget.setItem(tableRow, 9, QtWidgets.QTableWidgetItem(row[9]))
            
            tableRow += 1
            
        connection.close()
        
    def filterData(self):
        sheen = self.lineEdit_sheen.text()
        brand = self.lineEdit_brand.text()
        color = self.lineEdit_color.text()
        
        for i in range(0, self.tableWidget.rowCount()):
            itemSheen = self.tableWidget.item(i, 2)
            itemBrand = self.tableWidget.item(i, 3)
            itemColor = self.tableWidget.item(i, 5)
            
            if len(sheen) > 0 and itemSheen.text().count(sheen) <= 0 and itemSheen.text().lower().count(sheen) <= 0:
                self.tableWidget.setRowHidden(i, True)
                continue
            
            if len(brand) > 0 and itemBrand.text().count(brand) <= 0 and itemBrand.text().lower().count(brand) <= 0:
                self.tableWidget.setRowHidden(i, True)
                continue
                
            if len(color) > 0 and itemColor.text().count(color) <= 0 and itemColor.text().lower().count(color) <= 0:
                self.tableWidget.setRowHidden(i, True)
                continue
            
            self.tableWidget.setRowHidden(i, False)