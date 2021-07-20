# -*- coding: utf-8 -*-
"""
@author: Oscar Ortiz
Last Modified on Mon Jul 19 18:56:58 2021
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QAction, qApp
from PyQt5.QtGui import QIcon

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.statusBar().showMessage('Connected')
        
        self.setStyleSheet("background-color: lightblue;")
        self.setGeometry(300, 300, 700, 300)
        self.setWindowTitle('PaintAndSave')
        self.setWindowIcon(QIcon('paintIcon.png'))
        
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)
        
        self.show()

def main():
    
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
   
if __name__ == '__main__':
   main()