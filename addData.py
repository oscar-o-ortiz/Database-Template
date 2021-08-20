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

class AddDataWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("addDataWindow.ui", self)
        
        self.commitButton.clicked.connect(self.addData)
        self.resetButton.clicked.connect(self.clearData)
        
        self.comboBox_sheen.addItems(["", "Semi-Gloss", "High-Gloss", "Gloss", "Satin", "Eggshell", "Flat"])
        self.comboBox_package.addItems(["", "gal", "2gal", "5gal", "quart", "tote"])
        self.comboBox_sheen.currentIndexChanged.connect(self.selectionChange)
        
    def selectionChange(self):
        print(self.comboBox_sheen.currentText())
        
    # Add data to the sqlite3 database using client input
    def addData(self, data): 
        # Read data from the QTextEdit widgets and QComboBox widgets
        newPart = self.lineEdit_part.text()
        newSheen = self.comboBox_sheen.currentText()
        newBrand = self.lineEdit_brand.text()
        newPackage = self.comboBox_package.currentText()
        newColor = self.lineEdit_color.text()
        newUnits = self.lineEdit_units.text()
        newVendor = self.lineEdit_vendor.text()
        newLocation = self.lineEdit_location.text()
        newDescription = self.lineEdit_description.text()
        
        data = (newPart, newSheen, newBrand, newPackage, newColor, newUnits, newDescription, newVendor, newLocation)
        
        # Open connection to database
        connection = sqlite3.connect("inventory.db")
        cur = connection.cursor()
        
        # Insert data into the database
        cur.execute("INSERT INTO Inventory (Part_Num, Sheen, Brand, Package, Color, Units, Description, Vendor, Location) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        connection.commit()
        connection.close()
        
        self.closeWindow()
        
    # Closes window given client input - Attach to widget
    def closeWindow(self):
        self.close()
        
    # Displays an empty string on all lineEdits and comboBoxes
    def clearData(self):
        self.lineEdit_part.setText("")
        self.comboBox_sheen.setCurrentIndex(0)
        self.lineEdit_brand.setText("")
        self.comboBox_package.setCurrentIndex(0)
        self.lineEdit_color.setText("")
        self.lineEdit_units.setText("")
        self.lineEdit_vendor.setText("")
        self.lineEdit_location.setText("")
        self.lineEdit_description.setText("")    
        
        
        