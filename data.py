import sys
import sqlite3
from addData import AddDataWindow
from printData import PrintDataWindow

from tableModel import TableModel
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QSortFilterProxyModel, pyqtSignal, QObject, pyqtSlot
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QTableView,
    QDialog,
    QWidget,
    QTableWidgetItem,
    QCheckBox,
    QHBoxLayout
)

class Inventory(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("DatabaseApplication.ui", self)
        
        # Establishes table and loads data from database
        self.tableWidget.setHorizontalHeaderLabels(["ID (PK)", "Part #", "Sheen", "Brand", "Package", "Color/Base", "Units", "Description", "Vendor", "Location", "Edit?"])
        self.loadData()
        self.addButton.clicked.connect(self.insertData)
        self.loadButton.clicked.connect(self.loadData)
        self.editButton.clicked.connect(self.printData)
        
        # Establishes all dialog windows
        self.dialogAdd = AddDataWindow(self)
        self.dialogPrint = PrintDataWindow(self)
        
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setFixedHeight(30)
        self.tableWidget.setColumnCount(11)
        
        self.tableWidget.cellChanged.connect(self.recordData) # Trigger for checkbox status change
        
        self.pushButton_search.clicked.connect(self.filterData)
        
        # Set placeholder text for search lineEdits
        self.lineEdit_sheen.setPlaceholderText("Sheen")
        self.lineEdit_brand.setPlaceholderText("Brand")
        self.lineEdit_color.setPlaceholderText("Color/Base")
        
    # Loads all the data from database
    def loadData(self):
        connection = sqlite3.connect("inventory.db")
        cur = connection.cursor()
        sqlquery = "SELECT * FROM Inventory ORDER BY ID"
        
        cur.execute(sqlquery)
        
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
            
            # Sets a checkbox for each row
            checkBoxItem = QTableWidgetItem()
            checkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            checkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(tableRow, 10, checkBoxItem)
            self.tableWidget.item(tableRow, 10).setBackground(Qt.lightGray)
            
            tableRow += 1
            
        connection.close()
        
    # Moves 'checked' rows into Transition table and increments lcdNumber widget
    def recordData(self, row, col):
        currentNum = self.lcdNumber.value()
        uniqueID = self.tableWidget.item(row, 0).text()
        connection = sqlite3.connect("inventory.db")
        cur = connection.cursor()
        
        # If checkbox is checked adds data to Transition table
        if self.tableWidget.item(row, col).checkState() == QtCore.Qt.Checked:
            self.lcdNumber.display(currentNum + 1)
            
            cur.execute("SELECT * FROM Inventory WHERE ID = " + uniqueID)
            data = cur.fetchall()
            cur.execute("INSERT INTO Transition (ID, Part_Num, Sheen, Brand, Package, Color, Units, Description, Vendor, Location) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data[0])
            connection.commit()
        
        # If checkbox is unchecked removes data from Transition table
        else:
            self.lcdNumber.display(currentNum - 1)   
            cur.execute("DELETE FROM Transition WHERE ID = " + uniqueID)
            connection.commit()
            
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
    
    def insertData(self):
        self.dialogAdd.show()
        self.loadData()
        
    def printData(self):
        self.dialogPrint.loadPrintData()
        self.dialogPrint.show()
    

# main
app = QApplication(sys.argv)
win = Inventory()

widget = QtWidgets.QStackedWidget()
widget.addWidget(win)
widget.setFixedHeight(750)
widget.setFixedWidth(1200)

widget.show()
sys.exit(app.exec_())