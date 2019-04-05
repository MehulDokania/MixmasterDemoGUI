from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

import os
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setFixedSize(400,400)

        layout = QVBoxLayout()
        self.editor = QPlainTextEdit()  # Could also use a QTextEdit and set self.editor.setAcceptRichText(False)


        #Setup the QTextEdit editor configuration
       # fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        #fixedfont.setPointSize(12)
        #self.editor.setFont(fixedfont)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        #layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        
        

        #File Tab

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)   
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(QIcon(os.path.join('images', 'blue-folder-open-document.png')), "Open file...", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join('images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(QIcon(os.path.join('images', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        
        #Create Tab
        create_toolbar = QToolBar("View")
        create_toolbar.setIconSize(QSize(14,14))
        self.addToolBar(create_toolbar)
        create_menu = self.menuBar().addMenu("&Create")

        create_gas = QAction(QIcon(os.path.join('images','gas.jpg')) , "New Gas" , self)
        create_gas.setStatusTip("Make a new Gas mixture")
        create_toolbar.addAction(create_gas)
        create_menu.addAction(create_gas)

        create_mixture = QAction("Reaction Mixture" , self)
        create_mixture.setStatusTip("React different gas mixtures")
        create_menu.addAction(create_mixture)


        #View Tab

        view_toolbar = QToolBar("View")
        view_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(view_toolbar)
        view_menu = self.menuBar().addMenu("&View")

        thermo_state = QAction(QIcon(os.path.join('images', 'state.png')), "Thermodynamic State", self)
        thermo_state.setStatusTip("View thermodynamic state of your composition")
        view_toolbar.addAction(thermo_state)
        view_menu.addAction(thermo_state)

        rxn_paths = QAction("Reaction Paths" , self)
        view_menu.addAction(rxn_paths)

        rxn_list = QAction("Reaction List" , self)
        view_menu.addAction(rxn_list)

        #Mechanisms Tab

        mech_menu = self.menuBar().addMenu("&Mechanisms")


        #About Tab

        about_menu = self.menuBar().addMenu("&About")

        about_mixm = QAction("Mixmaster",self)
        about_cantera = QAction("Cantera",self)

        about_menu.addAction(about_mixm)
        about_menu.addAction(about_cantera)

        self.textbox = QLineEdit(self)
        self.textbox.move(70, 200)
        self.textbox.resize(100,30)

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(70, 150)
        self.textbox1.resize(100,30)

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(70, 100)
        self.textbox2.resize(100,30)


 
        self.label1 = QLabel("O2", self)
        self.label1.move(38,200)

        self.label2 = QLabel("H2", self)
        self.label2.move(38,100)

        self.label3 = QLabel("N2", self)
        self.label3.move(38,150)

        self.label = QLabel("Composition" , self)
        
        self.label.setGeometry(40,30,200,100)

        textboxValue = self.textbox.text()
        self.textbox.setText("")

        self.update_title()
        self.show()



    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Text documents (*.txt);All files (*.*)")

        try:
            with open(path, 'rU') as f:
                text = f.read()

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.editor.setPlainText(text)
            self.update_title()

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")
        text = self.editor.toPlainText()

        if not path:
            # If dialog is cancelled, will return ''
            return

        try:
            with open(path, 'w') as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle("%s - MixMaster" % (os.path.basename(self.path) if self.path else "V2"))

    


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setApplicationName("MixMaster")

    window = MainWindow()
    
    app.exec_()